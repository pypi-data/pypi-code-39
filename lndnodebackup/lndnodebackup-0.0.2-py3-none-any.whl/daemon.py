import os
import time
import logging
import signal # Signal Handling Stuff
import sys # System Stuff
from subprocess import call

def addsignalhandlers():
    logging.debug("Register signal handlers")
    # Add handlers
    from nodebackup.stophandler import handler_stop_signals
    signal.signal(signal.SIGTERM, handler_stop_signals) # 15
    signal.signal(signal.SIGHUP, handler_stop_signals) # Signal 1 (TODO: reload configs?)
    signal.signal(signal.SIGINT, handler_stop_signals) # Signal 2
    signal.signal(signal.SIGQUIT, handler_stop_signals)

def stopdaemon():
    print("Attempting to stop backup service")
    logging.info("Stopping daemon from commandline")
    from nodebackup.configutils import canAccessForReading, readconfig
    configuration = readconfig()
    if not 'pidfile' in configuration:
        pidfile = "/var/run/nodebackup.pid"
    else:
        pidfile = configuration["pidfile"]
    if canAccessForReading(pidfile):
        print("Stopping Service...")
        file = open(pidfile, "r") 
        pidnumber = file.read() 
        logging.debug("Killing off PID ID %s" % pidnumber)        
        call(["kill", pidnumber])
        print("Stopped")
        os._exit(0)
    else:
        print("Unable to stop service. Does the PID exist?")
        logging.error("Unable to kill off process as PID file does not exist for reading!")
        os._exit(1)


def startdaemon():
    from nodebackup.configutils import canAccessForWriting, readconfig
    from nodebackup.inotifyutils import watchFile
    logging.info('Started daemon') 
    addsignalhandlers()
    # Read from config
    configuration = readconfig()
    # Check pidfile (used for starting up the daemon. To go with Daemon)
    if not 'pidfile' in configuration:
        pidfile = "/var/run/nodebackup.pid"
    else:
        pidfile = configuration['pidfile']

    # Check backup file (Used for watching. To go with Daemon)
    if not 'backupfile' in configuration:
        # Default path
        backupfile = "/media/important/important/lnd/data/chain/bitcoin/mainnet/channel.backup"
    else:
        # Define the location of the backup in config
        backupfile = configuration['backupfile']
        
    # Forking stuff To background
    try:
        pid = os.fork()
        if pid > 0:
            logging.info("Running process as PID: %d" % pid)
            print('Running process as PID %d' % pid)
            # Check if writing is possible to the specified pid file
            if canAccessForWriting(pidfile):
                print('Using %s as pidfile' % pidfile)
                logging.info('Using %s as pidfile' % pidfile)
                with open(pidfile, 'w') as pidfilepointer:
                    pidfilepointer.write("%d" % pid)
            else:
                print('Cannot write to %s' % pidfile)
                logging.warn('Cannot write to %s' % pidfile)
            os._exit(0)
    except:
        exception = sys.exc_info()[0]
        logging.fatal("Unable to fork")
        print("Unable to fork (%s)" % exception)
        os._exit(1)

    # Start daemon work
    watchFile(backupfile)
    
    # End Daemon function

if __name__ == "__main__":
    print("This file is not meant to be run directly")