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
import calendar
import datetime
import time
import re
import subprocess

from .settings import settings

from influxdb import InfluxDBClient
from shlex import quote

class Helios:
    url = settings['database']['host']
    port = settings.getint('database', 'port')
    user = settings.get('database', 'user', fallback='')
    password = settings.get('database', 'password', fallback='')
    db = settings['database']['database']

    def __init__(self, location):
        self.location = location
        self.db_client = InfluxDBClient(self.url,
                                        self.port,
                                        '','',
                                        self.db)

    def post_data(self, time_delta, loudness):
        now_time = datetime.datetime.utcnow()
        json_body = [
            {
                "measurement": "level",
                "tags": {
                    "stream": self.location
                },
                "time": now_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    'ebu_r128': loudness
                }
            }
        ]
        print(json_body)
        self.db_client.write_points(json_body)

    def process(self, line):
        line = line.rstrip()
        line = re.split(r' +', line)
        if 'Parsed' in line[0] and 'Summary:' not in line:
            str_time = line[4]
            if '.' in str_time or int(str_time) % 2 != 0:
                return
            time = int(str_time) / 2
            loudness = float(line[10])
            time_delta = datetime.timedelta(seconds=time)
            self.post_data(time_delta, loudness)

    def run(self):
        command = ['ffmpeg',
                   '-nostats',
                   '-i', quote(self.location),
                   '-filter_complex',
                   'ebur128=peak=true',
                   '-f', 'null', '-']
        self.start = datetime.datetime.now()
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        while not proc.poll():
            # For some reason ffmpeg writes to stderr
            out = proc.stderr.readline()
            self.process(out)
