from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("food_model.h5")

# Classes (must match your dataset folders)
classes = ['biryani', 'burger', 'dosa', 'pizza']

calories = {
    "pizza": 285,
    "burger": 295,
    "dosa": 168,
    "biryani": 290
}

def preprocess(img):
    img = img.resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files["image"]
        img = Image.open(file).convert("RGB")

        img = preprocess(img)

        pred = model.predict(img)
        class_name = classes[np.argmax(pred)]

        return jsonify({
            "food": class_name,
            "calories": calories[class_name]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)