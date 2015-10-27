#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

class RemovePlayerDialog(QtGui.QDialog):
    def __init__(self, players, parent = None):
        super(RemovePlayerDialog, self).__init__(parent)

        self.vbox = QtGui.QVBoxLayout(self)
        self.buttongroup = QtGui.QButtonGroup()
        for (playerId, playerName, playerImageFilename) in players:
            button = QtGui.QRadioButton(playerName)
            self.buttongroup.addButton(button, playerId)
            self.vbox.addWidget(button)
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.vbox.addWidget(buttons)

    def getRemovedPlayer(self):
        return (self.buttongroup.checkedId(), self.buttongroup.checkedButton().text())

    @staticmethod
    def getPlayerToRemove(players, parent = None):
        dialog = RemovePlayerDialog(players, parent)
        result = dialog.exec_()
        playerId, playerName = dialog.getRemovedPlayer()
        return (playerId, playerName, result == QtGui.QDialog.Accepted)

def loadPixmap(playerImageFilename):
    pixmap = QtGui.QPixmap(500, 500)
    image = QtGui.QImage(playerImageFilename)
    image = image.scaled(500, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    pixmap.convertFromImage(image)
    return pixmap

class PlayerLabel(QtGui.QLabel):
    def __init__(self, playerName, playerImageFilename, parent = None):
        super(PlayerLabel, self).__init__(parent)

        self.vbox = QtGui.QVBoxLayout(self)

        self.name = QtGui.QLabel(playerName)
        self.name.setAlignment(QtCore.Qt.AlignCenter)

        self.picture = QtGui.QLabel()
        self.picture.setPixmap(loadPixmap(playerImageFilename))

        self.vbox.addWidget(self.name)
        self.vbox.addWidget(self.picture)

        self.setLayout(self.vbox)

    def sizeHint(self):
        return self.vbox.sizeHint()


class ActivePlayerLabel(PlayerLabel):
    clicked = QtCore.pyqtSignal(int, 'QString', 'QString')

    def __init__(self, playerId, playerName, playerImageFilename, parent = None):
        super(ActivePlayerLabel, self).__init__(playerName, playerImageFilename, parent)

        self.playerId = playerId
        self.playerName = playerName
        self.playerImageFilename = playerImageFilename

    def mouseReleaseEvent(self, ev):
        self.clicked.emit(self.playerId, self.playerName, self.playerImageFilename)

class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Main!")

        self.statusBar()
        self.setupMainMenu()
        self.showMaximized()

        self.playersFilename = ""
        self.players = {}
        self.nextPlayerId = 1

        self.damagesFilename = ""
        self.damages = []

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

        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollAreaContents = QtGui.QWidget()
        self.scrollAreaContents.setGeometry(0, 0, 500 * 3, 500 * 3)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.grid = QtGui.QGridLayout()
        self.scrollAreaContents.setLayout(self.grid)
        self.setCentralWidget(self.scrollArea)

    def playerUpdate(self, playerId, playerName, playerImageFilename):
        print("playerUpdate" + ": " + str(playerId) + " " + playerName + " " + playerImageFilename)

    def updateMainWindow(self):
        row = 0
        column = 0
        for playerId in self.players.keys():
            if (column == 3):
                row = row + 1
                column = 0
            playerLabel = ActivePlayerLabel(playerId, self.players[playerId][0], self.players[playerId][1], self.scrollAreaContents)
            playerLabel.clicked.connect(self.playerUpdate)
            self.grid.addWidget(playerLabel, row, column)
            column = column + 1

    def displayWarning(self, title, text):
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.exec_()

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
        self.playersFilename = QtGui.QFileDialog.getSaveFileName(self, "Create New Players File", "Players.csv", "*.csv")
        if (self.playersFilename == ""):
            self.displayWarning("Error", "No valid players file selected!")
            return

        self.damagesFilename = QtGui.QFileDialog.getSaveFileName(self, "Create New Damages File", "Damages.csv", "*.csv")
        if (self.damagesFilename == ""):
            self.displayWarning("Error", "No valid damages file selected!")
            return

        self.writePlayers(self.playersFilename)
        self.writeDamages(self.damagesFilename)

        self.updateMainWindow()

    def readLines(self, filename):
        fd = open(filename, 'r')
        lines = fd.readlines()
        fd.close()
        return lines

    def readPlayers(self, filename):
        lines = self.readLines(filename)
        for line in lines:
            line = line.strip().split(';')
            playerId = int(line[0])
            playerName = line[1]
            playerImageFilename = line[2]
            if playerId not in self.players:
                self.players[playerId] = (playerName, playerImageFilename)
                if (playerId >= self.nextPlayerId):
                    self.nextPlayerId = playerId + 1
        print self.players
        print self.nextPlayerId

    def readDamages(self, filename):
        lines = self.readLines(filename)
        for line in lines:
            line = line.strip().split(';')
            self.damages.append((int(line[0]),line[1],line[2],int(line[3])))
        print self.damages

    def open(self):
        self.playersFilename = QtGui.QFileDialog.getOpenFileName(self, "Open Existing Players File", "Players.csv", "*.csv")
        if (self.playersFilename == ""):
            self.displayWarning("Error", "No valid players file selected!")
            return

        self.damagesFilename = QtGui.QFileDialog.getOpenFileName(self, "Open Existing Damages File", "Damages.csv", "*.csv")
        if (self.damagesFilename == ""):
            self.displayWarning("Error", "No valid damages file selected!")
            return

        self.players = {}
        self.readPlayers(self.playersFilename)
        self.damages = []
        self.readDamages(self.damagesFilename)

        self.updateMainWindow()

    def close(self):
        print("Quiting")
        sys.exit()

    def writePlayers(self, filename):
        fd = open(filename, 'w')
        lines = []
        for key in self.players.keys():
            lines.append(str(key) + ";" + self.players[key][0] + ";" + self.players[key][1] + "\n")
        fd.writelines(lines)
        fd.close()

    def writeDamages(self, filename):
        fd = open(filename, 'w')
        lines = []
        for damage in self.damages:
            lines.append(str(damage[0]) + ";" + damage[1] + ";" + damage[2] + ";" + str(damage[3]) + "\n")
        fd.writelines(lines)
        fd.close()

    def addPlayer(self):
        print("Add Player")

        # No players file selected
        if (self.playersFilename == ""):
            self.displayWarning("Error", "No valid players file selected!")
            return

        playerName, ok = QtGui.QInputDialog.getText(self, "Player details", "Enter the player's name:")
        if (not ok):
            self.displayWarning("Warning", "No player name entered! Cancelling player entry.")
            return

        playerImageFilename = QtGui.QFileDialog.getOpenFileName(self, "Open Player Image", "", "*.jpg")
        if (playerImageFilename == ""):
            self.displayWarning("Warning", "No player image selected! Cancelling player entry.")
            return

        self.players[self.nextPlayerId] = (playerName, playerImageFilename)
        self.nextPlayerId = self.nextPlayerId + 1

        self.writePlayers(self.playersFilename)

        self.updateMainWindow()
        
    def removePlayer(self):
        if (not self.players):
            return

        playerId, playerName, ok = RemovePlayerDialog.getPlayerToRemove(self.players, self)
        print(str(playerId) + ";" + playerName + ";" + str(ok))
        if (playerId in self.players):
            del self.players[playerId]
            self.writePlayers(self.playersFilename)
            self.updateMainWindow()

    def generateDamageOverview(self):
        print("Generate Damage Overview")

        filename = QtGui.QFileDialog.getSaveFileName(self, "Save Damage Overview", "DamageOverview.pdf", "*.pdf")

        printer = QtGui.QPrinter()
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(filename)

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
