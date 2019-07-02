# File notify libraries (pip3 install inotify)
import inotify.adapters    
# System
import logging 
import time

# Internal
from nodebackup.cloudutils import dropboxbackup    
from nodebackup.configutils import canAccessForWriting, pathExists

def watchFile(fileparam):    
    if pathExists(fileparam):
        i = inotify.adapters.Inotify()
        i.add_watch(fileparam)
        logging.info("Watching file " + fileparam + " for changes")
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            logging.debug("File changed with flag: " + str(type_names))
            logged_debug_watch = "Path: %s Filename %s" % (path, filename)
            logging.debug(logged_debug_watch)
            if type_names == ['IN_MODIFY'] or type_names == ['IN_DELETE_SELF']:
                logging.debug("Dropbox Upload")
                logging.info('File ' + fileparam + ' Changed.. uploading to defined cloud services')
                dropboxbackup(filename=fileparam)
                if type_names == ['IN_DELETE_SELF']:
                    # Call self
                    watchFile(fileparam)
    else:
        logging.warn("File doesn't exist.. waiting for 10 minutes before checking again")
        time.sleep(600)

if __name__ == "__main__":
    print("This file is not meant to be run directly")
