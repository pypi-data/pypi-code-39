# -*- coding: utf-8 -*-
# Copyright © 2015-2017 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Main class
'''Main class'''

# standard libraries imports
import configparser
import os.path
import sys

# app libraries imports
from db2twitter.buildmessages import buildmessages
from db2twitter.cfgparse import parseconfig
from db2twitter.cliparse import CliParse
from db2twitter.dbparse import dbparse
from db2twitter.getnewmessages import getnewmessages
from db2twitter.sendmessages import sendmessages
from db2twitter.sqlitesession import sqlitesession

class Main:
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        self.main()

    def main(self):
        '''Main of the Main class'''
        # parse the command line
        cargs = CliParse()
        cliargs = cargs.args
        # read the configuration file
        cfgvalues = parseconfig(cliargs.pathtoconf)
        # get the connector to the database storing the already-sent tweets
        sqlite = sqlitesession(cfgvalues)
        # parse the database
        tweet_elements_from_origin_db = dbparse(cfgvalues, sqlite)
        # build the tweets
        tweets_from_origin_db = buildmessages(cfgvalues, tweet_elements_from_origin_db)
        # store all tweets from origin db
        newmessages = getnewmessages(sqlite, cliargs.populate, tweets_from_origin_db)
        # prepare the tweets
        if not cliargs.populate:
            # send the messages (if any)
            if newmessages:
                sendmessages(cfgvalues, cliargs, newmessages, sqlite)
        sys.exit(0)
