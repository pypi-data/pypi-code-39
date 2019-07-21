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
import argparse

from . import settings
from .helios import Helios

VERSION = '1.0.0'

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='Helios ' + VERSION)
    parser.add_argument('path', metavar='PATH', type=str,
                        help='the path to the stream to monitor')
    args = parser.parse_args()

    sm = Helios(args.path)
    sm.run()
