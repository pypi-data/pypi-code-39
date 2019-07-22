###########################################################################
# Helios is Copyright (C) 2016-2018 Kyle Robbertze
# <paddatrapper@debian.org>
#
# Helios is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Helios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Helios.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
import configparser
import os

# Order of preference (highest takes priority)
# ./helios.ini
# $HOME/.helios.ini
# /etc/helios/helios.ini

locations = ['helios.ini',
             os.path.join(os.path.expanduser('~'), '.helios.ini'),
             os.path.join('/etc', 'helios', 'helios.ini'),]


config_file = None
for location in locations:
    if os.path.isfile(location):
        config_file = location
        break

if not config_file:
    raise FileNotFoundError('Config file not found')

settings = configparser.ConfigParser()
settings.read(config_file)
