# -*- coding: utf-8 -*-

'''
multitooner.authenticate module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The authentication module for the MultiTooner application.

Contains code for the window that appears to prompt a user for their
ToonGuard validation code.
'''

import rumps


class AuthenticationWindow(rumps.Window):
    '''A window that allows the input their ToonGuard authentication code.

    A very basic wrapper around rumps.Window with preset titles, text, 
    etc. It includes one supplementary method that handles looping of 
    the rumps.Window.run() method if incorrect input is received, as 
    well as parsing of valid input.

    Upon valid input, the parsed input will be returned.

    Args:
        application (multitooner.app.Application object):
            A reference to the main Application object.
    '''

    def __init__(self, application, name):
        '''Please see help(Authenticate) for more info.'''

        # Store parameters and initalize the base message of the window
        self._application = application
        self._base_message = (
            f'Enter your ToonGuard validation code for {name}.'
        )

        # Initialize and set up the class
        super().__init__(ok='Submit', cancel='Cancel', dimensions=(295, 55))
        self.title = 'Enter ToonGuard Code'
        self.message = self._base_message
        self.default_text = ''
        self.icon = None

    def get_input(self):
        '''Run the window until valid input is received.
        
        Continuously run the window until the user either cancels or 
        enters valid input. Validity is determined by parsing the input 
        and verifying that it matches the expected pattern.
        '''

        # Define a failure message
        failure_message = 'Please try again. Your input should only be numbers.'
        
        # Loop continuously until cancelled or valid input is received
        while True:
            # Display the window and wait for the user's response
            response = self.run()
            if response.clicked:
                # If the user presses "Submit", check the validity of the input
                if self.is_valid(response.text):
                    # If the input is valid, break the loop
                    break
                else:
                    # Otherwise, edit the message and run the window again
                    self.message = f'{failure_message} {self._base_message}'
                    continue
            else:
                # Exit if the user cancels
                return
        # Return the user's valid input
        return str(response.text)
    
    def is_valid(self, text):
        '''Checks the validity of the user's input.
        
        Args:
            text (str):
                Input/text to check the validity of.
        '''

        return all([
            len(text) == 6,
        ])
