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
import tweepy

# 3rd party libraries
from db2twitter.imagesize import ImageSize
from db2twitter.networks.mastodon import post2mastodon
from db2twitter.networks.twitter import post2twitter
from db2twitter.storestatus import store_status_id
from db2twitter.timetosend import TimeToSend
from db2twitter.wasposted import WasPosted

def sendmessages(cfgvalues, cliargs, tweets, session):
    '''Send messages to the social networks'''
    # iterate over all the messages
    for tweet in tweets:
        tts = TimeToSend(cfgvalues)
        # are date and time ok to send the tweet?
        if tts.sendthetweet:
            # was the tweet already sent?
            if tweets[tweet]['withimage']:
                # dry run mode
                if cliargs.dryrun:
                    if 'imagepath' in tweets[tweet]:
                        print('Should have been tweeted: {tweet} | image:{imagepath}'.format(tweet=tweets[tweet]['data'], imagepath=tweets[tweet]['imagepath']))
                    else:
                        print('Should have been tweeted: {tweet}'.format(tweet=tweets[tweet]['data']))
                    if 'mastodon' in cfgvalues and cfgvalues['mastodon']:
                        if 'imagepath' in tweets[tweet]:
                            print('Should have been tooted: {toot} | image:{imagepath}'.format(toot=tweets[tweet]['data'], imagepath=tweets[tweet]['imagepath']))
                        else:
                            print('Should have been tooted: {toot}'.format(toot=tweets[tweet]['data'], imagepath=tweets[tweet]['imagepath']))
                else:
                    statusid = post2twitter(cfgvalues, tweets[tweet])
                    if 'mastodon' in cfgvalues and cfgvalues['mastodon']:
                        post2mastodon(cfgvalues, tweets[tweet])
            else:
                # dry run mode
                if cliargs.dryrun:
                    print('Should have been tweeted: {tweet}'.format(tweet=tweets[tweet]['data']))
                    if 'mastodon' in cfgvalues and cfgvalues['mastodon']:
                        if 'imagepath' in tweets[tweet]:
                            print('Should have been tooted: {toot} | image:{imagepath}'.format(toot=tweets[tweet]['data'], imagepath=tweets[tweet]['imagepath']))
                        else:
                            print('Should have been tooted: {toot}'.format(toot=tweets[tweet]['data']))
                else:
                    statusid = post2twitter(cfgvalues, tweets[tweet])
                    if 'mastodon' in cfgvalues and cfgvalues['mastodon']:
                        post2mastodon(cfgvalues, tweets[tweet])
        # store the status id
        if 'redis' in cfgvalues and cfgvalues['redis']:
            if cliargs.dryrun:
                print('Should have stored twitter status id for db row {rowid}'.format(rowid=tweet))
            else:
                store_status_id(cfgvalues['redis'], tweet, statusid)
    # store the last sent tweet id
    if tweets:
        store_last_sent(session, tweet)

def store_last_sent(session, originid):
    '''store the last sent tweet id'''
    previous_sent = session.query(WasPosted).filter(WasPosted.lastcircled == True).first()
    if previous_sent:
        previous_sent.lastcircled = False
    # store the new last sent tweet id
    last_sent = session.query(WasPosted).filter(WasPosted.originid == originid).first()
    last_sent.lastcircled = True
    session.commit()
