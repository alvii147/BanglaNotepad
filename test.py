import numpy as np
from PIL import Image
from PIL import ImageOps
import tensorflow as tf
import matplotlib.pyplot as plt

a_label_lut = []
asc_label_lut = []
d_label_lut = []

with open("a_label_lut.txt", encoding = "utf8") as readfile:
    lines = readfile.readlines()
    for i in range(len(lines)):
        a_label_lut.append(str(lines[i].strip()))

with open("asc_label_lut.txt", encoding = "utf8") as readfile:
    lines = readfile.readlines()
    for i in range(len(lines)):
        asc_label_lut.append(str(lines[i].strip()))

with open("d_label_lut.txt", encoding = "utf8") as readfile:
    lines = readfile.readlines()
    for i in range(len(lines)):
        d_label_lut.append(str(lines[i].strip()))

img = Image.open("test.png")
img = img.convert("L")
img = ImageOps.invert(img)
img = img.resize((28, 28), Image.ANTIALIAS)
img = np.array(img)
x_test = np.array([img])
for i in range(len(x_test[0])):
    for j in range(len(x_test[0][i])):
        x_test[0][i][j] = x_test[0][i][j]/255

model_alphabets = tf.keras.models.load_model("alphabets.model")
alphabets_prediction = model_alphabets.predict(x_test)

model_alphabets_sc = tf.keras.models.load_model("alphabets_sc.model")
alphabets_sc_prediction = model_alphabets_sc.predict(x_test)

model_digits = tf.keras.models.load_model("digits.model")
digits_prediction = model_digits.predict(x_test)

print(np.argmax(alphabets_prediction[0]))

a_pred = a_label_lut[np.argmax(alphabets_prediction[0])]
asc_pred = asc_label_lut[np.argmax(alphabets_sc_prediction[0])]
d_pred = d_label_lut[np.argmax(digits_prediction[0])]

print("ALPHABET: " + str(a_pred))
print("ALPHABET (SPECIAL CHARACTERS): " + str(asc_pred))
print("NUMERAL: " + str(d_pred))
plt.imshow(x_test[0], cmap="Greys")
plt.show()