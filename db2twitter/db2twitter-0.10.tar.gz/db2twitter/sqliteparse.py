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

# GetDbLastTweets class
'''GetDbLastTweets class'''

# standard libraries imports
import sys

# 3rd party libraries imports
from sqlalchemy import desc

# app libraries imports
from db2twitter.wasposted import WasPosted

def sqliteparse(session):
    '''get previously tweets in sqlite'''
    tweets = {}
    all_tweets_from_sqlite = session.query(WasPosted).all()
    for tweet_from_sqlite in all_tweets_from_sqlite:
        if not tweet_from_sqlite.tweetimage:
            withimage = False
        else:
            withimage = True
        # build the same dict as in dbparse
        tweets[tweet_from_sqlite.originid] = {'withimage': withimage, 'imagepath': tweet_from_sqlite.tweetimage, 'data': tweet_from_sqlite.tweet}
    return tweets
