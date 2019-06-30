import yaml
import re
import os
import requests
import cnvrg.modules.errors as errors
from tinynetrc import Netrc
from pathlib import Path
NETRC_HOST = "cnvrg.io"
CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".cnvrg", "config.yml")
NETRC_FILE_PATH = os.path.join(os.path.expanduser("~"), '.netrc')


class CnvrgCredentials():

    def __init__(self):
        self.token = None
        self.api_url = self.set_api_url("https://app.cnvrg.io/api")
        self.owner = None
        self.username = None
        self.logged_in = self._load_environ() or self._load_yaml()


    def set_api_url(self, api_url):
        api_url = re.sub(r'(\/api\/?)?(v1.*)?', '', api_url)
        self.api_url = os.path.join(api_url, 'api')
        return self.api_url

    def login(self, email, password, api_url=None):
        api_url = self.set_api_url(api_url or self.api_url)
        resp = requests.post(os.path.join(api_url, 'v1', 'users', 'sign_in'), headers={"EMAIL": email, "PASSWORD": password})
        if resp.status_code != 200:
            raise errors.CnvrgError("Can't Authenticate {email}".format(email=email))

        res = resp.json().get("result")
        token = res.get("token")
        username = res.get("username")
        owner = res.get("owners")[0]
        api_url = api_url or res.get("urls")[0]
        self.__set_credentials(token=token, owner=owner, username=username, email=email, api_url=api_url)
        self.logged_in = True
        self.username = username

    def logout(self):
        if not self.logged_in: return
        netrc= Netrc()
        del netrc[NETRC_HOST]
        netrc.save()
        os.remove(CONFIG_FILE_PATH)
        return True


    def __set_credentials(self, token=None, owner=None, username=None, email=None, api_url=None):
        Path(NETRC_FILE_PATH).touch()
        netrc = Netrc()
        netrc[NETRC_HOST] = {"login": email, "password": token}
        netrc.save()

        os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
        Path(CONFIG_FILE_PATH).touch()
        with open(CONFIG_FILE_PATH, "w") as cnvrg_config:
            yaml.dump({":owner": owner, ":username": username, ":api": api_url}, cnvrg_config)





    def _load_environ(self):
        token = os.environ.get("CNVRG_AUTH_TOKEN")
        api_url = os.environ.get("CNVRG_API")
        owner = os.environ.get("CNVRG_OWNER")
        if not api_url: return None
        self.set_api_url(api_url)
        if not token: return None
        if not owner: return None
        self.token = token
        self.owner = owner
        return True

    def _load_yaml(self):
        if not os.path.exists(NETRC_FILE_PATH): return None
        if not os.path.exists(CONFIG_FILE_PATH): return None
        netrc = Netrc()
        token = netrc[NETRC_HOST]["password"]
        config = yaml.safe_load(open(CONFIG_FILE_PATH, "r"))
        api_url = config.get(":api") or config.get("api")
        owner = config.get(":owner") or config.get("owner")
        if not api_url: return None
        self.set_api_url(api_url)
        if not token: return None
        if not owner: return None
        self.token = token
        self.owner = owner
        return True