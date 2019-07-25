# -*- coding: utf-8 -*-
# diamond-patterns (cc) 2019 Ian Dennis Miller

import os
import glob
import json
import arrow
import requests


class Pattern:
    def __init__(self):
        self.config_file = "~/.diamond-patterns.json"
        self.config_file = os.path.expanduser(self.config_file)

        self.ensure_config()
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        self.config["manifest_file"] = os.path.expanduser(self.config["manifest_file"])

        self.ensure_manifest()
        with open(self.config["manifest_file"], 'r') as f:
            self.manifest = json.load(f)

        self.patterns = self.manifest['patterns']

    def ensure_config(self):
        master_config = {
            'manifest_file': '~/.diamond-patterns-manifest.json',
            'manifest_url': 'https://raw.githubusercontent.com/iandennismiller/diamond-patterns/master/patterns/manifest.json',
            'archive_url': 'https://github.com/iandennismiller/diamond-patterns/archive/master.zip#diamond-patterns-master/patterns',
        }

        if not os.path.isfile(self.config_file):
            print("WARNING: {} not found".format(self.config_file))
            with open(self.config_file, 'w') as f:
                f.write(json.dumps(master_config, indent=2, sort_keys=True))

    def open_docs(self, pattern):
        if pattern not in self.patterns:
            print("unrecognized pattern: {0}".format(pattern))
            return
        
        url = "https://diamond-patterns.readthedocs.io/en/latest/patterns/{}.html".format(pattern)
        print("Open: {}".format(url))
        os.system("open '{}'".format(url))

    def run_scaffold(self, pattern, interactive=True):
        if pattern not in self.patterns:
            print("unrecognized pattern: {0}".format(pattern))
            return

        pattern_url = "{}/{}".format(self.config["archive_url"], pattern)

        if interactive:
            cmd = "mrbob -w -O . {}".format(pattern_url)
        else:
            cmd = "mrbob -w -n -O . {}".format(pattern_url)
        os.system(cmd)

    def download_manifest(self):
        r = requests.get(self.config["manifest_url"])
        if r.status_code == 200:
            with open(self.config["manifest_file"], 'w') as f:
                f.write(r.text)
        else:
            print("ERROR: failed to download {}".format(self.config["manifest_url"]))

    def ensure_manifest(self):
        if not os.path.isfile(self.config['manifest_file']):
            print("WARNING: {} not found".format(self.config["manifest_file"]))
            self.download_manifest()

    def write_manifest(self):
        h = {
            'timestamp': arrow.utcnow().timestamp,
            'patterns': [f.split('/')[1] for f in glob.glob("patterns/*/")],
        }

        with open('patterns/manifest.json', 'w') as f:
            f.write(json.dumps(h, indent=2, sort_keys=True))
