import sys
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QBrush, QColor

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

canvas_width = 200
canvas_height = 200
canvas_posX = 20
canvas_posY = 20
canvas_dash_width = 150
canvas_dash_height = 150
canvas_dash_posX = canvas_width/2 - canvas_dash_width/2
canvas_dash_posY = canvas_height/2 - canvas_dash_height/2
sigmoid_a = 200
sigmoid_b = -45

class Painter(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent = None)
        self._path = QPainterPath()
    
    def paintEvent(self, event):
        global canvas_width
        global canvas_height
        global canvas_posX
        global canvas_posY
        painter = QPainter(self)

        painter.setBrush(QBrush(QColor(255, 240, 230), Qt.SolidPattern))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRect(canvas_posX - 20, canvas_posY - 20, canvas_width + 20, canvas_height + 20)

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(230, 230, 255))
        pen.setStyle(Qt.DashLine)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(pen)
        painter.drawRect(canvas_dash_posX, canvas_dash_posY, canvas_dash_width, canvas_dash_height)

        pen.setWidth(13)
        pen.setColor(QColor(0, 0, 0))
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPath(self._path)
    
    def mousePressEvent(self, event):
        self._path.moveTo(event.pos())
        self.update()
    
    def mouseMoveEvent(self, event):
        self._path.lineTo(event.pos())
        self.update()
    
    def newPath(self):
        self._path = QPainterPath()
        self.update()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._width = 800
        self._height = 500
        self._x = 500
        self._y = -600
        self.initUI()
    
    def initUI(self):
        self.setGeometry(self._x, self._y, self._width, self._height)
        self.setStyleSheet("background-color: rgb(0, 0, 26)")

        self._predictThread = predictThread()
        self._predictThread.predictDone.connect(self.displayResult)

        global canvas_width
        global canvas_height
        global canvas_posX
        global canvas_posY
        self._paintlabel = QLabel(self)
        self._painter = Painter(self)
        self._painter.move(canvas_posX, canvas_posY)
        self._painter.resize(canvas_width, canvas_height)
        self.layout().addWidget(self._paintlabel)
        self.layout().addWidget(self._painter)

        pushButtonWidth = 90
        pushButtonHeight = 25
        x = canvas_posX + canvas_width + 20
        y = canvas_posY
        self.clearButton = QPushButton(self)
        self.clearButton.move(x, y)
        self.clearButton.resize(pushButtonWidth, pushButtonHeight)
        self.clearButton.setText("Clear")
        self.clearButton.setStyleSheet("background-color: rgb(153, 187, 255)")
        self.clearButton.clicked.connect(self.clearCanvas)

        y += 40
        self.predictButton = QPushButton(self)
        self.predictButton.move(x, y)
        self.predictButton.resize(pushButtonWidth, pushButtonHeight)
        self.predictButton.setText("Predict")
        self.predictButton.setStyleSheet("background-color: rgb(153, 187, 255)")
        self.predictButton.clicked.connect(self.predict)

        self.show()
    
    def clearCanvas(self):
        self._painter.newPath()
    
    def predict(self):
        screen = self.grab()
        screen.save("screen.png")
        self._predictThread.start()
    
    def displayResult(self, value):
        print("Match: " + str(value))

class predictThread(QThread):
    predictDone = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    
    def run(self):
        global canvas_width
        global canvas_height
        global canvas_posX
        global canvas_posY
        global sigmoid_a
        global sigmoid_b
        global a_label_lut
        global asc_label_lut
        global d_label_lut
        
        img = Image.open("screen.png")
        img = img.convert("L")
        img = ImageOps.invert(img)
        img = img.crop((canvas_posX, canvas_posY, canvas_posX + canvas_width, canvas_posY + canvas_height))
        img = img.resize((28, 28), Image.ANTIALIAS)
        img = np.array(img)
        img = np.divide(img, 255)
        
        x_test = np.array([img])
        for i in range(len(x_test[0])):
            for j in range(len(x_test[0][i])):
                x_test[0][i][j] = modified_sigmoid(x_test[0][i][j], sigmoid_a, sigmoid_b)
        
        #plt.imshow(x_test[0], cmap = "Greys")
        #plt.show()
        model_alphabets = tf.keras.models.load_model("alphabets.model")
        alphabets_prediction = model_alphabets.predict(x_test)
        a_pred = a_label_lut[np.argmax(alphabets_prediction[0])]
        self.predictDone.emit(str(a_pred))

def modified_sigmoid(x, a, b):
    exponent = (-a * x) - b
    return 1/(1 + np.exp(exponent))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Window()
    sys.exit(app.exec_())