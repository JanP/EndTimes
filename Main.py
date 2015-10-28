#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

class RemovePlayerDialog(QtGui.QDialog):
    def __init__(self, players, parent = None):
        super(RemovePlayerDialog, self).__init__(parent)

        self.vbox = QtGui.QVBoxLayout(self)
        self.buttongroup = QtGui.QButtonGroup()
        for playerId in players.keys():
            playerName, playerImageFilename = players[playerId]
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

class AddDamageDialog(QtGui.QDialog):
    def __init__(self, playerId, playerName, playerImageFilename, parent = None):
        super(AddDamageDialog, self).__init__(parent)

        vbox = QtGui.QVBoxLayout(self)

        hbox = QtGui.QHBoxLayout(vbox)

        playerLabel = PlayerLabel(playerName, playerImageFilename)
        hbox.addWidget(playerLabel)

        scrollArea = QtGui.QScrollArea(self)
        scrollAreaContents = QtGui.QWidget()
        scrollAreaContents.setGeometry(0, 0, 500, 500)
        scrollArea.setWidget(self.scrollAreaContents)
        self.grid = QtGui.QGridLayout()
        scrollAreaContents.setLayout(self.grid)
        hbox.addWidget(scrollArea)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

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

class AddDamageDialog(QtGui.QDialog):
    def __init__(self, playerId, playerName, playerImageFilename, parent = None):
        super(AddDamageDialog, self).__init__(parent)

        self.playerId = playerId

        self.row = 0

        vbox = QtGui.QVBoxLayout(self)
        widget = QtGui.QWidget()
        vbox.addWidget(widget)
        hbox = QtGui.QHBoxLayout(widget)

        playerLabel = PlayerLabel(playerName, playerImageFilename)
        hbox.addWidget(playerLabel)

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaContents = QtGui.QWidget()
        self.scrollAreaContents.setGeometry(0, 0, 500, 300)
        self.scrollAreaContents.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        scrollArea.setWidget(self.scrollAreaContents)
        self.grid = QtGui.QGridLayout()
        self.scrollAreaContents.setLayout(self.grid)

        amountLabel = QtGui.QLabel("Damage Amount", self.scrollAreaContents)
        amountLabel.setAlignment(QtCore.Qt.AlignCenter)
        amountLabel.setMaximumHeight(20)
        self.grid.addWidget(amountLabel, self.row, 0)
        typeLabel = QtGui.QLabel("Damage Type", self.scrollAreaContents)
        typeLabel.setAlignment(QtCore.Qt.AlignCenter)
        typeLabel.setMaximumHeight(20)
        self.grid.addWidget(typeLabel, self.row, 1)
        locationLabel = QtGui.QLabel("Damage Location", self.scrollAreaContents)
        locationLabel.setAlignment(QtCore.Qt.AlignCenter)
        locationLabel.setMaximumHeight(20)
        self.grid.addWidget(locationLabel, self.row, 2)

        self.row = self.row + 1

        self.moreButton = QtGui.QPushButton(self.scrollAreaContents)
        self.moreButton.setText("Add Damage")
        self.moreButton.clicked.connect(self.addDamageEntry)
        self.grid.addWidget(self.moreButton, self.row, 2)

        scrollArea.setMinimumWidth(self.scrollAreaContents.minimumSizeHint().width() + scrollArea.verticalScrollBar().width())

        hbox.addWidget(scrollArea)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

    def addDamageEntry(self):
        self.grid.removeWidget(self.moreButton)

        damageAmount = QtGui.QSpinBox(self.scrollAreaContents)
        self.grid.addWidget(damageAmount, self.row, 0)

        damageType = QtGui.QComboBox(self.scrollAreaContents)
        damageTypeList = QtCore.QStringList("Melee")
        damageTypeList.append("Firearms")
        damageTypeList.append("Explosives")
        damageTypeList.append("Zombie")
        damageType.addItems(damageTypeList)
        damageType.setEditable(False)
        damageType.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.grid.addWidget(damageType, self.row, 1)

        damageLocation = QtGui.QComboBox(self.scrollAreaContents)
        damageLocationList = QtCore.QStringList("Head")
        damageLocationList.append("Left Arm")
        damageLocationList.append("Right Arm")
        damageLocationList.append("Torso")
        damageLocationList.append("Left Leg")
        damageLocationList.append("Right Leg")
        damageLocation.addItems(damageLocationList)
        damageLocation.setEditable(False)
        damageLocation.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.grid.addWidget(damageLocation, self.row, 2)

        self.row = self.row + 1

        self.grid.addWidget(self.moreButton, self.row, 2)

        self.scrollAreaContents.setGeometry(0, 0, 500, self.grid.sizeHint().width())

    def getDamage(self):
        damages = []
        for row in range(1, self.grid.rowCount() - 1):
            damageAmount = self.grid.itemAtPosition(row, 0).widget().value()
            damageType = str(self.grid.itemAtPosition(row, 1).widget().currentText())
            damageLocation = str(self.grid.itemAtPosition(row, 2).widget().currentText())
            if (damageAmount == 0):
                continue
            damages.append((self.playerId, damageType, damageLocation, damageAmount))
        return damages

    @staticmethod
    def addDamageToPlayer(playerId, playerName, playerImageFilename, parent = None):
        dialog = AddDamageDialog(playerId, playerName, playerImageFilename, parent)
        result = dialog.exec_()
        damages = dialog.getDamage()
        return (damages, result == QtGui.QDialog.Accepted)

