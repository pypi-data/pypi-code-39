"""Use Tor to scrape websites. Remember to still respect the server!

# https://www.sylvaindurand.org/use-tor-with-python/

1. Make sure tor is installed.

$ sudo apt-get install tor
$ sudo service tor start
$ curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs

2. Install requests

$ pip install requests
$ pip install requests[socks]
$ pip install requests[security]

try this is you have problems with crpytography
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

3. Install stem

4. Install fake_useragent
"""

raise NotImplementedError("coming soon")


from arackpy.backends.backend_default import Backend

import requests

from stem import Signal
from stem.control import Controller

from fake_useragent import UserAgent


class Backend_Tor(Backend):
    """Uses the Tor protocol to anonymously crawl pages"""
    pass
