# -*- coding: utf-8 -*-

"""downgram.downgram: Entrypoint to main()."""

import sys, getopt, configparser

settings = configparser.ConfigParser()
settings.read('settings.py')

__version__="0.2.1"

#config = configparser.ConfigParser()
#config.read(settings['Global']['path'] +'downgram.ini')

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hc:r")
    except getopt.GetoptError:
        print (settings['Help']['help'])
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print (settings['Help']['help'])
            sys.exit()
        elif opt == "-c":
            settings['Global']['path'] = arg
            sys.exit()
        elif opt == "-r":
            pass

#if __name__ == '__main__':
#    main(sys.argv[1:])
