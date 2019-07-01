# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2017 Carl Chenet <carl.chenet@ohmytux.com>
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

'''Post a tweet to Twitter'''

# standard libraires imports
import logging

# 3rd party libraries imports
import tweepy

def post2twitter(cfgoptions, tweet):
    '''Post to the Twitter network'''
    network = 'twitter'
    consumer_key = cfgoptions[network]['consumer_key']
    consumer_secret = cfgoptions[network]['consumer_secret']
    access_token = cfgoptions[network]['access_token']
    access_token_secret = cfgoptions[network]['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        if 'imagepath' in tweet and tweet['imagepath']:
            status = api.update_with_media(tweet['imagepath'],status=tweet['data'])
        else:
            status = api.update_status(status=tweet['data'])
    except tweepy.TweepError as err:
        logging.warning('Error occurred while updating status: {err}'.format(err=err))
        status = 0
    return status.id
    
