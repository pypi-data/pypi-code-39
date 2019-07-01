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

# Get values of the configuration file for the messages
'''Get values of the configuration file for the messages'''

# standard libraries imports
import sys

def parsemedia(config):
   # messages section
    mediaconf = {}
    section = 'media'
    ############################
    # image_path option
    ############################
    confkey = 'image_path'
    if config.has_option(section, confkey):
        confkey = '{optionname}'.format(optionname=confkey)
        mediaconf[confkey] = config.get(section, confkey)
    else:
        sys.exit('You should define a parameter "{confoption}" in the [{section}] section'.format(confoption=confoption, section=section))
    possibleoptions = ['image_prefix', 'fallback_image_prefix']
    for confkey in possibleoptions:
        if config.has_option(section, confkey):
            confkey = '{optionname}'.format(optionname=confkey)
            mediaconf[confkey] = config.get(section, confkey)
    return mediaconf
