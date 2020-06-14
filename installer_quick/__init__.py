# -*- encoding: utf-8 -*-

"""
This file is the entry point of the module and must contain a createPlugin()
or createPlugins() function.
"""

from .installer import SimpleInstaller


def createPlugin() -> SimpleInstaller:
    return SimpleInstaller()