class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Main!")

        self.statusBar()
        self.setupMainMenu()
        self.setupCentralWidget()
        self.showMaximized()

        self.playersFilename = ""
        self.players = {}
        self.nextPlayerId = 1

        self.damagesFilename = ""
        self.damages = []

    def setupCentralWidget(self):
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollAreaContents = QtGui.QWidget()
        self.scrollAreaContents.setGeometry(0, 0, 500 * 3, 500 * 3)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.grid = QtGui.QGridLayout()
        self.scrollAreaContents.setLayout(self.grid)
        self.setCentralWidget(self.scrollArea)

    def setupMainMenu(self):
        self.mainMenu = self.menuBar()

        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(self.setupNewAction())
        self.fileMenu.addAction(self.setupOpenAction())
        self.fileMenu.addAction(self.setupQuitAction())

        self.playerMenu = self.mainMenu.addMenu("&Player")
        self.playerMenu.addAction(self.setupAddPlayerAction())
        self.playerMenu.addAction(self.setupRemovePlayerAction())

        self.damageMenu = self.mainMenu.addMenu("&Damage")
        self.damageMenu.addAction(self.setupGenerateDamageOverviewAction())
        self.damageMenu.addAction(self.setupClearDamagesAction())

    def playerUpdate(self, playerId, playerName, playerImageFilename):
        damages, ok = AddDamageDialog.addDamageToPlayer(playerId, playerName, playerImageFilename, self)
        if (not ok):
            return

        for damage in damages:
            self.damages.append(damage)
        
        self.writeDamages(self.damagesFilename)

    def updateMainWindow(self):
        row = 0
        column = 0
        self.setupCentralWidget()
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

    def setupClearDamagesAction(self):
        self.clearDamagesAction = QtGui.QAction("&Clear Damages", self)
        self.clearDamagesAction.setStatusTip("Clear all damages")
        self.clearDamagesAction.triggered.connect(self.clearDamages)
        return self.clearDamagesAction

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

    def readDamages(self, filename):
        lines = self.readLines(filename)
        for line in lines:
            line = line.strip().split(';')
            self.damages.append((int(line[0]),line[1],line[2],int(line[3])))

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
        self.writePlayers(self.playersFilename)
        self.writeDamages(self.damagesFilename)
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

        if (not ok):
            return

        if (playerId in self.players):
            del self.players[playerId]
            self.writePlayers(self.playersFilename)
            self.updateMainWindow()

    def generateDamageOverview(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save Damage Overview", "DamageOverview.pdf", "*.pdf")

        printer = QtGui.QPrinter()
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(filename)

        row = 0

        document = QtGui.QTextDocument()
        header = QtGui.QTextCursor(document)
        header.movePosition(QtGui.QTextCursor.Start)
        table = header.insertTable(1, 4)
        table.cellAt(0, 0).firstCursorPosition().insertText("Name")
        table.cellAt(0, 1).firstCursorPosition().insertText("Damage Type")
        table.cellAt(0, 2).firstCursorPosition().insertText("Damage Location")
        table.cellAt(0, 3).firstCursorPosition().insertText("Damage Amount")

        row = row + 1

        for damage in self.damages:
            table.appendRows(1)
            table.cellAt(row, 0).firstCursorPosition().insertText(self.players[damage[0]][0])
            table.cellAt(row, 1).firstCursorPosition().insertText(damage[1])
            table.cellAt(row, 2).firstCursorPosition().insertText(damage[2])
            table.cellAt(row, 3).firstCursorPosition().insertText(str(damage[3]))
            row = row + 1

        document.print_(printer)

    def clearDamages(self):
        self.damages = []
        self.writeDamages(self.damagesFilename)

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Main()
    sys.exit(app.exec_())

run()
