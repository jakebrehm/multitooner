import rumps


class AddAccount(rumps.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(ok='Add', cancel='Cancel', dimensions=(290, 55))
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


if __name__ == '__main__':

    window = AddAccount()
    while True:
        response = window.run()
        if response.clicked:
            text = [t for t in response.text.split('\n') if t]
            if len(text) == 3:
                break
            else:
                window = AddAccount()
                window.message = (
                    'Please try again.\n\n'
                    'Replace the placeholder text with your login information.'
                )
                continue
        else:
            break
    
    print(text)