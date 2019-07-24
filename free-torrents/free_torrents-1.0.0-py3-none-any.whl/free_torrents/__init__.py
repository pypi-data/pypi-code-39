"""
Copyright (C) 2019 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
from pathlib import Path
import re
import requests
import sys


RE_TORRENT = re.compile(r'<a(.*?)href="(.*?)\.torrent"')
GROUPS = {
    'debian': {
        'index': 'https://cdimage.debian.org/debian-cd/current/amd64/bt-cd/',
    },
    'ubuntu': {
        'index': 'https://ubuntu.com/download/alternative-downloads',
    },
    'fedora': {
        'index': 'https://torrents.fedoraproject.org/',
        # TODO: Don't hardcode latest fedora release
        'has': '-30.torrent'
    },
    'tails': {
        'index': 'https://tails.boum.org/torrents/files/'
    },
    #  'qubes': {},
}


class FreeTorrents:
    def __init__(self, watch: Path):
        self.session = requests.Session()
        self.watch = watch

    def index_scraper(self, url: str, has=None):
        r = self.session.get(url)
        r.raise_for_status()
        matches = set(RE_TORRENT.findall(r.text))
        for _,  match in matches:
            torrent = f'{match}.torrent'
            if not torrent.startswith(('https://', 'http://')):
                torrent = f'{url}/{torrent}'
            if has is None or has in torrent:
                yield torrent

    def download(self, url: str):
        fname = url.rsplit('/')[-1]
        path = self.watch / fname
        if path.is_file():
            print(f'Skipping {fname}...')
            return
        with self.session.get(url, stream=True) as r:
            r.raise_for_status()
            with path.open('wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f'Downloaded {fname}!')

    def run(self, enabled):
        for group, conf in GROUPS.items():
            if group not in enabled:
                continue
            torrents = self.index_scraper(
                conf['index'], conf.get('has')
            )
            print(f'-- {group} --')
            for torrent in torrents:
                # print(torrent)
                self.download(torrent)


def parse_args(real_args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('watch', help='Watch folder to download torrents to')
    for group in GROUPS:
        parser.add_argument(f'--no-{group}',
                            help=f'Skip {group} torrents',
                            action='store_true')
    args = parser.parse_args(real_args)
    enabled = []
    for group in GROUPS:
        if not args.__getattribute__(f'no_{group}'):
            enabled.append(group)
    path = Path(args.watch)
    assert path.is_dir()
    return [path, enabled]


def main():
    path, enabled = parse_args()
    ft = FreeTorrents(path)
    ft.run(enabled)


if __name__ == '__main__':
    main()
