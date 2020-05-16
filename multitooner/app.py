import configparser
import os
import pathlib

import rumps
import tooner


class Application(rumps.App):

    def __init__(self, *args, **kwargs):
        # Initialize the application and set the icon
        super().__init__(*args, **kwargs)
        self._set_icon('icon.ico')

        # Get the application support directory of the toontown engine
        self._toontown = rumps.application_support("Toontown Rewritten")

        # Read the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(self['config.ini'])

        # Create a menu item for each account in the config file
        for section in self.config.sections():
            item = rumps.MenuItem(section, callback=self._launch(section))
            self.menu.add(item)

    def _launch(self, section):
        toontown_launcher = tooner.ToontownLauncher
        def wrapped(*args, **kwargs):
            # Read the login information for the first toon
            username = self.config[section]['username']
            password = self.config[section]['password']
            # Launch the game
            launcher = toontown_launcher(self._toontown)
            launcher.play(username=username, password=password)
        return wrapped

    def _set_icon(self, item):
        try:
            self.icon = os.path.join(pathlib.Path(__file__).parent, item)
        except FileNotFoundError:
            PROJECT_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent
            DATA_FOLDER = os.path.join(PROJECT_DIRECTORY, 'assets')
            self.icon = os.path.join(DATA_FOLDER, item)

    def __getitem__(self, item):
        return os.path.join(rumps.application_support("MultiTooner"), item)


if __name__ == '__main__':
    # rumps.debug_mode(True)
    Application("MultiTooner").run()
