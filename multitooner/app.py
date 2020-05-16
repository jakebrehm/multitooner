import configparser
import os
import pathlib

import rumps
import tooner

import preferences


class Application(rumps.App):

    def __init__(self, *args, **kwargs):
        # Initialize the application and set the icon
        super().__init__(*args, **kwargs)
        # self._set_icon('icon.ico')
        self._set_icon('appicon.icns')

        # Get the application support directory of the toontown engine
        self._toontown = rumps.application_support("Toontown Rewritten")

        # Read the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(self['config.ini'])

        # Add a "Launch All" item
        launch_all = rumps.MenuItem('Launch All')
        self.menu.add(launch_all)
        self.menu.add(None)
        # Create a menu item for each account in the config file
        for section in self.config.sections():
            item = rumps.MenuItem(section, callback=self._launch(section))
            self.menu.add(item)
        self.menu.add(None)
        # Make a nested preferences menu
        preferences = rumps.MenuItem('Preferences')
        preferences.add(rumps.MenuItem(
            'Add Account',
            callback=self._add_account,
        ))
        preferences.add(rumps.MenuItem('Remove Account'))
        preferences.add(rumps.MenuItem('Run at Startup'))
        self.menu.add(preferences)
        self.menu.add(None)

        for item in self.menu.items():
            print(item)

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

    def _add_account(self, event):
        window = preferences.AddAccount()
        while True:
            response = window.run()
            if response.clicked:
                text = [t for t in response.text.split('\n') if t]
                if len(text) == 3:
                    break
                else:
                    window = preferences.AddAccount()
                    window.message = (
                        'Please try again.\n\n'
                        'Replace the placeholders with your login information.'
                    )
                    continue
            else:
                return
        
        self.config.add_section(text[0])
        self.config.set(text[0], 'username', text[1])
        self.config.set(text[0], 'password', text[2])

        item = rumps.MenuItem(text[0], callback=self._launch(text[0]))
        self.menu.insert_before('SeparatorMenuItem_2', item)

        self._save_config()

    def _save_config(self):
        with open(self['config.ini'], 'w') as config:
            self.config.write(config)
        # self.config.write()

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
    rumps.debug_mode(True)
    Application("MultiTooner").run()
