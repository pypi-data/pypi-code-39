"""
This module provides verification of user's email and password.


"""

import runningConfiguration as cfg
import requests

name = "miupload"

# Check if module is configured and ready.
try:
    if (cfg.configured):
        ready = True
    else:
        ready = False
except:
    ready = False

try:
    if (cfg.base_url):
        base_url = cfg.base_url
    else:
        base_url = "http://sss-data.minerva.community"
except:
    base_url = "http://sss-data.minerva.community"

def get_status():
    global ready
    global base_url
    print(ready,base_url)
    return ready


def login(email, psw):
    """

    Function checks email password and then saves configuration data for later use.

    :param email:
    :param psw:
    :return:
    """
    global ready
    global base_url
    if (ready):
        Q = input("Module is already configured. Rewrite? (y/n")
        if (Q == "y"):
            pass
        else:
            "Answer not recognized. Configuration aborted."
            return None

    print("Contacting data server...")

    r = requests.post(base_url+"/User/validate", data={'email': email, 'psw': psw})
    print(r.content)
    if (r.content == "TRUE"):  # TODO
        print("Verification successful! Saving Configuration...")
        cfg.email = email
        cfg.psw = psw
        cfg.configured = True
        ready = True
    else:
        print("Verification failed! Please check your Minerva email and password. Try again!")
        return False

    print("Hello Minerva")


def set_server(new_url):
    """
    For DEBUG only. Allows to change server address and redirect communication to alternative server.

    :param url:
    :return:
    """
    global base_url

    cfg.base_url = new_url
    base_url = new_url
    return True


def submit_notebook():
    print("Autosaving notebook...")
