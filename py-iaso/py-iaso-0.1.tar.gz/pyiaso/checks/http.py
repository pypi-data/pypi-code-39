import requests
from typing import List

from . import DefaultCheck
from ..utils import print_log

class HttpCheck(DefaultCheck):
    def __init__(self, *url_list: List[str]):
        self.url_list = url_list

    def check(self) -> bool:
        for url in self.url_list:
            try:
                r = requests.get(url)
                if not r.status_code == 200:
                    self.failure = 'HTTP code {} for {}'.format(r.status_code, url)
                    return False
            except requests.exceptions.RequestException as e:
                self.failure = 'Error fetching {}.\n\n{}'.format(url, e)
                return False
        
        self.failure = None
        return True
