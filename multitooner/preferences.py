import rumps


class AddAccount(rumps.Window):

    def __init__(self, application):

        self._application = application
        self._base_message = (
            'Enter your login information.\n\n'
            'This includes the arbitrary name of the account, the username, '
            'and the password each on separate lines.\n\n'
            'For your convenience, you can just replace the placeholder text. '
            'Otherwise, <Option+Return> will add a new line.'
        )

        super().__init__(ok='Add', cancel='Cancel', dimensions=(295, 55))
        self.title = 'Add Account'
        self.message = self._base_message
        self.default_text = 'name\nusername\npassword'
        self.icon = None

    def get_input(self):
        while True:
            response = self.run()
            if response.clicked:
                text = [t for t in response.text.split('\n') if t]
                if len(text) == 3:
                    break
                else:
                    self.message = f'Please try again. {self._base_message}'
                    continue
            else:
                return
        return text


class RemoveAccount(rumps.Window):

    def __init__(self, application):

        self._application = application
        self._base_message = 'Enter the exact name of the account to remove.'

        super().__init__(ok='Remove', cancel='Cancel', dimensions=(295, 24))
        self.title = 'Remove Account'
        self.message = self._base_message
        self.default_text = 'name'
        self.icon = None

    def get_input(self):
        while True:
            response = self.run()
            if response.clicked:
                text = [t for t in response.text.split('\n') if t]
                if len(text) == 1 and text[0] in self._application.accounts:
                    break
                else:
                    self.message = f'Please try again. {self._base_message}'
                    continue
            else:
                return
        return text
