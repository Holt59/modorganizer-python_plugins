# -*- encoding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QFrame

import mobase


class HideRunPanelPlugin(mobase.IPlugin):

    _runFrame: QFrame

    def __init__(self):
        super().__init__()

    def init(self, organizer: mobase.IOrganizer):
        """ For a IPlugin, the only place where things can be done is in init(). """
        self._organizer = organizer

        # mobase.IOrganizer has a few callbacks available:

        # onUserInterfaceInitialized is called when the UI has been initialized, so
        # we can use it to retrieve the actual run frame from the main window. Trying
        # to access the main window in init() would not work since the main window is
        # not yet created.
        self._organizer.onUserInterfaceInitialized(self._onUiInit)

        # We add a callback when plugin change to hide/show the run frame depending
        # on the setting.
        self._organizer.onPluginSettingChanged(self._onPluginSettingChanged)

        return True

    def _onUiInit(self, mainWindow: QMainWindow):
        self._runFrame = mainWindow.findChild(QFrame, "startGroup")  # type: ignore
        self._onPluginSettingChanged(
            self.name(),
            "visible",
            None,
            self._organizer.pluginSetting(self.name(), "visible"),
        )

    def _onPluginSettingChanged(
        self, pluginName: str, pluginKey: str, oldValue, newValue
    ):
        """ Note: oldValue and newValue are Union type (mobase.MoVariant), but
        MovVariant is not actually in mobase, so we cannot specify it currently. """
        if pluginName == self.name() and pluginKey == "visible":
            self._runFrame.setVisible(newValue)  # type: ignore

    def name(self):
        return "Hide Run Panel"

    def author(self):
        return "Holt59"

    def description(self):
        return self._tr("Hide the run panel")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.final)

    def isActive(self):
        return True

    def settings(self):
        # We have a single setting indicating if the run frame should be visible or
        # not. We use this in _onPluginSettingChanged.
        return [mobase.PluginSetting("visible", "run frame visible", False)]

    def _tr(self, str):
        return QCoreApplication.translate("HideRunPanelPlugin", str)


def createPlugin():
    return HideRunPanelPlugin()
