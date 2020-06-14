# -*- encoding: utf-8 -*-

# Force load of resources so that Qt can see them:
from .resources import *  # noqa

from .generic_game import GenericGame


def createPlugin():
    return GenericGame()
