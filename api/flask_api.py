from pathlib import Path
from io import BytesIO
import os
import numpy as np
from PIL import Image, ImageOps
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "deep_learning_model.h5"))
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = load_model(MODEL_PATH, compile=False)
print(f"CNN model loaded successfully from: {MODEL_PATH}")

def preprocess_image(file_bytes: bytes) -> np.ndarray:
    image = Image.open(BytesIO(file_bytes)).convert("L")
    image = ImageOps.fit(image, (28, 28), method=Image.Resampling.LANCZOS)
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    if len(model.input_shape) == 4:
        return pixels.reshape(1, 28, 28, 1)
    if len(model.input_shape) == 3:
        return pixels.reshape(1, 28, 28)
    raise ValueError(f"Unsupported model input shape: {model.input_shape}")

@app.get("/")
def index():
    return jsonify({"success": True, "message": "MNIST CNN Flask API is running inside Task 11 Docker Compose.", "endpoints": {"health": "/health", "predict": "/predict"}}), 200

@app.get("/health")
def health():
    return jsonify({"success": True, "status": "healthy", "model_loaded": model is not None}), 200

@app.post("/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "Missing image. Send it in form field 'file'."}), 400
    uploaded = request.files["file"]
    if not uploaded.filename:
        return jsonify({"success": False, "error": "No file selected."}), 400
    try:
        image_bytes = uploaded.read()
        if not image_bytes:
            return jsonify({"success": False, "error": "Uploaded file is empty."}), 400
        probabilities = np.asarray(model.predict(preprocess_image(image_bytes), verbose=0))[0]
        predicted_digit = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_digit])
        return jsonify({"success": True, "predicted_digit": predicted_digit, "confidence": confidence, "confidence_percent": round(confidence * 100, 2), "probabilities": [float(p) for p in probabilities]}), 200
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({"success": False, "error": "Could not process this image."}), 400

@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"success": False, "error": "File is too large (maximum 10 MB)."}), 413

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)