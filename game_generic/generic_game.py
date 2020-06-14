# -*- encoding: utf-8 -*-

from PyQt5.QtCore import (
    QCoreApplication,
    QDir,
    QStandardPaths,
)
from PyQt5.QtGui import QIcon

import mobase

from .generic_moddatachecker import GenericGameModDataChecker
from .generic_moddatacontent import GenericGameModDataContent
from .generic_gameplugins import GenericGameGamePlugins
from .generic_savegameinfo import GenericGameSaveGameInfo


class GenericGame(mobase.IPluginGame):
    """
    Actual plugin class, extends the IPluginGame interface, meaning it adds support for
    a new game.
    """

    _organizer: mobase.IOrganizer

    def __init__(self):
        super(GenericGame, self).__init__()
        self.__featureMap = {}

    # IPlugin interface:

    def init(self, organizer):
        """
        Initialize the plugin here.
        If you are able to detect game installation you may do so here and already set
        the various paths.
        MO2 will call setGamePath() in case the user already has an instance or selects
        a custom location.
        """

        self._organizer = organizer

        self.__featureMap[mobase.GamePlugins] = GenericGameGamePlugins(organizer)
        self.__featureMap[mobase.SaveGameInfo] = GenericGameSaveGameInfo(organizer)
        self.__featureMap[mobase.ModDataContent] = GenericGameModDataContent(
            organizer, self
        )
        self.__featureMap[mobase.ModDataChecker] = GenericGameModDataChecker()
        self.m_GamePath = ""
        self.m_DataPath = ""
        self.m_DocumentsPath = ""

        return True

    def name(self):
        """
        @return name of this plugin (used for example in the settings menu).
        @note Please ensure you use a name that will not change. Do NOT include a
        version number in the name.
        Do NOT use a localizable string (tr()) here.
        Settings for example are tied to this name, if you rename your plugin you lose
        settings users made.
        """
        return "GenericGamePlugin"

    def author(self):
        """
        @return author of this plugin.
        AnyOldName3 for initial fake game mock implementation,
        AL12 for generic game support and documentation comments,
        """
        return "AnyOldName3, AL12, Holt59"

    def description(self):
        """
        @return a short description of the plugin to be displayed to the user
        """
        return self.__tr(
            "Adds support for a generic game (this is basically a hack, so expect some "
            "features to not work or be unavailable)."
        )

    def version(self):
        """
        @return version of the plugin. This can be used to detect outdated versions of
        plugins.
        """
        return mobase.VersionInfo(0, 1, 0, mobase.ReleaseType.prealpha)

    def isActive(self):
        """
        @brief called to test if this plugin is active. inactive plugins can still be
            configured and report problems but otherwise have no effect.
            For game plugins this is currently ignored during instance creation!
        @return true if this plugin is active.
        """
        return True

    def settings(self):
        """
        @return list of configurable settings for this plugin. The list may be empty.
        This could be used for example to allow users to change some of the parameters
        of this plugin.
        Example: [mobase.PluginSetting("enabled", self.__tr("Enable this plugin), True)]
        To retrieve it: isEnabled = self.__organizer.pluginSetting(self.name(),
        "enabled")
        """
        return [
            mobase.PluginSetting(
                "content", self.__tr("enable content visualization"), True
            )
        ]

    def isContentVisualizationEnabled(self):
        return self._organizer.pluginSetting(self.name(), "content")

    """
    Here IPluginGame interface stuff.
    """

    def gameName(self):
        """
        @return name of the game.
        """
        return "Generic Game"

    def gameShortName(self):
        """
        @brief Get the 'short' name of the game.

        The short name of the game is used for savegames, registry entries,
        Nexus API calls and some MO2 internal settings storage.
        """
        return "GenericGame"

    def gameIcon(self):
        """
        @return an icon for this game (QIcon constructor accepts a path).
        """
        return QIcon()

    def validShortNames(self):
        """
        @brief Get the list of valid game names, this is also used to accept
            alternative game sources. Eg: Skyrim nexus for SSE.

        Originally the short name was used for Nexus stuff but then Nexus changed the
        game identifiers forcing Mo2 to add the gameNexusName() to use the correct one.
        """
        return [self.gameShortName()]

    def gameNexusName(self):
        """
        @brief get the Nexus name of the game, used for API calls and for mod pages
        resolution.
        """
        return ""

    def nexusModOrganizerID(self):
        """
        @brief Get the Nexus ID of the Mod Organizer page for this game.
        Use 0 if no page exists.
        """
        return 0

    def nexusGameID(self):
        """
        @brief Get the Nexus Game ID (you may find this in a download link from nexus).
        """
        return 0

    def steamAPPId(self):
        """
        @return steam app id for this game. Should be empty for games not
            available on steam
        @note if a game is available in multiple versions those might have different
            app ids. the plugin should try to return the right one
        """
        return ""

    def binaryName(self):
        """
        @brief Get the name of the executable that gets run.
        """
        return ""

    def getLauncherName(self):
        """
        @brief Get the name of the game launcher.
        """
        return ""

    def executables(self):
        """
        @return list of automatically discovered executables of the game itself and
            tools surrounding it.
        This is a list of
            mobase.ExecutableInfo("Display name", QFileInfo("absolute/path/to/exe"))
        The path can either be absolute or relative to the gameDirectory.
        """
        return []

    def savegameExtension(self):
        """
        @return file extension of save games for this game.
        """
        return "save"

    def savegameSEExtension(self):
        """
        @return file extension of script extender save game files for this game.
        """
        return ""

    def initializeProfile(self, path, settings):
        """
        @brief initialize a profile for this game.
        @param path the directory where the profile is to be initialized.
        @param settings parameters for how the profile should be initialized.
        @note this function will be used to initially create a profile, potentially
            to repair it or upgrade/downgrade it so the implementations
            have to gracefully handle the case that the directory already contains
            files!
        """
        pass

    def primarySources(self):
        return []

    def primaryPlugins(self):
        """
        @return list of plugins that are part of the game and not considered optional.
        """
        return []

    def gameVariants(self):
        """
        @return list of game variants
        @note If there are multiple variants of a game (and the variants make a
            difference to the plugin) like a regular one and a GOTY-edition the plugin
            can return a list of them and the user gets to chose which one he owns.
        """
        return []

    def setGameVariant(self, variantStr):
        """
        @brief if there are multiple game variants (returned by gameVariants) this will
            get called on start with the user-selected game edition allowing for manual
            internal adjustments.
        @param variant the game edition selected by the user
        """
        pass

    def gameVersion(self):
        """
        @brief return version of the managed game.
        """
        return "1"

    def iniFiles(self):
        """
        @brief Get the list of .ini files this game uses.

        @note just the name, these are all assumed residing in the documentsDirectory().
        @note It is important that the 'main' .ini file comes first in this list.
        """
        return []

    def DLCPlugins(self):
        """
        @brief Get a list of esp/esm files that are part of known dlcs.
        """
        return []

    def CCPlugins(self):
        """
        @brief Get the current list of active Creation Club plugins.
        """
        return []

    def loadOrderMechanism(self):
        """
        @brief determine the load order mechanism used by this game.

        @note this may throw an exception if the mechanism can't be determined.

        Either:
            FileTime,
            PluginsTxt

        Leave to PluginsTxt in case the game does not use plugins.
        """
        return mobase.LoadOrderMechanism.PluginsTxt

    def sortMechanism(self):
        """
        @brief determine the sorting mech
        Either:
            NONE,
            MLOX,
            BOSS,
            LOOT
        """
        return mobase.SortMechanism.NONE

    def looksValid(self, aQDir):
        """
        @brief See if the supplied directory looks like a valid installation of the
            game.
        """
        return True

    def isInstalled(self):
        """
        @return true if this game has been discovered as installed, false otherwise.

        Used to allow fast instance creation. This function can be used to check
        registry keys for the path of the game and setting the internal game/data
        directories.
        """
        return False

    def gameDirectory(self):
        """
        @return directory (QDir) to the game installation.
        """
        return QDir(self.m_GamePath)

    def dataDirectory(self):
        """
        @return directory (QDir) where the game expects to find its data files
            (virtualization target).
        """
        return QDir(self.m_DataPath)

    def setGamePath(self, pathStr):
        """
        @brief set the path to the managed game.
        @param path to the game.
        @note this will be called by by MO to set the concrete path of the game. This
            is particularly relevant if the path wasn't auto-detected but had to be set
            manually by the user.
        """
        self.m_GamePath = pathStr
        self.m_DataPath = self.m_GamePath

    def documentsDirectory(self):
        """
        @return directory (QDir) of the documents folder where configuration files and
            such for this game reside.
        """
        return QDir(
            "{}/My Games/{}".format(
                QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
                self.gameName(),
            )
        )

    def savesDirectory(self):
        """
        @return path to where save games are stored.
        """
        return self.documentsDirectory()

    def _featureList(self):
        """
        Map of features that the game supports where each feature is a class abiding to
        an interface of one of the supported features found in the game_features project
        on the Modorganizer2 github.

        GamePlugins feature is currently mandatory as Mo2 will otherwise crash.
        """
        return self.__featureMap

    def __tr(self, str):
        return QCoreApplication.translate("GenericGame", str)
