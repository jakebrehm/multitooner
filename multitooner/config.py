# -*- coding: utf-8 -*-

'''
multitooner.config module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration module for the MultiTooner app. Manages the 
application's configuration file.
'''

import configparser
import os

import rumps


def save_config(function):
    '''Decorator that saves the configuration file after execution.'''
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        self.save()
    return wrapper


class Configuration(configparser.ConfigParser):
    '''Handles the application's configuration file.

    A subclass of configparser.ConfigParser, with only a few additional 
    properties and methods that simply aim to make adding accounts from 
    other modules easier.

    Args:
        application (multitooner.app.Application object):
            A reference to the main Application object.
        filename (str):
            The filename of the configuration file (not the full 
            filepath).

    Attributes:
        accounts:
            Returns a list of sections (which is essentially just a 
            list of account names).
    '''

    def __init__(self, application, filename):
        '''Please see help(Configuration) for more info.'''

        # Store parameters and initialize the class
        self._application = application
        self._filename = filename
        super().__init__(self)

        # Build the path to the configuration file
        self._config_path = self._application[self._filename]
        # Read the configuration file whether it exists or not
        self.read(self._config_path)

    def get_account(self, account):
        '''Get information about the specified account.
        
        Grabs the username and password of the user-specified account 
        from the configuration file.

        Args:
            account (str):
                The name of the account to grab information for as it 
                is listed in the configuration file.
        '''

        return self[account]['username'], self[account]['password']

    @save_config
    def add_account(self, name, username, password):
        '''Add an account to the configuration file.
        
        Creates a new section in the configuration file for an account 
        and populates it with its corresponding username and password.

        Args:
            name (str):
                The name that the user wishes to call the account by. 
                Will be used as the name of the new section in the 
                configuration file.
            username (str):
                The username of the new account.
            password (str):
                The password the corresponds to the given username.
        '''

        self.add_section(name)
        self.set(name, 'username', username)
        self.set(name, 'password', password)

    @save_config
    def remove_account(self, name):
        '''Removes an account from the configuration file.
        
        Removes the section in the configuration file that corresponds to 
        the account that the user would like to remove.

        Args:
            name (str):
                The name of the account/section of the configuration 
                file that the user wishes to remove.
        '''

        self.remove_section(name)

    def save(self):
        '''Saves the configuration file.'''

        with open(self._config_path, 'w') as config:
            self.write(config)

    @property
    def accounts(self):
        '''Returns a list of accounts/sections of the configuration.'''

        return self.sections()
