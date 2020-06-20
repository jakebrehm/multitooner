# -*- coding: utf-8 -*-

'''
multitooner.app module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main module for the MultiTooner application. Includes all menu bar
functionality.
'''

import configparser
import os
import pathlib

import rumps
import tooner

import config
import login
import preferences


def update_menu(function):
    '''Decorator that updates the menu after executing the method.'''
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        self.update_menu_items()
    return wrapper


class Application(rumps.App):
    '''Main class of the MultiTooner application.

    Please see the documentation for rumps.App for information on 
    parameters.

    Attributes:
        accounts:
            Returns a list of account names.
    '''

    def __init__(self, *args, **kwargs):
        '''Please see help(Applicatioon) for more info.'''

        # Initialize the application and set the icon
        super().__init__(*args, **kwargs)
        self._set_icon('icon-desaturated.icns')

        # Get the application support directory of the toontown engine
        self._toontown = rumps.application_support("Toontown Rewritten")

        # Initialize the configuration file and menu
        self.config = config.Configuration(self, 'config.ini')
        self.initialize_menu()

        # Initialize the invasion tracker and start if necessary
        self._interval = 15
        self._invasion_timer = rumps.Timer(self._get_invasions, self._interval)
        self._tracker = tooner.InvasionTracker()
        self._invasions = {}
        if self._track_option.state:
            self._invasion_timer.start()

    def __getitem__(self, item):
        '''Returns path to an item in the Application Support folder.
        
        Returns the full path to the specified item in the  
        MultiTooner application's Application Support folder.

        Args:
            item (str):
                The name of the file.
        '''

        return os.path.join(rumps.application_support("MultiTooner"), item)

    @property
    def accounts(self):
        '''Returns a list of configured account names.'''

        return self.config.accounts

    @update_menu
    def initialize_menu(self):
        '''Initializes/creates the menu items.

        Creates each menu item, including the dynamically created 
        account items. These account items are created by reading the
        configuration file and making one item for each section.
        '''

        # Add a "Launch All" item
        self._launch_all_option = rumps.MenuItem(
            'Launch All',
            callback=self.launch_all,
        )
        self.menu.add(self._launch_all_option)
        self.menu.add(None)

        # Create a menu item for each account in the config file
        for account in self.accounts:
            item = rumps.MenuItem(account, callback=self.launch(account))
            self.menu.add(item)
        self.menu.add(None)

        # Make a nested preferences menu
        preferences = rumps.MenuItem('Preferences')
        preferences.add(rumps.MenuItem(
            'Add Account',
            callback=self.add_account,
        ))
        self._remove_account_option = rumps.MenuItem(
            'Remove Account',
            callback=self.remove_account,
        )
        preferences.add(self._remove_account_option)
        preferences.add(None)
        self._track_option = rumps.MenuItem(
            'Invasion Notifications',
            callback=self.toggle_invasion_notifications,
        )
        preferences.add(self._track_option)
        preferences.add(None)
        self._login_option = rumps.MenuItem(
            'Run at Login',
            callback=self.run_at_login,
        )
        preferences.add(self._login_option)
        self.menu.add(preferences)
        self.menu.add(None)

    def update_menu_items(self):
        '''Updates and refreshes menu items.

        Certain menu items are meant to be disabled under certain 
        conditions. Other items need their checked/unchecked state to 
        be programmatically determined.
        '''

        # Determine if the "Track Invasions" preference should be checked
        self._update_track_option()
        
        # Determine if the "Run at Login" preference should be checked
        self._update_login_option()

        # Disable certain items if there are no accounts configured
        self._disable_if_no_accounts(
            self._launch_all_option,
            self.launch_all,
        )
        self._disable_if_no_accounts(
            self._remove_account_option,
            self.remove_account,
        )

    def toggle_invasion_notifications(self, sender):
        '''

        '''

        original_state = self._track_option.state

        if sender.state == -1 or original_state != sender.state:
            return
        
        sender.state = int(not sender.state)
        self.config.set_setting('invasions', sender.state)

        if sender.state:
            self._invasion_timer.start()
        else:
            self._invasion_timer.stop()

    def run_at_login(self, sender):
        '''Toggles whether or not the application will run at login.

        If the "Run at Login" menu item is currently unchecked, check 
        it and modify the user's system preferences to make the 
        application run at login. If it is currently checked, uncheck 
        it and stop the application from running at login.

        Args:
            sender (rumps.MenuItem):
                Automatically sent when a menu item is invoked, and 
                is essentially a reference to the invoked menu item.
        '''

        # Note the original state of the "Run at Login" menu item
        original_state = self._login_option.state
        # Make sure that the "Run at Login" menu item is properly updated
        self._update_login_option()
        # Exit if the "Run at Login" menu item wasn't updated properly
        if sender.state == -1 or original_state != sender.state:
            return
        # Check the menu item if unchecked and vice versa
        sender.state = int(not sender.state)
        # Toggle running at login appropriately
        if sender.state:
            login.enable_run_at_login()
        else:
            login.disable_run_at_login()

    @update_menu
    def add_account(self, sender):
        '''Adds an account.

        Launches a window where information can be specified about the 
        account the user wants to add. If the user's input is valid, 
        the account is added to both the configuration file and the end 
        of the accounts section of the menu.

        Args:
            sender (rumps.MenuItem):
                Automatically sent when a menu item is invoked, and 
                is essentially a reference to the invoked menu item.
        '''

        # Launch the Add Account window and get the user's input
        window = preferences.AddAccount(self)
        response = window.get_input()
        # If the input is valid, add the account
        if response:
            self.config.add_account(*response)
            item = rumps.MenuItem(
                response[0],
                callback=self.launch(response[0]),
            )
            self.menu.insert_before('SeparatorMenuItem_2', item)

    @update_menu
    def remove_account(self, sender):
        '''Removes an account.

        Launches a window where the user can specify which currently 
        configured account to remove. If the user's input is valid, 
        the account is removed from both the menu and the configuration 
        file.

        Args:
            sender (rumps.MenuItem):
                Automatically sent when a menu item is invoked, and 
                is essentially a reference to the invoked menu item.
        '''

        # Launch the Remove Account window and get the user's input
        window = preferences.RemoveAccount(self)
        response = window.get_input()
        # If the input is valid, remove the account
        if response:
            self.config.remove_account(*response)
            self.menu.pop(response[0])

    def launch(self, name):
        '''Launches the specified account.

        Dynamically creates a callback function for the specified 
        account.

        Args:
            name (str):
                The name of the configured account to launch. Should 
                match the name of a valid section of the configuration 
                file.
        '''

        def wrapped(sender=None):
            # Read the login information for the first toon
            username, password = self.config.get_account(name)
            # Launch the game
            launcher = tooner.ToontownLauncher(self._toontown)
            launcher.play(username=username, password=password)
        return wrapped

    def launch_all(self, sender):
        '''Launches all configured accounts.

        Args:
            sender (rumps.MenuItem):
                Automatically sent when a menu item is invoked, and 
                is essentially a reference to the invoked menu item.
        '''

        for account in self.accounts:
            self.launch(account)()

    def _disable_if_no_accounts(self, item, callback):
        '''Disables the specified item if no accounts are configured.

        If no accounts are currently configured, this method will set 
        the specified menu item's callback to None, essentially 
        disabling it. Otherwise, it will set it back to its 
        normal callback method.

        Args:
            item (rumps.MenuItem object):
                The menu item to enable or disable.
            callback (method):
                The menu item's normal callback method.
        '''
        
        item.set_callback(callback if len(self.accounts) else None)

    def _update_option(self, menu_item, value):
        '''

        '''

        if menu_item.state == -1:
            return
        menu_item.state = int(value)
        if menu_item.state == -1:
            menu_item.set_callback(None)

    def _update_track_option(self):
        '''

        '''

        menu_item = self._track_option
        value = self.config.get_setting('invasions')
        self._update_option(menu_item, value)

    def _update_login_option(self):
        '''Toggles the "Run at Login" preference appropriately.

        Looks at the user's system preferences to see if the 
        application is currently configured to run at login. If it is, 
        it checks the "Run at Login" menu item. If it isn't, it will 
        uncheck it.
        '''

        menu_item = self._login_option
        value = login.run_at_login_is_enabled()
        self._update_option(menu_item, value)

    def _get_resource(self, filename):
        '''

        '''

        try:
            # When frozen, the icon will be in the same directory
            path = os.path.join(pathlib.Path(__file__).parent, filename)
            # Attempt to open the file so that an error might be triggered
            with open(path) as _:
                pass
        except FileNotFoundError:
            # During development, use the icon in the data directory
            PROJECT_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent
            ASSETS_FOLDER = os.path.join(PROJECT_DIRECTORY, 'assets')
            path = os.path.join(ASSETS_FOLDER, filename)
        return path

    def _set_icon(self, filename):
        '''Sets the icon of the application.

        Sets the application's icon, which will appear in the menu 
        bar, to the specified icon file.
        
        Args:
            filename (str):
                The name of the icon file. The icon should either be a 
                .ico (Windows icon) file or a .icns (Mac icon, 
                recommended) file.
        '''
        
        self.icon = self._get_resource(filename)

    def _get_invasions(self, sender):
        '''Notifies the user of new invasions.

        Communicates with the Toontown Rewritten API to get information 
        about current invasions, then determines which invasions are 
        new. If there are new invasions, the user will be notified via 
        notification.

        Args:
            sender (rumps.MenuItem):
                Automatically sent when a menu item is invoked.
        '''

        #
        previous = self._invasions
        current = self._tracker.get_invasions()

        #
        difference = set(current.items()) - set(previous.items())
        #
        for invasion in difference:
            #
            district, cog = invasion
            rumps.notification(
                title='A cog invasion has begun!',
                subtitle=None,
                message=f'{cog}s have invaded {district}!',
            )
        
        self._invasions = current


if __name__ == '__main__':
    # Set debug mode and run the application
    rumps.debug_mode(True)
    Application("MultiTooner").run()
