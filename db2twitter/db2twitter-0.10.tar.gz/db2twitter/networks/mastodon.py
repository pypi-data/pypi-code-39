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

# Post to the Mastodon network
'''Post to the Mastodon network'''

# 3rd party libraries imports
from mastodon import Mastodon

def post2mastodon(cfgoptions, toot):
    '''Post to the Mastodon network'''
    network = 'mastodon'
    mastodon = Mastodon(
        client_id=cfgoptions[network]['client_credentials'],
        access_token=cfgoptions[network]['user_credentials'],
        api_base_url=cfgoptions[network]['instance_url']
    )
    # if the user users image_path
    if 'imagepath' in toot and toot['imagepath']:
        mediaid = mastodon.media_post(toot['imagepath'])
        mastodon.status_post(toot['data'], media_ids=[mediaid], visibility=cfgoptions[network]['visibility'])
    else:
        mastodon.status_post(toot['data'], visibility=cfgoptions[network]['visibility'])
