from PyQt4 import uic
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import pyqtSignal, QString
from PyQt4.QtGui import QDialog

sliderForm = uic.loadUiType("Slider.ui")[0]

class Slider(QDialog, sliderForm):
    finished =  pyqtSignal(QString)
    slide = pyqtSignal(int)

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setupBehaviour()

    def setupBehaviour(self):
        print "todo"
