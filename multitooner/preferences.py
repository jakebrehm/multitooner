# -*- coding: utf-8 -*-

'''
multitooner.preferences module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The preferences module for the MultiTooner application. Contains 
classes for the application's Preference windows.
'''

import rumps


class AddAccount(rumps.Window):
    '''A window that allows the user to add an account.

    A very basic wrapper around rumps.Window with preset titles, text, 
    etc. It includes one supplementary method that handles looping of 
    the rumps.Window.run() method if incorrect input is received, as 
    well as parsing of valid input.

    Upon valid input, the parsed input will be returned.

    Args:
        application (multitooner.app.Application object):
            A reference to the main Application object.
    '''

    def __init__(self, application):
        '''Please see help(AddAccount) for more info.'''

        # Store parameters and initalize the base message of the window
        self._application = application
        self._base_message = (
            'Enter your login information.\n\n'
            'This includes the arbitrary name of the account, the username, '
            'and the password each on separate lines.\n\n'
            'For your convenience, you can just replace the placeholder text. '
            'Otherwise, <Option+Return> will add a new line.'
        )

        # Initialize and set up the class
        super().__init__(ok='Add', cancel='Cancel', dimensions=(295, 55))
        self.title = 'Add Account'
        self.message = self._base_message
        self.default_text = 'name\nusername\npassword'
        self.icon = None

    def get_input(self):
        '''Run the window until valid input is received.
        
        Continuously run the window until the user either cancels or 
        enters valid input. Validity is determined by parsing the input 
        and verifying that it matches the expected pattern.
        '''

        # Loop continuously until cancelled or valid input is received
        while True:
            # Display the window and wait for the user's response
            response = self.run()
            if response.clicked:
                # If the user presses "Add", parse the input
                text = [t for t in response.text.split('\n') if t]
                if text[0] == 'DEFAULT':
                    # The name of the account must not be DEFAULT
                    self.message = f'Invalid account name. Please try again.'
                    continue
                elif self._is_valid(text):
                    # If the input is valid, break the loop
                    break
                else:
                    # Otherwise, edit the message and run the window again
                    self.message = f'Please try again. {self._base_message}'
                    continue
            else:
                # Exit if the user cancels
                return
        # Return the user's valid input
        return text
    
    def _is_valid(self, text):
        '''Checks the validity of the user's input.
        
        Args:
            text (str):
                Input/text to check the validity of.
        '''

        return all([
            len(text) == 3,
            text[0] not in self._application.accounts
        ])


class RemoveAccount(rumps.Window):
    '''A window that allows the user to remove an account.

    A very basic wrapper around rumps.Window with preset titles, text, 
    etc. It includes one supplementary method that handles looping of 
    the rumps.Window.run() method if incorrect input is received, as 
    well as parsing of valid input.

    Upon valid input, the parsed input will be returned.

    Args:
        application (multitooner.app.Application object):
            A reference to the main Application object.
    '''

    def __init__(self, application):
        '''Please see help(RemoveAccount) for more info.'''

        # Store parameters and initalize the base message of the window
        self._application = application
        # self._base_message = 'Enter the exact name of the account.'
        self._base_message = "Enter the account's exact name."

        # Initialize and set up the class
        super().__init__(ok='Remove', cancel='Cancel', dimensions=(295, 24))
        self.title = 'Remove Account'
        self.message = self._base_message
        self.default_text = 'name'
        self.icon = None

    def get_input(self):
        '''Run the window until valid input is received.
        
        Continuously run the window until the user either cancels or 
        enters valid input. Validity is determined by parsing the input 
        and verifying that it matches the expected pattern.
        '''

        # Loop continuously until cancelled or valid input is received
        while True:
            # Display the window and wait for the user's response
            response = self.run()
            if response.clicked:
                # If the user presses "Remove", parse the input
                text = [t for t in response.text.split('\n') if t]
                if text[0] == 'DEFAULT':
                    # The name of the account must not be DEFAULT
                    self.message = f'Invalid account name. Please try again.'
                    continue
                elif self._is_valid(text):
                    # If the input is valid, break the loop
                    break
                else:
                    # Otherwise, edit the message and run the window again
                    self.message = f'Please try again. {self._base_message}'
                    continue
            else:
                # Exit if the user cancels
                return
        # Return the user's valid input
        return text
    
    def _is_valid(self, text):
        '''Checks the validity of the user's input.
        
        Args:
            text (str):
                Input/text to check the validity of.
        '''

        return all([
            len(text) == 1,
            text[0] in self._application.accounts,
        ])
