import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULTS_FOLDER'] = 'static/results'
app.config['MODEL_FOLDER'] = 'models'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Model paths
PROTOTXT = os.path.join(app.config['MODEL_FOLDER'], 'colorization_deploy_v2.prototxt')
MODEL = os.path.join(app.config['MODEL_FOLDER'], 'colorization_release_v2.caffemodel')
POINTS = os.path.join(app.config['MODEL_FOLDER'], 'pts_in_hull.npy')

net = None

def load_model():
    global net
    # Check if files exist
    missing = []
    if not os.path.exists(PROTOTXT): missing.append('colorization_deploy_v2.prototxt')
    if not os.path.exists(MODEL): missing.append('colorization_release_v2.caffemodel')
    if not os.path.exists(POINTS): missing.append('pts_in_hull.npy')

    if missing:
        print("!" * 50)
        print("MISSING MODEL FILES:")
        print(f"The following files are missing from '{app.config['MODEL_FOLDER']}':")
        for m in missing:
            print(f" - {m}")
        print("Please download them (e.g. from Richard Zhang's GitHub) and place them in the 'models' folder.")
        print("!" * 50)
        return False

    try:
        print("Loading model...")
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        pts = np.load(POINTS)
        
        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        
        net.getLayer(class8).blobs = [pts.astype("float32")]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
        print("Model loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

model_loaded = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not model_loaded:
        # Try loading again in case user added files
        if not load_model():
            return jsonify({'error': 'Model files are missing. Check server console for instructions.'}), 500
        
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Colorize
        try:
            colorized_filename = process_image(filepath, filename)
            return jsonify({
                'original_url': f"/static/uploads/{filename}",
                'colorized_url': f"/static/results/{colorized_filename}",
                'colorized_filename': colorized_filename
            })
        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({'error': str(e)}), 500

def process_image(path, filename):
    image = cv2.imread(path)
    if image is None:
        raise ValueError("Could not read image")
        
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    
    colorized = (255 * colorized).astype("uint8")
    
    result_filename = f"colorized_{filename}"
    result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
    cv2.imwrite(result_path, colorized)
    
    return result_filename

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    # Use the port Railway provides, or default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
