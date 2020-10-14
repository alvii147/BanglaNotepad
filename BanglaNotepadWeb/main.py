from flask import Flask, render_template, request, redirect, url_for, jsonify
import base64
import numpy as np
import tensorflow as tf
from PIL import Image
from PIL import ImageOps

def modified_sigmoid(x, a, b):
    exponent = (-a * x) - b
    return 1/(1 + np.exp(exponent))

def get_image_data(filename):
    img = Image.open(filename)
    img = img.resize((28, 28), Image.ANTIALIAS)
    img = np.array(img)
    img_arr = np.zeros(shape = (28, 28))
    for i in range(len(img)):
        for j in range(len(img[i])):
            img_arr[i][j] = modified_sigmoid(float(img[i][j][3])/255.0, 200, -60)
    return np.array(img_arr)

a_label_lut = []
with open("tf/a_label_lut.txt", encoding = "utf8") as readfile:
    lines = readfile.readlines()
    for i in range(len(lines)):
        a_label_lut.append(str(lines[i].strip()))

d_label_lut = []
with open("tf/d_label_lut.txt", encoding = "utf8") as readfile:
    lines = readfile.readlines()
    for i in range(len(lines)):
        d_label_lut.append(str(lines[i].strip()))

model_alphabets = tf.keras.models.load_model("tf/alphabets.model")
model_digits = tf.keras.models.load_model("tf/digits.model")

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        reqjson = str(request.get_json())
        img_data = reqjson[23:]
        with open("image.png", "wb") as imgfile:
            imgfile.write(base64.b64decode(img_data))
        img = get_image_data("image.png")
        img_array = np.array([img])
        if reqjson[0] == "0":
            digits_prediction = model_digits.predict(img_array)
            d_pred = d_label_lut[np.argmax(digits_prediction[0])]
            return jsonify(d_pred)
        else:
            alphabets_prediction = model_alphabets.predict(img_array)
            a_pred = a_label_lut[np.argmax(alphabets_prediction[0])]
            return jsonify(a_pred)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()