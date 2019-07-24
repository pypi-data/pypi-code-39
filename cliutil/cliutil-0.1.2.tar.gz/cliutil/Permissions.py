import ctypes
import os
import sys


def getwindowsadmin():
    """
    Check if the script is being run with elevated privilages on Windows
    :param restart: restart the script with admin privilaages
    :return: Boolean; is_admin
    """
    try:  # Check for admin rights
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin