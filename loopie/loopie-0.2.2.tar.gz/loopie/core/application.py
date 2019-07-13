'''
Created on Sunday 07/07/2019

@author: yaztown
'''

from loopie.logging import get_logger
logger = get_logger()

from loopie.core.base_threads.default_routines import register_exit_signal_handler
from loopie.core.base_threads.base_exceptions import ThreadExitException

from time import sleep


class Application(object):
    '''
    This is the main application class that you need to subclass and override the start() method
    '''


    def __init__(self, mainloop):
        '''
        mainloop is an instance of the subclassed mainloop
        '''
#         settings = load_settings_from_file('settings/hgc_settings_minimal.json')
        self.main_loop = mainloop   #MainLoop(setup_object=settings, name='main_loop', loop_sleep_time=1)
        
    def start(self):
        logger.debug('Starting main_loop')
        register_exit_signal_handler()
        self.main_loop.start()
        try:
            # Keep the main thread running, otherwise signals are ignored.
            while True:
    #             main_loop.get_status()
                sleep(0.5)
     
        except ThreadExitException:
            # Terminate the running threads.
            # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
            self.main_loop.stop()
            # Wait for the threads to close...
            self.main_loop.join()
        logger.debug('Exiting...')
    
# if __name__ == '__main__':
#     main()
