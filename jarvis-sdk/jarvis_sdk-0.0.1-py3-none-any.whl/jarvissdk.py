# -*- coding: utf-8 -*-

import os
import argparse
import datetime
import json
import base64
import pickle
import warnings
import pprint

from jarvis_sdk import jarvis_config
from jarvis_sdk import jarvis_configuration_manager

import google.auth

# Globals
#
JARVIS_SDK_VERSION="0.0.1"
PYTHON_EXECUTABLE="python3"
PIP_EXECUTABLE="pip3"


def display_jarvis_header():

    print("")
    print("*************************************************")
    print("*                                               *")
    print("*      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗  *")
    print("*      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝  *")
    print("*      ██║███████║██████╔╝██║   ██║██║███████╗  *")
    print("* ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║  *")
    print("* ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║  *")
    print("*  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝  *")
    print("*                                               *")
    print("*             ███████╗██████╗ ██╗  ██╗          *")
    print("*             ██╔════╝██╔══██╗██║ ██╔╝          *")
    print("*             ███████╗██║  ██║█████╔╝           *")
    print("*             ╚════██║██║  ██║██╔═██╗           *")
    print("*             ███████║██████╔╝██║  ██╗          *")
    print("*             ╚══════╝╚═════╝ ╚═╝  ╚═╝          *")
    print("*                                               *")
    print("*************************************************")
    print("Version : " + JARVIS_SDK_VERSION)
    print("")


def get_user_gcp_credential():

    try:

        # Get default infos
        #
        credentials, project = google.auth.default()

        # Pickling the Credential object
        #
        pickled_credentials = pickle.dumps(credentials)

        # Encode pickled credentials using Base64
        #
        base64_pickled_credentials = base64.encodebytes(pickled_credentials)

        # Convert to string
        #
        final_payload = str(base64_pickled_credentials, "utf-8")

        return final_payload

    except Exception as ex:
        print(ex)
        print("Error while retrieving GCP default credentials.")
        print("Did you run the gcloud command : gcloud auth application-default login")
        return None


def main():

    # Display Jarvis header
    #
    display_jarvis_header()

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("command", help="Jarvis SDK command.", type=str)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)

    # parser.add_argument("-i", "--install", help="Jarvis SDK installation process", type=str)

    # parser.add_argument("collection", help="Firebase collection.", type=str)
    # parser.add_argument("document_id", help="Document ID to be updated.", type=str)

    args = parser.parse_args()

    # Retrieve Jarvis configuration
    #
    # /Users/jguarino/.jarvis-home/jarvis-configuration.json
    #
    jarvis_configuration = None
    with open("/Users/jguarino/.jarvis-home/jarvis-configuration.json", "r") as f:
        jarvis_configuration = json.load(f)
        print(jarvis_configuration)

    # Extract GCP user's credentials
    #
    user_credential = get_user_gcp_credential()
    if user_credential is None:
        # Exiting
        return

    # Evaluating COMMAND
    #
    if args.command == "config":

        jarvis_config.jarvis_config()

    elif args.command == "deploy":

        if len(args.arguments) > 0:
            if (args.arguments)[0] == "configuration":
                jarvis_configuration_manager.process(args.command, args.arguments, jarvis_configuration, user_credential)

        else:
            print("Needs help here ...")




if __name__ == "__main__":
    main()