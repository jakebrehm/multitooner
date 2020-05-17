import configparser
import os

import rumps


class Configuration(configparser.ConfigParser):

    def __init__(self, application, filename):

        super().__init__(self)

        self._application = application
        self._filename = filename

        self._config_path = self._application[self._filename]

        self.read(self._config_path)

    def get_account(self, account):
        return self[account]['username'], self[account]['password']

    def add_account(self, name, username, password):
        self.add_section(name)
        self.set(name, 'username', username)
        self.set(name, 'password', password)
        self.save()

    def remove_account(self, name):
        self.remove_section(name)
        self.save()

    def save(self):
        with open(self._config_path, 'w') as config:
            self.write(config)

    @property
    def accounts(self):
        return self.sections()
