# -*- encoding: utf-8 -*-

from typing import Optional, Union

# MO2 ships with PyQt5, so you can use it in your plugins:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets

# You need to import mobase to access it.
# Note: This import will obviously not work in a standard python interpreter,
# but if you set-up your ID appropriately (by specifying the location of mobase.pyi),
# you can enable auto-completion and type-checking for mobase.
import mobase

# Note: Use relative import for anything in submodules.
from .ui.simpleinstalldialog import Ui_SimpleInstallDialog


class SimpleInstallDialog(QtWidgets.QDialog):

    """
    This is the dialog that is shown before any installation. The user can modify
    the name of the plugin, cancel the installation or switch to a manual installation.

    The layout of the dialog is not created here but in the `ui/simpleinstalldialog.ui`
    file, so you need Qt Designer to modify it.
    """

    # Flag to indicate if the user chose to do a manual installation:
    _manual: bool = False

    def __init__(self, name: mobase.GuessedString, parent: QWidget):
        super().__init__(parent)

        # Set the ui file:
        self.ui = Ui_SimpleInstallDialog()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # mobase.GuessedString contains multiple names with various level of
        # "guess". Using .variants() returns the list of names, and doing str(name)
        # will return the most-likely value.
        for value in name.variants():
            self.ui.nameCombo.addItem(value)
        self.ui.nameCombo.completer().setCaseSensitivity(Qt.CaseSensitive)
        self.ui.nameCombo.setCurrentIndex(self.ui.nameCombo.findText(str(name)))

        # We need to connect the Ok / Cancel / Manual buttons. We can of course use
        # PyQt5 signal/slot syntax:
        self.ui.okBtn.clicked.connect(self.accept)
        self.ui.cancelBtn.clicked.connect(self.reject)

        def manualClicked():
            self._manual = True
            self.reject()

        self.ui.manualBtn.clicked.connect(manualClicked)

    def getName(self):
        return self.ui.nameCombo.currentText()

    def isManualRequested(self):
        return self._manual


