#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Main!")

        self.statusBar()
        self.setupMainMenu()
        self.showMaximized()

    def setupMainMenu(self):
        self.mainMenu = self.menuBar()

        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(self.setupNewAction())
        self.fileMenu.addAction(self.setupOpenAction())
        self.fileMenu.addAction(self.setupQuitAction())

        self.playerMenu = self.mainMenu.addMenu("&Player")
        self.playerMenu.addAction(self.setupAddPlayerAction())
        self.playerMenu.addAction(self.setupRemovePlayerAction())

        self.damageOverviewMenu = self.mainMenu.addMenu("&Damage Overview")
        self.damageOverviewMenu.addAction(self.setupGenerateDamageOverviewAction())

    def setupNewAction(self):
        self.newAction = QtGui.QAction("&New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create New Database")
        self.newAction.triggered.connect(self.new)
        return self.newAction

    def setupOpenAction(self):
        self.openAction = QtGui.QAction("&Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open existing Database")
        self.openAction.triggered.connect(self.open)
        return self.openAction

    def setupQuitAction(self):
        self.quitAction = QtGui.QAction("&Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit Application")
        self.quitAction.triggered.connect(self.close)
        return self.quitAction

    def setupAddPlayerAction(self):
        self.addPlayerAction = QtGui.QAction("&Add Player", self)
        self.addPlayerAction.setShortcut("Ctrl+A")
        self.addPlayerAction.setStatusTip("Add Player")
        self.addPlayerAction.triggered.connect(self.addPlayer)
        return self.addPlayerAction

    def setupRemovePlayerAction(self):
        self.removePlayerAction = QtGui.QAction("&Remove Player", self)
        self.removePlayerAction.setShortcut("Ctrl+R")
        self.removePlayerAction.setStatusTip("Remove Player")
        self.removePlayerAction.triggered.connect(self.removePlayer)
        return self.removePlayerAction

    def setupGenerateDamageOverviewAction(self):
        self.generateDamageOverviewAction = QtGui.QAction("&Generate Damage Overview", self)
        self.generateDamageOverviewAction.setShortcut("Ctrl+P")
        self.generateDamageOverviewAction.setStatusTip("Generate PDF with the damage overview")
        self.generateDamageOverviewAction.triggered.connect(self.generateDamageOverview)
        return self.generateDamageOverviewAction

    def new(self):
        print("New Database")

    def open(self):
        print("Open Existing Database")

    def close(self):
        print("Quiting")
        sys.exit()

    def addPlayer(self):
        print("Add Player")

    def removePlayer(self):
        print("Remove Player")

    def generateDamageOverview(self):
        print("Generate Damage Overview")
        printer = QtGui.QPrinter()
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName("DamageOverview.pdf")

        document = QtGui.QTextDocument()
        header = QtGui.QTextCursor(document)
        header.movePosition(QtGui.QTextCursor.Start)
        table = header.insertTable(1, 4)
        table.cellAt(0, 0).firstCursorPosition().insertText("Name")
        table.cellAt(0, 1).firstCursorPosition().insertText("Damage Type")
        table.cellAt(0, 2).firstCursorPosition().insertText("Damage Location")
        table.cellAt(0, 3).firstCursorPosition().insertText("Damage Amount")
        document.print_(printer)

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Main()
    sys.exit(app.exec_())

run()
