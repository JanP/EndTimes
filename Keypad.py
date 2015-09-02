from PyQt4 import uic
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import pyqtSignal, QString
from PyQt4.QtGui import QDialog

keypadForm = uic.loadUiType("Keypad.ui")[0]

class Keypad(QDialog, keypadForm):
	finished = pyqtSignal(int)
	keyPressed = pyqtSignal(int)
	backspace = pyqtSignal()

	def __init__(self, parent = None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.setupBehaviour()

	def setupBehaviour(self):
		self.key0.clicked.connect(self.handleKey0)
		self.key1.clicked.connect(self.handleKey1)
		self.key2.clicked.connect(self.handleKey2)
		self.key3.clicked.connect(self.handleKey3)
		self.key4.clicked.connect(self.handleKey4)
		self.key5.clicked.connect(self.handleKey5)
		self.key6.clicked.connect(self.handleKey6)
		self.key7.clicked.connect(self.handleKey7)
		self.key8.clicked.connect(self.handleKey8)
		self.key9.clicked.connect(self.handleKey9)
		self.keyCorr.clicked.connect(self.handleKeyCorr)
		self.keyOK.clicked.connect(self.handleKeyOK)

	def handleKey0(self):
		self.keyPressed.emit(0)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("0")))
		self.keypadDisplay.end(False)

	def handleKey1(self):
		self.keyPressed.emit(1)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("1")))
		self.keypadDisplay.end(False)

	def handleKey2(self):
		self.keyPressed.emit(2)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("2")))
		self.keypadDisplay.end(False)
		
	def handleKey3(self):
		self.keyPressed.emit(3)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("3")))
		self.keypadDisplay.end(False)
		
	def handleKey4(self):
		self.keyPressed.emit(4)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("4")))
		self.keypadDisplay.end(False)
		
	def handleKey5(self):
		self.keyPressed.emit(5)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("5")))
		self.keypadDisplay.end(False)
		
	def handleKey6(self):
		self.keyPressed.emit(6)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("6")))
		self.keypadDisplay.end(False)
		
	def handleKey7(self):
		self.keyPressed.emit(7)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("7")))
		self.keypadDisplay.end(False)
		
	def handleKey8(self):
		self.keyPressed.emit(8)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("8")))
		self.keypadDisplay.end(False)
		
	def handleKey9(self):
		self.keyPressed.emit(9)
		self.keypadDisplay.setText(self.keypadDisplay.text().append(QString.fromAscii("9")))
		self.keypadDisplay.end(False)
		
	def handleKeyCorr(self):
		self.backspace.emit()
		self.keypadDisplay.backspace()
		
	def handleKeyOK(self):
                value, ok = self.keypadDisplay.text().toInt(10)
                if (ok):
                        self.finished.emit(value)
