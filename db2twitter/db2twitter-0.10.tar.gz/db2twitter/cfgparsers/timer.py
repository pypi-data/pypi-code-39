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

# Get values of the configuration file for the timer section
'''Get values of the configuration file for the timer section'''

# standard libraries imports
import sys

def parsetimer(config):
    '''parse the configuration of the messages section'''
    # timer section
    timerconf = {}
    section = 'timer'
    ############################
    # timer option
    ############################
    possibleconfs = ['days', 'hours']
    for confkey in possibleconfs:
        if config.has_option(section, confkey):
            timerconf[confkey] = config.get(section, confkey)
    return timerconf
