# -*- encoding: utf-8 -*-

from typing import List

import mobase


class GenericGameGamePlugins(mobase.GamePlugins):
    """
    Game feature class for plugin type mods. This does nothing but was required
    at some point by MO2 (it is not required anymore!).
    """

    def __init__(self, organizer: mobase.IOrganizer):
        super().__init__()
        self._organizer = organizer
        self._lastRead = None

    def writePluginLists(self, pluginList: mobase.IPluginList):
        return

    def readPluginLists(self, pluginList: mobase.IPluginList):
        return

    def lightPluginsAreSupported(self) -> bool:
        return False

    def getLoadOrder(self) -> List[str]:
        return []
