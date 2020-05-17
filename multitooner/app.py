import configparser
import os
import pathlib

import rumps
import tooner

import config
import login
import preferences


def update_menu(function):
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        self._update_menu_items()
    return wrapper


class Application(rumps.App):

    @update_menu
    def __init__(self, *args, **kwargs):
        # Initialize the application and set the icon
        super().__init__(*args, **kwargs)
        self._set_icon('icon-desaturated.icns')

        # Get the application support directory of the toontown engine
        self._toontown = rumps.application_support("Toontown Rewritten")

        # Initialize the configuration file and menu
        self.config = config.Configuration(self, 'config.ini')
        self._initialize_menu()

    def _initialize_menu(self):
        # Add a "Launch All" item
        self._launch_all_item = rumps.MenuItem(
            'Launch All',
            callback=self._launch_all,
        )
        self.menu.add(self._launch_all_item)
        self.menu.add(None)

        # Create a menu item for each account in the config file
        for account in self.accounts:
            item = rumps.MenuItem(account, callback=self._launch(account))
            self.menu.add(item)
        self.menu.add(None)

        # Make a nested preferences menu
        preferences = rumps.MenuItem('Preferences')
        preferences.add(rumps.MenuItem(
            'Add Account',
            callback=self._add_account,
        ))
        self._remove_account_item = rumps.MenuItem(
            'Remove Account',
            callback=self._remove_account,
        )
        preferences.add(self._remove_account_item)
        preferences.add(None)
        self._login_option = rumps.MenuItem(
            'Run at Login',
            callback=self._login,
        )
        preferences.add(self._login_option)
        self.menu.add(preferences)
        self.menu.add(None)

    def _update_menu_items(self):
        self._update_login_option()
        self._disable_if_no_accounts(
            self._launch_all_item,
            self._launch_all,
        )
        self._disable_if_no_accounts(
            self._remove_account_item,
            self._remove_account,
        )

    def _disable_if_no_accounts(self, item, callback):
        item.set_callback(callback if len(self.accounts) else None)

    def _update_login_option(self):
        run_at_login = self._login_option
        if run_at_login.state == -1:
            return
        run_at_login.state = int(login.is_run_at_login_enabled())
        if run_at_login.state == -1:
            run_at_login.set_callback(None)

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

    def _launch(self, section):
        def wrapped(sender=None):
            # Read the login information for the first toon
            username, password = self.config.get_account(section)
            # Launch the game
            launcher = tooner.ToontownLauncher(self._toontown)
            launcher.play(username=username, password=password)
        return wrapped

    def _launch_all(self, sender):
        for account in self.accounts:
            self._launch(account)()

    @update_menu
    def _add_account(self, sender):
        window = preferences.AddAccount(self)
        response = window.get_input()
        if response:
            self.config.add_account(*response)
            item = rumps.MenuItem(
                response[0],
                callback=self._launch(response[0]),
            )
            self.menu.insert_before('SeparatorMenuItem_2', item)

    @update_menu
    def _remove_account(self, sender):
        window = preferences.RemoveAccount(self)
        response = window.get_input()
        if response:
            self.config.remove_account(*response)
            self.menu.pop(response[0])

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
    def accounts(self):
        return self.config.accounts


if __name__ == '__main__':
    rumps.debug_mode(True)
    Application("MultiTooner").run()
