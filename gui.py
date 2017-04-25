import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from imagemusic import jpg_to_midi


class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        self.home()

    def home(self):

        layout = QtGui.QGridLayout()
        layout.setSpacing(5)

        self.imgTxt = QLineEdit()
        self.imgTxt.setReadOnly(True)

        imgBtn = QtGui.QPushButton("Choose image", self)
        imgBtn.clicked.connect(self.selectImage)

        self.gridTxt = QLineEdit()
        self.gridTxt.setReadOnly(True)

        gridBtn = QtGui.QPushButton("Choose map", self)
        gridBtn.clicked.connect(self.selectMap)

        self.dirTxt = QLineEdit()
        self.dirTxt.setReadOnly(True)

        dirBtn = QtGui.QPushButton("Choose output location", self)
        dirBtn.clicked.connect(self.selectDir)

        outLbl = QtGui.QLabel("Output MIDI Name")
        self.outTxt = QLineEdit()

        convertBtn = QtGui.QPushButton("Convert to MIDI")
        convertBtn.clicked.connect(self.selectConvert)

        layout.addWidget(imgBtn, 2, 0)
        layout.addWidget(self.imgTxt, 2, 1, 1, -1)

        layout.addWidget(gridBtn, 3, 0)
        layout.addWidget(self.gridTxt, 3, 1, 1, -1)

        layout.addWidget(dirBtn, 4, 0)
        layout.addWidget(self.dirTxt, 4, 1, 1, -1)

        fname = self.outTxt.text()
        layout.addWidget(outLbl, 5, 0)
        layout.addWidget(self.outTxt, 5, 1, 1, -1)

        layout.addWidget(convertBtn, 6, 4)
        
        self.setLayout(layout)

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("JPG2MIDI Converter")
        
        self.show()
        

    def selectImage(self):
        fname = QFileDialog.getOpenFileName(self, "Choose image...", "~/", "JPG Images (*.jpg)")
        self.imgTxt.setText(fname)
        self.imgName = fname

    def selectMap(self):
        fname = QFileDialog.getOpenFileName(self, "Choose duration map...", "~/", "CSV Files (*.csv)")
        self.gridTxt.setText(fname)
        self.mapName = fname

    def selectDir(self):
        self.dirName = QFileDialog.getExistingDirectory(self, "Choose save folder", "~/")
        self.dirTxt.setText(self.dirName)

    def selectConvert(self):
        print "hi"
        print self.imgName
        print self.mapName
        print self.dirName
        print self.outTxt.text()
        if hasattr(self, "imgName") and hasattr(self, "mapName") and hasattr(self, "dirName") and self.outTxt.text():
            print "we made it?"
            jpg_to_midi(self.imgName, self.mapName, self.dirName + "/" + self.outTxt.text())
        

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
