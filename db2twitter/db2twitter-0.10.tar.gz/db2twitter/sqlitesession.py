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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Got data about the already sent tweets
'''Got data about the already sent tweets'''

# 3rs party libraries imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# app libraries imports
from db2twitter.wasposted import WasPosted

def sqlitesession(cfgvalues):
    '''Get a SQLite session'''
    # activate the sqlite db
    engine = create_engine('sqlite:///{}'.format(cfgvalues['sqlitepath']))
    tmpsession = sessionmaker(bind=engine)
    session = tmpsession()
    WasPosted.metadata.create_all(engine)
    return session
