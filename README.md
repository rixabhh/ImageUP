# 🎨 ImageUP - AI Image Colorization

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 Project Overview

**ImageUP** is a full-stack web application that leverages Deep Learning to automatically colorize black-and-white images. 

The project integrates a **Flask** backend with **OpenCV's** DNN module to run Caffe models for image processing. The frontend is designed with **HTML5** and **Tailwind CSS**, providing a modern, drag-and-drop interface. The entire application is containerized using **Docker** for consistent deployment.

---

## 📂 Repository Structure

| File / Directory | Description |
| :--- | :--- |
| `app.py` | **Main Application**: Flask server handling routes, image processing, and inference logic. |
| `download_models.py` | **Setup Script**: Python script to automatically download the required Caffe model files. |
| `Dockerfile` | **Container Config**: Instructions to build the Docker image with Python 3.11 and system dependencies. |
| `requirements.txt` | **Dependencies**: List of Python libraries (`flask`, `opencv-python`, `numpy`, `gunicorn`). |
| `templates/index.html` | **Frontend**: User interface built with HTML and styled using Tailwind CSS (via CDN). |
| `models/` | **Model Storage**: Directory where `colorization_release_v2.caffemodel` and related files are stored. |
| `static/` | **Assets**: Contains `uploads/` for input images and `results/` for processed outputs. |

---

## 🛠️ Tech Stack & Dependencies

The project is built using the following technologies:

| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Core programming language. |
| **Web Framework** | Flask | Handles HTTP requests and routing. |
| **Computer Vision** | OpenCV (`cv2`) | Image manipulation and Deep Learning inference. |
| **Data Processing** | NumPy | Matrix operations for image tensors. |
| **Frontend** | HTML5, JavaScript | Structure and client-side logic. |
| **Styling** | Tailwind CSS | Utility-first CSS framework for the UI. |
| **Infrastructure** | Docker | Containerization and deployment. |
| **Server** | Gunicorn | WSGI HTTP Server for production. |

---

## ✨ Key Features

* **AI-Powered Colorization**: Utilizes the Zhang et al. (2016) Caffe model for realistic color prediction.
* **Drag & Drop Interface**: User-friendly upload zone with immediate visual feedback.
* **Real-time Processing**: Fast inference pipeline using OpenCV's optimized DNN backend.
* **Comparison View**: Side-by-side display of the original grayscale and the new colorized image.
* **Automatic Model Fetching**: `download_models.py` handles the retrieval of large model weights.

---

## 🚀 Usage Instructions

### Prerequisites
* **Docker** (Recommended)
* *OR* **Python 3.x** with `pip` installed.

### Option 1: Run with Docker (Easiest)
1.  **Build the Image**
    ```bash
    docker build -t imageup-app .
    ```
2.  **Run the Container**
    ```bash
    docker run -p 5000:5000 imageup-app
    ```
    Access the application at `http://localhost:5000`.

### Option 2: Run Locally (Python)
1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Download Models**
    The model files are too large for git. Run this script to fetch them:
    ```bash
    python download_models.py
    ```
3.  **Start the Server**
    ```bash
    python app.py
    ```
    Open your browser and navigate to `http://localhost:5000`.

---

## 🧠 Model Details

The application uses the **Colorful Image Colorization** algorithm.
* **Input**: Lightness channel (L) from the LAB color space.
* **Output**: Predicted 'a' and 'b' color channels.
* **Process**: The system combines the original L channel with the predicted ab channels to reconstruct the final color image.

---

## 👤 Author

**Rishabh**
* [GitHub Profile](https://github.com/rixabhh)