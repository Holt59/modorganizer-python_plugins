# MO2 Python Plugins - Generic Game

This plugin is a generic game plugin inspired by [Al12rs](https://github.com/Al12rs)
[modorganizer-game_generic](https://github.com/Al12rs/modorganizer-game_generic).

The [`__init__.py`](__init__.py) file contains the usual `createPlugin()` function that is called
by Mod Organizer 2 to create the plugin. Importing sub-modules is done using relative import,
e.g., `from .installer import *`, to avoid issues.

## Creating Game Plugins

This example shows how to create a "complete" game plugins. If you are looking for a way to create
a simple game plugin, heads out to [Holt59's `basic_games` plugin](https://github.com/holt59/modorganizer-basic_games).

## Game features

Aisde the actual interface of MO2 `IPluginGame`, game plugins can expose game "features". These features
are optional but can improve the user-experience in some cases. Some of these features were initially created
for Bethesda's games, and thus have very little usage for other games, but other features can be very useful,
such as:
- the `ModDataChecker` feature can be used to check the content of mods and eventually fix archives during
    mod installation.
- the `ModDataContent` feature can be used to detect the contents of mods as shown in the "Content" column
    of MO2, and also in the list of filters.
- the `SaveGameInfo` feature can be used to display information on save game (e.g., for profile-specific saves),
    or to provide a save preview for the "Saves" tab.

## Generate files for shipping

This plugin contains a `.ui` file and uses Qt translation systems, so files need to be generated
before shipping.

:warning: &nbsp; You need a python environment with `PyQt5` installed to generate the files.

Generate the `.py` resource file containing the icons:

```bash
pyrcc5 -compress 2 -threshold 3 resources.qrc -o resources.py
```

:information_source: &nbsp; If you use Qt resources, do not forget to import `resources.py` before
using them. A good place to do so is the `__init__.py` file.

Generate the translation file:

```bash
# You need to specify all the files that may contain strings to be translated:
pylupdate5 generic_game.py generic_savegameinfo.py -ts game-generic.ts
```