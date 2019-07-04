#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import glob

from orbis import app

from .html_pages import HTMLPages

from orbis.core.addon import AddonBaseClass


class Tunnelblick(AddonBaseClass):
    """docstring for Tunnelblick"""

    def __init__(self):
        super(AddonBaseClass, self).__init__()
        self.addon_path = os.path.realpath(__file__).replace("main.py", "")

    def get_folder_names(self):
        return [(corpus.strip("/").split("/")[-1], corpus) for corpus in glob.glob(os.path.join(app.paths.corpora_dir, "*/"))]


    def menu(self):
        os.system('cls')  # on Windows
        os.system('clear')  # on linux / os x

        print("\nWelcome to Tunnelblick!")
        print("Which corpus would you like to look at?")

        corpora = self.get_folder_names()
        for idx, (corpus, corpus_path) in enumerate(corpora):
            print(f"[{idx}]:\t {corpus} ({corpus_path})")
        selection = int(input("--> "))

        hp = HTMLPages(*corpora[selection])
        hp.run()


    def run(self):
        self.menu()
