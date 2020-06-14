# -*- encoding: utf-8 -*-

import os

from typing import List

import mobase


class GenericGameModDataContent(mobase.ModDataContent):

    """ The ModDataContent feature is used to show the contents of mod to user or
    to allow user to filter mod based on contents. """

    AL = 1
    AON3 = 2
    ISA = 3
    LP = 4
    LD = 5
    SILARN = 6

    def __init__(self, organizer: mobase.IOrganizer, gameplugin):
        super().__init__()
        self._iconpath = os.path.join(organizer.pluginDataPath(), "icons")
        self._gameplugin = gameplugin

    def getAllContents(self) -> List[mobase.ModDataContent.Content]:
        """ Retrieve the list of available contents for the corresponding game.

        Returns: The list of Content that can be found in the game. """

        # Note: This is a dummy example where we return a content per-MO2 developer:
        Content = mobase.ModDataContent.Content
        return [
            # To use Qt resource path (:/generic_game/ui/al), we need to generate the
            # resource file (see the README and resources.qrc). We could have used
            # path to the files:
            Content(self.AL, "AL, @Al12rs", ":/generic_game/ui/al"),
            Content(self.AON3, "AnyOldName3, @AnyOldName3", ":/generic_game/ui/aon3"),
            Content(self.ISA, "isa, @isanae", ":/generic_game/ui/isa"),
            Content(self.LP, "LePresidente, @LePresidente", ":/generic_game/ui/lp",),
            Content(self.LD, "LostDragonist, @LostDragonist", ":/generic_game/ui/ld"),
            Content(self.SILARN, "Silarn, @Silarn", ":/generic_game/ui/silarn"),
        ]

    def getContentsFor(self, fileTree: mobase.IFileTree) -> List[int]:
        """ Returns the list of content in the given tree.

        Args:
            fileTree: The tree to return contents for.

        Returns: The IDs of contents in the given tree. """
        import random

        # We return a random list of content (for a real plugin, you should check
        # the content of the tree):
        return [i for i in range(1, 7) if random.uniform(0, 1) < 0.5]
