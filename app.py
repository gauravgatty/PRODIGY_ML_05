from flask import Flask, request, jsonify, render_template
from PIL import Image
import os

app = Flask(__name__)

# Make sure upload folder exists
UPLOAD_FOLDER = "static"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Simple prediction logic (you can improve later)
def predict_image(image_path):
    # Dummy logic (replace later if needed)
    return "pizza", 285

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    food, calories = predict_image(path)

    return jsonify({
        "food": food,
        "calories": calories
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)