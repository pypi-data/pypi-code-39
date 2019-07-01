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

# Send the tweet
'''Send the tweet'''

# 3rd party libraries imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# 3rd party libraries
from db2twitter.wasposted import WasPosted

def getnewmessages(session, populate, tweets):
    '''get the new messages to be sent'''
    newmessages = {}
    # find the lastcircled tweet id
    lastcircled = session.query(WasPosted).filter(WasPosted.lastcircled == True).first()
    if lastcircled:
        lastcircledid = lastcircled.originid
    # find the last max id
    pviousmaxid = session.query(func.max(WasPosted.originid).label('previousmaxid')).first()
    if pviousmaxid:
        previousmaxid = pviousmaxid.previousmaxid
    # delete everything from the sqlite
    session.query(WasPosted).delete()
    # update with the current content of the origin db
    session.commit()
    # store all tweets and return new ones
    for tweetid in tweets:
        tweetdata = tweets[tweetid]['data']
        if 'imagepath' in tweets[tweetid]:
            tweetimage = tweets[tweetid]['imagepath']
        else:
            tweetimage = ''
        # indicate if this one is the last sent message 
        if lastcircled and lastcircled.originid == tweetid:
            newtweet = WasPosted(originid=tweetid, lastcircled=True)
        else:
            newtweet = WasPosted(originid=tweetid)
        session.add(newtweet)
        if not populate and tweetid > previousmaxid:
            newmessages[tweetid] = tweets[tweetid]
    # save messages in sqlite database
    session.commit()
    # manage the case if no new message, lets circle
    if not populate and not newmessages:
        indice = 0
        # if not circled yet
        if not lastcircled:
            lastcircledid = previousmaxid + 1
        # manage case when back to the start of ids
        if lastcircledid == 0 or lastcircledid == 1:
            lastcircledid = previousmaxid
        # decrease of one until finding next available id
        indice = lastcircledid - 1
        found = False
        while not found:
            # manage case when back to the start of ids
            if indice == 0 or indice == 1:
                newmaxid = max(tweets.keys())
                indice = newmaxid
            # check if the id exists
            if indice in tweets:
                newmessages[indice] = tweets[indice]
                found = True
            indice -= 1
    return newmessages
