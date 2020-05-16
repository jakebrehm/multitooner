import rumps


class AddAccount(rumps.Window):

    def __init__(self):
        super().__init__(ok='Add', cancel='Cancel', dimensions=(295, 55))
        self.title = 'Add Account'
        self.message = (
            'Please enter your login information.\n\n'
            'This includes the arbitrary name of the account, the username, '
            'and the password each on separate lines.\n\n'
            'For your convenience, you can just replace the placeholder text. '
            'Otherwise, <Option+Return> will add a new line.'
        )
        self.default_text = 'name\nusername\npassword'
        self.icon = None


class RemoveAccount(rumps.Window):

    def __init__(self):
        super().__init__(ok='Remove', cancel='Cancel', dimensions=(295, 24))
        self.title = 'Remove Account'
        self.message = 'Enter the exact name of the account you wish to remove.'
        self.default_text = 'name'
        self.icon = None
    