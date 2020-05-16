import configparser
import os
import pathlib

import rumps
import tooner

import login
import preferences


class Application(rumps.App):

    def __init__(self, *args, **kwargs):
        # Initialize the application and set the icon
        super().__init__(*args, **kwargs)
        self._set_icon('icon-desaturated.icns')

        # Get the application support directory of the toontown engine
        self._toontown = rumps.application_support("Toontown Rewritten")

        # Read the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(self['config.ini'])

        # Initialize the menu
        self._initialize_menu()

        # Update the Run at Login option
        self._update_login_option()

    def _initialize_menu(self):
        # Add a "Launch All" item
        launch_all = rumps.MenuItem('Launch All', callback=self._launch_all)
        self.menu.add(launch_all)
        self.menu.add(None)
        # Create a menu item for each account in the config file
        for account in self._accounts:
            item = rumps.MenuItem(account, callback=self._launch(account))
            self.menu.add(item)
        self.menu.add(None)
        # Make a nested preferences menu
        preferences = rumps.MenuItem('Preferences')
        preferences.add(rumps.MenuItem(
            'Add Account',
            callback=self._add_account,
        ))
        preferences.add(rumps.MenuItem(
            'Remove Account',
            callback=self._remove_account,
        ))
        preferences.add(None)
        self._login_option = rumps.MenuItem(
            'Run at Login',
            callback=self._login,
        )
        preferences.add(self._login_option)
        self.menu.add(preferences)
        self.menu.add(None)

    def _login(self, sender):
        original_state = self._login_option.state
        self._update_login_option()
        if sender.state == -1:
            return
        if original_state != sender.state:
            return
        sender.state = int(not sender.state)
        if sender.state:
            login.enable_run_at_login()
        else:
            login.disable_run_at_login()

    def _update_login_option(self):
        run_at_login = self._login_option
        if run_at_login.state == -1:
            return
        run_at_login.state = int(login.is_run_at_login_enabled())
        if run_at_login.state == -1:
            run_at_login.set_callback(None)

    def _launch(self, section):
        def wrapped(sender=None):
            # Read the login information for the first toon
            username = self.config[section]['username']
            password = self.config[section]['password']
            # Launch the game
            launcher = tooner.ToontownLauncher(self._toontown)
            launcher.play(username=username, password=password)
        return wrapped

    def _launch_all(self, sender):
        for account in self._accounts:
            self._launch(account)()

    def _add_account(self, sender):
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

    def _remove_account(self, sender):
        window = preferences.RemoveAccount()
        while True:
            response = window.run()
            if response.clicked:
                text = [t for t in response.text.split('\n') if t]
                if len(text) == 1 and text[0] in self._accounts:
                    break
                else:
                    window = preferences.RemoveAccount()
                    window.message = ('Please try again.\n\n' + window.message)
                    continue
            else:
                return
        
        self.config.remove_section(text[0])

        self.menu.pop(text[0])

        self._save_config()

    def _save_config(self):
        with open(self['config.ini'], 'w') as config:
            self.config.write(config)

    def _set_icon(self, item):
        try:
            self.icon = os.path.join(pathlib.Path(__file__).parent, item)
        except FileNotFoundError:
            PROJECT_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent
            DATA_FOLDER = os.path.join(PROJECT_DIRECTORY, 'assets')
            self.icon = os.path.join(DATA_FOLDER, item)

    def __getitem__(self, item):
        return os.path.join(rumps.application_support("MultiTooner"), item)

    @property
    def _accounts(self):
        return self.config.sections()


if __name__ == '__main__':
    rumps.debug_mode(True)
    Application("MultiTooner").run()
