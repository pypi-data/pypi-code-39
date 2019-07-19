# -*- coding: utf-8 -*-

import os
import sys
import requests

import shutil
import json
from pathlib import Path
from subprocess import check_output
import platform
import ctypes

# Globals
#


def display_configuration_deploy_help(jarvis_configuration):

    try:
        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/help"
        data = {
            "payload": {
                "resource": "help"
            }
        }
        headers = {"Content-type": "application/json"}
        params = {"key" : jarvis_configuration["jarvis_api_key"]}

        r = requests.post(url, headers=headers, data=json.dumps(data), params=params)

        response = r.json()

        print(response["payload"]["help"])

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False

    return True


def deploy_configuration(input_conf_file, gcp_project_id, jarvis_configuration, user_credentials):

    # Check if the file exists
    #
    if os.path.isfile(input_conf_file) is False:
        print("File \"%s\" does not exists." % input_conf_file)
        return False

    # Read file and parse it as JSON
    #
    read_configuration = None
    try:
        with open(input_conf_file, "r") as f:
            read_configuration = json.load(f)
    except Exception as ex:
        print("Error while parsing configuration file.")
        return False

    # Call API
    #
    try:

        if gcp_project_id is None:
            gcp_project_id = jarvis_configuration["gcp_default_project"]
            print("Destination GCP Project : %s" % gcp_project_id)

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration"
        data = {
            "payload": {
                "resource": read_configuration,
                "gcp_project_id" : gcp_project_id,
                "user_credentials" : user_credentials
            }
        }
        headers = {"Content-type": "application/json"}
        params = {"key" : jarvis_configuration["jarvis_api_key"]}

        response = requests.put(url, headers=headers, data=json.dumps(data), params=params)

        if response.status_code != 200 :
            print("API returned an error.")
            print(response.json())
            return False

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False

    # Success
    #
    print("Configuration deployed successfully.")
    return True


def process(command, arguments, jarvis_configuration, user_credentials):

    print("Jarvis Configuration Manager.")

    if command == "deploy":
        if len(arguments) >= 2:
            if arguments[1] is not None:
                if arguments[1] == "help":
                    return display_configuration_deploy_help(jarvis_configuration)
                else:

                    # Check if the GCP Project ID has been specified
                    #
                    gcp_project_id = None
                    try:
                        gcp_project_id = arguments[2]
                    except IndexError:
                        print("GCP Project ID not specified, will use default.")

                    return deploy_configuration(arguments[1],gcp_project_id, jarvis_configuration, user_credentials)
            else:
                print("Argument unknown." % arguments[1])
                return False
        else:
            return display_configuration_deploy_help(jarvis_configuration)

    return True
