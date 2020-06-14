# -*- encoding: utf-8 -*-

import os

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel

import mobase


class GenericGameSaveGame(mobase.ISaveGame):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename

    def getFilename(self):
        return self._filename

    def getCreationTime(self):
        return QDateTime(os.path.getmtime(self._filename))

    def getSaveGroupIdentifier(self):
        return "Holt59"

    def allFiles(self):
        return [self._filename]

    def hasScriptExtenderFile(self):
        return False


class GenericGameSaveGameInfoWidget(mobase.ISaveGameInfoWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self._label = QLabel()
        palette = self._label.palette()
        palette.setColor(self._label.foregroundRole(), Qt.white)
        self._label.setPalette(palette)
        layout.addWidget(self._label)
        self.setLayout(layout)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setSave(self, filename):
        self.setWindowTitle("The Title: {}".format(filename))
        self._label.setText("Showing save '{}'.".format(os.path.basename(filename)))
        self.resize(200, 50)


class GenericGameSaveGameInfo(mobase.SaveGameInfo):
    """
    Game feature class for plugin type mods.
    This is currently required to be implemented or Mo2 will crash.
    """

    def __init__(self, organizer):
        super().__init__()
        self._organizer = organizer

    def getSaveGameInfo(self, filename):
        return GenericGameSaveGame(filename)

    def getMissingAssets(self, filename):
        return {}

    def getSaveGameWidget(self, parent=None):
        return GenericGameSaveGameInfoWidget(parent)

    def hasScriptExtenderSave(self, filename):
        return False
