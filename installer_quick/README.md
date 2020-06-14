# MO2 Python Plugins - Simple Installer

This plugin is the python equivalent of the official [`installer_quick`](https://github.com/modorganizer2/modorganizer-installer_quick)
plugin (written in C++).

The [`__init__.py`](__init__.py) file contains the usual `createPlugin()` function that is called
by Mod Organizer 2 to create the plugin. Importing sub-modules is done using relative import,
e.g., `from .installer import *`, to avoid issues.

## Generate files for shipping

This plugin contains a `.ui` file and uses Qt translation systems, so files need to be generated
before shipping.

:warning: &nbsp; You need a python environment with `PyQt5` installed to generate the files.

Generate the `.py` file for the install dialog:

```bash
# If you have multiple .ui file, you need to generate a .py file for each of them:
pyuic5 ui/simpleinstalldialog.ui -o ui/simpleinstalldialog.py
```

Generate the translation file:

```bash
# You need to specify all the files that may contain strings to be translated:
pylupdate5 installer.py ui/simpleinstalldialog.py -ts simple-installer.ts
```