# Mod Organizer 2 - Python Plugins

This repository contains examples of python plugins for [Mod Organizer 2](https://github.com/ModOrganizer2/modorganizer).

## Available plugins

Each plugin is in its own folder, and you can install it by simply downloading [the archive](https://github.com/Holt59/modorganizer-python_plugins/archive/master.zip)
and extracting the corresponding folder to the `plugins/` folder of your MO2 installation.

:warning: &nbsp; These plugins are not meant to be used by normal MO2 users but are examples to get plugin
developers started.

:information_source: &nbsp; I tried to document each plugin as best as I could, so some plugins
might look overly commented. Some plugins requires to generate files using `PyQt5`, everything is
explained in the `README.md` in the folder.

## Common implementation details

There is currently two way to ship of Python plugin for Mod Organizer 2:
- Ship a single Python file (`.py`) and put it in the `plugins/` folder. The file should
 expose a `createPlugin()` or `createPlugins()` method that returns the created plugin or
 the list of created plugins.
- Ship a Python module (folder) containing the plugin and put it in the `plugins/` folder.
 This is now the recommended way if your plugins is made of multiple files or contains
 resources. This repository only contains example of this.

When using the second version, the `createPlugin()` or `createPlugins()` functions must be
exposed in the `__init__.py` file of the module. You should make sure to use relative
imports when importing sub-modules to avoid issues (see the various plugins).

*Note:* When using the simple `.py` file version, it is possible to ship resources or even
a whole module by having user put them in `plugins/data`, but that is not recommended
anymore.