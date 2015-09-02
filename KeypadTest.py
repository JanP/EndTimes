import sys

from PyQt4 import QtCore, QtGui

import Keypad

def onFinished(value):
	print value
	QtGui.QApplication.closeAllWindows()

def onBackspace():
	print "backspace"

def onKeyPressed(number):
	print "Number: " + str(number)

app = QtGui.QApplication(sys.argv)

keypad = Keypad.Keypad(None)

keypad.finished.connect(onFinished)
keypad.keyPressed.connect(onKeyPressed)
keypad.backspace.connect(onBackspace)

keypad.show()

app.exec_()
