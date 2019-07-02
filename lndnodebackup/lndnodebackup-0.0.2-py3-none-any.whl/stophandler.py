import logging, os, sys
from pathlib import Path
import signal

def handler_stop_signals(signum, frame):
    logging.debug("Signal %d received" % signum)

    if signum == signal.SIGHUP:
        logging.info("Caught SIGHUP (%d) signal" % signum)
        logging.debug("Dont do anything on SIGHUP for now")
    else:
        if signum == signal.SIGTERM:
            logging.info("Caught SIGTERM (%d) signal" % signum)
        if signum == signal.SIGQUIT:
            logging.info("Caught SIGQUIT (%d) signal" % signum) 
        logging.info("Caught Terminate signal - exiting")
        logging.debug("Really.. this is just a catch-all")
        sys.exit(0)
    
if __name__ == "__main__":
    print("This file is not meant to be run directly")