class SimpleInstaller(mobase.IPluginInstallerSimple):

    """
    This is the actual plugin. MO2 has two types of installer plugin, this one is
    "simple", i.e., it will work directly on the file-tree contained in the archive.
    The purpose of the installer is to take the file-tree from the archive, check if
    it is valid (for this installer) and then modify it if required before extraction.
    """

    _organizer: mobase.IOrganizer

    def __init__(self):
        super().__init__()

    # Method for IPlugin - I will not details these here since those are quite
    # self-explanatory and are common to all plugins:

    def init(self, organizer: mobase.IOrganizer):
        self._organizer = organizer
        return True

    def name(self):
        return "Simple Installer (Python)"

    def author(self):
        return "Holt59"

    def description(self):
        return self._tr("Installer for very simple archives... In python!")

    def version(self):
        return mobase.VersionInfo(0, 1, 0, mobase.ReleaseType.PRE_ALPHA)

    def isActive(self):
        return self._organizer.pluginSetting(self.name(), "enabled")

    def settings(self):
        return [
            # It is usually a good idea to allow user to enable or disable plugins:
            mobase.PluginSetting("enabled", "check to enable this plugin", True),
            # Installer plugins usually do not allow user to change priority, but
            # since this is a mock plugin, it's a good idea to do so. The official
            # MO2 quick installer has a priority of 50, so using 55 our python
            # installer will be used instead of the official one.
            mobase.PluginSetting("priority", "priority of this installer", 55),
        ]

    # Method for IPluginInstallerSimple:

    def priority(self):
        return self._organizer.pluginSetting(self.name(), "priority")

    def isManualInstaller(self) -> bool:
        # This method should usually return False. Only the official MO2 manual
        # installer returns True for this.
        return False

    def _isDataTextArchiveTopLayer(
        self, tree: mobase.IFileTree, data_name: str
    ) -> bool:
        """ Check if the given tree corresponds to a "data-text archive".

        A "Data-Text Archive" contains a single folder named "data" or whatever the
        data directory is called for the current game, together with txt or pdf files.

        Args:
            tree: The tree to check.
            data_name: Name of the data folder (e.g., "data" for Bethesda games).

        Returns: True if the given tree is a data-text archive, False otherwise.
        """

        # We are looking for a single folder called `data_name` and some txt/pdf files.
        data_found = txt_found = False

        # You can iterate a mobase.IFileTree (but should not modify the tree while
        # iterating it):
        for e in tree:
            if e.isDir():
                # You can compare a tree entry with a string using ==. It is recommended
                # instead of doing e.name() == data_name because e == data_name is case
                # insensitive.
                if data_found or e == data_name:
                    return False
                data_found = True
            if e.isFile():
                # e.suffix() returns the extension of the file (without the .).
                if e.suffix().lower() not in ["txt", "pdf"]:
                    return False
                txt_found = True

        # The tree corresponds to a data-text archive if it contains a "data" folder and
        # some txt/pdf files:
        return data_found and txt_found

    def _getSimpleArchiveBase(
        self, tree: mobase.IFileTree, data_name: str, checker: mobase.ModDataChecker
    ) -> Optional[mobase.IFileTree]:
        """ Try to find the data folder in the given tree.

        Args:
            tree: Tree to look the data folder in.
            data_name: Name of the data folder (e.g., "data" for Bethesda games).
            checker: Checker to use to check if a tree is a data folder.

        Returns: A tree corresponding to the data-folder, or to a folder containing the
            data-folder with txt/pdfs files, or None if such folder was not found.
        """

        if checker is None:
            return None

        while True:
            # If the tree is valid, we simple return it:
            if checker.dataLooksValid(tree) == mobase.ModDataChecker.VALID:
                return tree
            # If the tree is a data-text archive, also return it:
            elif self._isDataTextArchiveTopLayer(tree, data_name):
                return tree
            # If the tree contains a single folder, recurse into it (this is very useful
            # since a lot of mod archives contains a useless folder at the root):
            elif len(tree) == 1 and tree[0].isDir():
                tree = tree[0]  # type: ignore
            else:
                return None

    def isArchiveSupported(self, tree: mobase.IFileTree) -> bool:
        """ Check if the given file-tree (from the archive) can be installed by this
        installer.

        Args:
            tree: The tree to check.

        Returns: True if the file-tree can be installed, false otherwise.
        """

        # Retrieve the name of the "data" folder:
        data_name = self._organizer.managedGame().dataDirectory().dirName()

        # Retrieve the mod-data-checker:
        checker: mobase.ModDataChecker = self._organizer.managedGame().feature(
            mobase.ModDataChecker
        )

        # Do the actual check - Convert to bool or do `is not None` to avoid
        # issue with Python > C++ conversion:
        return bool(self._getSimpleArchiveBase(tree, data_name, checker))

    def install(
        self,
        name: mobase.GuessedString,
        otree: mobase.IFileTree,
        version: str,
        modId: int,
    ) -> Union[mobase.InstallResult, mobase.IFileTree]:
        """ Perform the actual installation.

        Args:
            name: The "name" of the mod. This can be updated to change the name of the
                mod.
            otree: The original archive tree.
            version: The original version of the mod.
            modId: The original ID of the mod.

        Returns: We either return the modified file-tree (if the installation was
            successful), or a InstallResult otherwise.

        Note: It is also possible to return a tuple (InstallResult, IFileTree, str, int)
            containing where the two last members correspond to the new version and ID
            of the mod, in case those were updated by the installer.
        """

        # Retrieve the name of the "data" folder:
        data_name = self._organizer.managedGame().dataDirectory().dirName()

        # Retrieve the mod-data-checker:
        checker: mobase.ModDataChecker = self._organizer.managedGame().feature(
            mobase.ModDataChecker
        )

        # Retrieve the archive base:
        tree = self._getSimpleArchiveBase(otree, data_name, checker)

        # This should never happen, but better safe than sorry!
        if tree is None:
            return mobase.InstallResult.FAILED

        # We create the dialog and show it to the user:
        dialog = SimpleInstallDialog(name, self._parentWidget())

        # Note: Unlike the official installer, we do not have a "silent" setting,
        # but it is really simple to add it.
        if dialog.exec() == QtWidgets.QDialog.Accepted:

            # We update the name with the user specified one:
            name.update(dialog.getName(), mobase.GuessQuality.USER)

            # If the archive is a "data-text archive", we set the root to the
            # data folder and move everything in it (using detach() and merge()):
            if self._isDataTextArchiveTopLayer(tree, data_name):

                # We get the "data" folder:
                ntree: mobase.IFileTree = tree.find(data_name)  # type: ignore

                # .detach() remove the entry from its parent, so the "data" tree is
                # removed from the original tree:
                ntree.detach()

                # .merge() will move everything from the original tree in the "data"
                # folder:
                ntree.merge(tree)

                # The tree is now the "data" folder:
                tree = ntree

            # We return the modified tree to the installation manager.
            # Note: Unlike the C++ version, we need to return the new tree since
            # assigning `tree = ...` is not sufficient in Python.
            return tree

        # If user requested a manual installation, we update the name (to keep it
        # in the manual installation dialog) and just notify the installation manager:
        elif dialog.isManualRequested():
            name.update(dialog.getName(), mobase.GuessQuality.USER)
            return mobase.InstallResult.MANUAL_REQUESTED

        # If user canceled, we simply notify the installation manager:
        else:
            return mobase.InstallResult.CANCELED

    def _tr(self, str):
        # We need this to translate string in Python. Check the common documentation
        # for more details:
        return QApplication.translate("SimpleInstallerPython", str)
