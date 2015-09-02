import sys

from PyQt4 import QtCore, QtGui

import Slider

def onFinished(value):
        print value
        QtGui.QApplication.closeAllWindows()

app = QtGui.QApplication(sys.argv)

slider = Slider.Slider(None)

slider.finished.connect(onFinished)

slider.show()

app.exec_()
