# -*- coding: utf-8 -*-

'''
multitooner.main module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main module for the MultiTooner application. Combines all modules.
'''

import rumps

import app


class MultiTooner:

    def start(self, debug=False):
        '''Starts the application.
        
        Args:
            debug (bool):
                Whether or not to run in debug mode. Defaults to False.
        '''
        
        app.MenuBar(name="MultiTooner", quit_button="Quit").start(debug=debug)


if __name__ == '__main__':
    MultiTooner().start(debug=True)
