# Dropbox Libraries (TODO: move this to its own area)
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

import os, logging, sys


def dropboxbackup(filename):
    from nodebackup.configutils import readconfig
    configuration = readconfig()
    if not 'nodename' in configuration:
        print("'nodename' is not defined in toml root")
        sys.exit(1)

    # TODO: put apikeys (and defined provider) stuff in its own section (maybe into readconfig.py)
    if not 'provider' in configuration:
        print("No provider = 'providername' defined in toml root")
        sys.exit(1)    
    if not 'apikeys' in configuration:
        print("No section called [apikeys] in configuration file, please define this")
        sys.exit(1)
    # get providername from config
    providername = configuration['provider']
    if configuration['apikeys'][providername] is None:
        print("No API key for " + providername + " is defined")
        sys.exit()        

    # Define dropbox connection
    logging.info('Dropbox connection initialized')
   
    # Start Dropbox upload
    dbx = dropbox.Dropbox(configuration['apikeys'][providername])
    logging.info('Dropbox backup started')
    filearray = os.path.split(filename)
    pathname = '/lncm/channel_backups/' + configuration['nodename'] + '/' + filearray[len(filearray) - 1]
    with open(filename, 'rb') as f:
        logging.info("Uploading " + filename + " to dropbox " + pathname)
# Actually do the upload now
        try:
            dbx.files_upload(f.read(), pathname, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                err.error.get_path().reason.is_insufficient_space()):
                logging.fatal("Not enough space on dropbox")
                sys.exit("Not enough space on dropbox")
            elif err.user_message_text:
                logging.warn("Dropbox system error: " + err.user_message_text)
            else:
                logging.warn("Generic system error: " + err)

if __name__ == "__main__":
    print("This file is not meant to be run directly")