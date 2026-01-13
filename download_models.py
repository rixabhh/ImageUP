import os
import urllib.request
import sys

# Reliable URLs
FILES = {
    'colorization_deploy_v2.prototxt': 'https://raw.githubusercontent.com/richzhang/colorization/caffe/models/colorization_deploy_v2.prototxt',
    'pts_in_hull.npy': 'https://raw.githubusercontent.com/richzhang/colorization/caffe/resources/pts_in_hull.npy',
    'colorization_release_v2.caffemodel': 'https://storage.openvinotoolkit.org/repositories/datumaro/models/colorization/colorization_release_v2.caffemodel'
}

MODEL_DIR = 'models'

def download_file(url, filename):
    filepath = os.path.join(MODEL_DIR, filename)
    
    # Check if file exists and is valid (not empty or tiny error page)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 1024:
            print(f"[SKIP] {filename} exists ({size/1024/1024:.2f} MB).")
            return
        else:
            print(f"[RETRY] {filename} seems invalid (size {size} bytes). Downloading again...")
    
    print(f"[DOWNLOADING] {filename}...")
    try:
        def progress(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\rDownloading... {percent}%")
            else:
                sys.stdout.write(f"\rDownloading... {count * block_size / 1024:.1f} KB")
            sys.stdout.flush()
        
        # User-Agent strictly required for some servers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            total_size = int(response.getheader('Content-Length') or 0)
            block_size = 8192
            count = 0
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                out_file.write(buffer)
                count += 1
                progress(count, block_size, total_size)
        
        print("\n[DONE] Download complete.")

    except Exception as e:
        print(f"\n[ERROR] Failed to download {filename}: {e}")

def main():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    print(f"Checking models in {os.path.abspath(MODEL_DIR)}...")
    
    for filename, url in FILES.items():
        download_file(url, filename)
    
    print("\nAll tasks finished.")

if __name__ == "__main__":
    main()
