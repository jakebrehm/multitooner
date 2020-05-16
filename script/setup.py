"""
This script will build the application for running without Python installed.

Usage:
    Typically, one can just navigate to this directory in a terminal and
    use the command:
        python setup.py py2app
    but it might instead be necessary to use:
        python3 setup.py py2app
"""

from setuptools import setup

# Use pathlib to get the path of the project folder
import os
import pathlib
MAIN_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent
PROJECT_FOLDER = os.path.join(MAIN_DIRECTORY, 'multitooner')
DATA_FOLDER = os.path.join(MAIN_DIRECTORY, 'assets')

# Read the configuration file
APPLICATION_PATH = os.path.join(PROJECT_FOLDER, 'app.py')
MENUBAR_ICON_PATH = os.path.join(DATA_FOLDER, 'icon.ico')
APP_ICON_PATH = os.path.join(DATA_FOLDER, 'appicon.icns')

APP = [APPLICATION_PATH]
DATA_FILES = [
    MENUBAR_ICON_PATH,
    APP_ICON_PATH,
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'requests', 'tooner'],
    'iconfile': APP_ICON_PATH,
}

setup(
    app=APP,
    name='MultiTooner',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)