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

# DbParse class
'''DbParse class'''

# standard libraries imports
import sys

# 3rd party libraries imports
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.inspection

# app libraries imports
from db2twitter.wasposted import WasPosted

def dbparse(cfgvalues, sqlitesession):
    '''Parse the origin database and get current data'''
    sqlitesession = sqlitesession
    mainid = ''
    firstrun = True
    # Create and engine and get the metadata
    Base = declarative_base()
    engine = create_engine('{}://{}:{}@{}/{}'.format(cfgvalues['dbconnector'],
        cfgvalues['dbuser'],
        cfgvalues['dbpass'],
        cfgvalues['dbhost'], 
        cfgvalues['database']))
    meta = MetaData()
    meta.reflect(bind=engine)
    tableobjects = []
    tableschemas = {}
    # load schemas of tables
    for table in cfgvalues['rows']:
        tableschemas[table] = Table(table, meta, autoload=True, autoload_with=engine)
    #Create a session to use the tables    
    session = create_session(bind=engine)
    # find how many new tweets to send
    sqliteobj = sqlitesession.query(WasPosted).all()
    dbtables = [i for i in cfgvalues['dbtables'].split(',') if i !='']
    tweets = {}
    allfields = []
    firstrun = True
    for table in cfgvalues['rows']:
        if cfgvalues['sqlfilter']:
            filterrequest = '{sqlfilter}'.format(sqlfilter=cfgvalues['sqlfilter'][table])
            tableobj = session.query(tableschemas[table]).filter(text(filterrequest))
        else:
            tableobj = session.query(tableschemas[table]).all()
        # ignore the None query result
        if tableobj:
            for tweetdb in tableobj:
                if table in cfgvalues['images']:
                    # split the different fields we need, last field is the image path
                    if not cfgvalues['ids']:
                        #tweets.append({'withimage': True, 'originid': getattr(tweetdb, 'id'), 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]})
                        tweets[getattr(tweetdb, 'id')] = {'withimage': True, 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]}
                    else:
                        tableid = '{tableid}'.format(tableid=cfgvalues['ids'][table])
                        #tweets.append({'withimage': True, 'originid': getattr(tweetdb, tableid), 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]})
                        tweets[getattr(tweetdb, tableid)] = {'withimage': True, 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]}
                else:
                    # split the different fields we need
                    if not cfgvalues['ids']:
                        #tweets.append({'withimage': False, 'originid': getattr(tweetdb, 'id'), 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]})
                        tweets[getattr(tweetdb, 'id')] = {'withimage': False, 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]}
                    else:
                        tableid = '{tableid}'.format(tableid=cfgvalues['ids'][table])
                        #tweets.append({'withimage': False, 'originid': getattr(tweetdb, tableid), 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]})
                        tweets[getattr(tweetdb, tableid)] = {'withimage': False, 'data': [getattr(tweetdb, i) for i in cfgvalues['rows'][table]]}
    # lets quit now if nothing new to tweet
    if not tweets:
        sys.exit(0)
    return tweets
