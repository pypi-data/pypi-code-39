# -*- coding: utf-8 -*-

def display_help():

    help = """
Jarvis SDK Help
===============

usage : jarvis [--gcp-project-id GOOGLE_PROJECT_ID] COMMAND ARGUMENTS


Configure Jarvis SDK
--------------------

usage : jarvis config


Authenticate with Firebase
--------------------------

usage : jarvis auth login


Configuration deployment
------------------------

Please type : jarvis deploy configuration help

"""

    print(help)