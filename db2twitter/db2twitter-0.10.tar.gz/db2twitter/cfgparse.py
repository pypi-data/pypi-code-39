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

# Get values of the configuration file
'''Get values of the configuration file'''

# standard libraries imports
import configparser
import os.path
import sys

# app libraries imports
from db2twitter.cfgparsers.mastodon import parsemastodon
from db2twitter.cfgparsers.twitter import parsetwitter
from db2twitter.cfgparsers.media import parsemedia
from db2twitter.cfgparsers.messages import parsemessages
from db2twitter.cfgparsers.redis import parseredis
from db2twitter.cfgparsers.timer import parsetimer

def parseconfig(pathtoconf):
    '''Parse the configuration'''
    dbrows = {}
    ids = {}
    sqlfilter = {}
    images = {}
    imagepath =''
    imageprefix =''
    fallbackimageprefix =''
    mastodonconf = {}
    timerconf = {}
    noimagecircling = False
    pathtoconf = pathtoconf
    twitterconf = {}
    upperfirstchar = False

    config = configparser.ConfigParser()
    try:
        with open(pathtoconf) as conffile:
            config.read_file(conffile)
            # parse twitter configuration
            twitterconf = parsetwitter(config)
            mastodonconf = parsemastodon(config)
            # parse mastodon configuration
            mastodonconf = parsemastodon(config)
            # parse configuration of the media
            mediaconf = parsemedia(config)
            # parse configuration of the messages
            messagesconf = parsemessages(config)
            # parse configuration of the timer section
            timerconf = parsetimer(config)
            # parse configuration of the redis section
            redisconf = parseredis(config)
            # database section
            if config.has_section('database'):
                dbconnector = config.get('database', 'dbconnector')
                dbhost = config.get('database', 'dbhost')
                database = config.get('database', 'database')
                dbuser = config.get('database', 'dbuser')
                dbpass = config.get('database', 'dbpass')
                dbtables = config.get('database', 'dbtables')
                # managing extraction of fields to parse
                alltables = dbtables.split(',')
                alltables = (i for i in alltables if i !='')
                for table in alltables:
                    if config.has_option('database', '{}_rows'.format(table)):
                        rows = config.get('database', '{}_rows'.format(table)).split(',')
                        rows = [i for i in rows if i != '']
                        dbrows[table] = rows
                    if config.has_option('database', '{}_id'.format(table)):
                        ids[table] = config.get('database', '{}_id'.format(table))
                    if config.has_option('database', '{}_sqlfilter'.format(table)):
                        sqlfilter[table] = config.get('database', '{}_sqlfilter'.format(table))
                    if config.has_option('database', '{}_image'.format(table)):
                        images[table] = config.getboolean('database', '{}_image'.format(table))
            if config.has_section('sqlite'):
                sqlitepath = config.get('sqlite', 'sqlitepath')
            if config.has_section('circle'):
                if 'no_image' in config['circle']:
                    noimagecircling = config.getboolean('circle', 'no_image')
    except (configparser.Error, IOError, OSError) as err:
        sys.exit(err)
    # parsed configuration values to return
    return {'twitter': twitterconf,
            'mastodon': mastodonconf,
            'messages': messagesconf,
            'redis': redisconf,
            'timer': timerconf,
            'dbconnector': dbconnector,
            'dbhost': dbhost,
            'database': database,
            'dbuser': dbuser,
            'dbpass': dbpass,
            'dbtables': dbtables,
            'rows': dbrows,
            'images': images,
            'media': mediaconf,
            'ids': ids,
            'sqlfilter': sqlfilter,
            'sqlitepath': sqlitepath,
            'circlenoimage': noimagecircling}
