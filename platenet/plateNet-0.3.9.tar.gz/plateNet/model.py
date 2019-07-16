import os
import sys
from pathlib import Path
from urllib.request import urlopen

import requests

import plateNet.color as color
from plateNet.tools import message


def internet_on():
    try:
        urlopen('https://www.google.com/', timeout=1)
        return True
    except:
        return False


def __download_file_from_google_drive(id, destination):
    if internet_on():
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': id}, stream=True)
        token = __get_confirm_token(response)

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        __save_response_content(response, destination)
        return True
    else:
        message("Could not download because no internet connection was found", color.CRED)
        sys.exit()


def __get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def __save_response_content(response, destination):
    CHUNK_SIZE = 327680

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return True


def download_plateNet_448(update:bool=False,savefolder="plateNet-448"):
    # savefolder = "plateNet-448"

    if not os.path.exists(savefolder):
        os.mkdir(savefolder)

    weights = "plateNet_448_last.weights"
    # weightsID = '1ZFCA_LtB3F7hk71a9YWMRSFeGZGgfiBr'
    weightsID = '1tjfTEZYcfe3dw91mOL7yNa-EejTQxRfd'
    # https://drive.google.com/open?id=1tjfTEZYcfe3dw91mOL7yNa-EejTQxRfd
    cfg = "plateNet_448.cfg"
    cfgID = '1V7etbj5YB41AcPH4s4hZQ_YVVIBnOZvC'

    items =[
        [cfg, cfgID],
        [weights,weightsID]

    ]
    downloadedPaths = []
    for item in items:

        path = os.path.join(savefolder, item[0])
        downloadedPaths.append(path)
        if not Path(path).is_file() or update:
            message("%s downloading..." % path, color.CVIOLET)
            __download_file_from_google_drive(item[1], path)
        else:
            message("%s found." % path, color.CGREEN)

    return downloadedPaths
