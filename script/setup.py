"""
This script will build the application for running without Python installed.

Usage:
    One must navigate to the parent directory of this directory in a terminal
    and use the command:
        python script/setup.py py2app
    but it might instead be necessary to use:
        python3 script/setup.py py2app
"""

from setuptools import setup

# Use pathlib to get the path of the project folder
import os
import pathlib
MAIN_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent
PROJECT_FOLDER = os.path.join(MAIN_DIRECTORY, 'multitooner')
DATA_FOLDER = os.path.join(MAIN_DIRECTORY, 'assets')

# Read the configuration file
MAIN_PATH = os.path.join(PROJECT_FOLDER, 'main.py')
APPLICATION_PATH = os.path.join(PROJECT_FOLDER, 'app.py')
PREFERENCES_PATH = os.path.join(PROJECT_FOLDER, 'preferences.py')
AUTHENTICATE_PATH = os.path.join(PROJECT_FOLDER, 'authenticate.py')
CONFIG_PATH = os.path.join(PROJECT_FOLDER, 'config.py')
LOGIN_PATH = os.path.join(PROJECT_FOLDER, 'login.py')
ICON_PATH = os.path.join(DATA_FOLDER, 'icon.icns')
MENUBAR_ICON_PATH = os.path.join(DATA_FOLDER, 'icon-desaturated.icns')

APP = [MAIN_PATH]
DATA_FILES = [
    APPLICATION_PATH,
    PREFERENCES_PATH,
    AUTHENTICATE_PATH,
    CONFIG_PATH,
    LOGIN_PATH,
    ICON_PATH,
    MENUBAR_ICON_PATH,
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': [
        'rumps',
        'requests',
        'tooner',
        'LaunchServices',
        'certifi',
    ],
    'iconfile': ICON_PATH,
}

setup(
    app=APP,
    name='MultiTooner',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)