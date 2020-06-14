# -*- encoding: utf-8 -*-

import mobase


class GenericGameModDataChecker(mobase.ModDataChecker):

    """ The ModDataChecker feature is used to check the content of mods during
    installationg and in the mod list. """

    def __init__(self):
        super().__init__()

    def dataLooksValid(
        self, tree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        """ Check if the given tree contains valid data.

        Args:
            tree: The tree to check.

        Returns: INVALID or VALID if the tree is invalid or valid, FIXABLE if the
            tree can be fixed by a call to fix().
        """

        # This is a dummy check: we only check if the tree is not empty:
        if tree:
            return mobase.ModDataChecker.VALID
        return mobase.ModDataChecker.INVALID

    def fix(self, tree: mobase.IFileTree) -> mobase.IFileTree:
        # This method can be used to fix the tree if dataLooksValid returned
        # mobase.ModDataChecker.FIXABLE.
        return tree
