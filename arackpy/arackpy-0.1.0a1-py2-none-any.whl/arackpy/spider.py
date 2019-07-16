"""A multi-threaded web crawler and scraper"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

from abc import abstractmethod
from collections import deque, defaultdict
import logging

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

import random

try:
    from robotparser import RobotFileParser
except ImportError:
    from urllib.robotparser import RobotFileParser

import sys
from socket import gethostbyname
import time
import threading

try:
    from urlparse import urlsplit, urljoin
except ImportError:
    from urllib.parse import urlsplit, urljoin


from arackpy.backends.backend_default import Backend_Default

# change default encoding for py27 from ascii
if sys.version_info <= (2, 7):
    reload(sys)
    sys.setdefaultencoding("utf8")


# report critial levels above 'warning', (i.e. 'error' and 'critical'), default
logging.basicConfig(level=logging.WARNING)

# mapping between name and class
BACKENDS = {"Default": Backend_Default,
            "BeautifulSoup": None,
            "Selenium": None,
            "Tor": None,
            }

try:
    from arackpy.backends.backend_beautifulsoup import Backend_BeautifulSoup
    BACKENDS["BeautifulSoup"] = Backend_BeautifulSoup
except NotImplementedError as e:
    logging.warning("Unable to import backend %s" % "BeautifulSoup")

try:
    from arackpy.backends.backend_selenium import Backend_Selenium
    BACKENDS["Selenium"] = Backend_Selenium
except NotImplementedError as e:
    logging.warning("Unable to import backend %s" % "Selenium")

try:
    from arackpy.backends.backend_tor import Backend_Tor
    BACKENDS["Tor"] = Backend_Tor
except NotImplementedError as e:
    logging.warning("Unable to import backend %s" % "Tor")


class Spider(object):
    """Create a spider.

    The spider is implemented using two queues. Reader threads get from the
    active queue and put into the empty queue. When the active queue is empty,
    it is swapped with the once empty but now full queue. New reader threads
    are spawned at every level and process urls from the active queue.

    Urls are grouped by host server ip address and the corresponding html is
    downloaded sequentially from each ip depending on the requirements set in
    the robots.txt file. If a time duration is not explicitly specified in the
    robots file, the default wait_time_range is used.

    The spider can be terminated by adjusting two parameters, namely max_urls
    and max_levels. Pressing Ctrl-c will also interrupt and terminate the
    process albeit in a harsh manner.

    :Parameters:
        `start_urls` : list
            The starting point for the spider.

        `wait_time_range` : tuple
            A time interval from which a wait time is randomly selected.

        `follow_external_links` : bool
            If set to True, spider will traverse domains outside the starting
            urls.

        `visit_history_limit` : int
            Used to set the cache size of the deque which keeps tracks of all
            the visisted urls.

        `respect_server` : bool
            If set to True, the wait_time_range attribute is applied.

        `read_robots_file` : bool
            If set to True, the robots.txt file is parsed and checked. The
            spider honors the time and/or download rate as well as whether
            to crawl the page at all. If a time cannot be determined, the
            wait_time_range is set to the default.

        `timeout` : int
            The timeout used when the url is read from. If the url cannot be
            read within the specified time, a timeout exception occurs.

        `thread_safe_parse` : bool
            If set to True, the parse method is thread safe, which allows for
            easy debugging using print statements.

        `max_urls_per_level` : int
            Children urls immediately below the start urls form the first
            level. Since the number of urls per level can increase at an
            exponential rate, a limit is set to prevent memory bottlenecks by
            defining a max queue size for the active and empty queues.

        `max_level` : int
            The maximum number of levels to crawl before termination. Everytime
            all the reader threads return (i.e. join), marks the end of the
            previous level and the beginning of the next.

        `max_urls`: int
            The total number of urls to crawl before termination. This is
            implemented using a counter that each reader thread increments
            by one after it reads an url.

        `debug` : bool
            Log all debug messages to stdout.

    TODO

        In order of importance:

        1. Implement a bloomfilter for visisted urls cache instead of a deque.
        2. Implement backends like BeautifulSoup, Tor, Selenium, and proxies.

    BUGS

        1. Fix REAME.rst spacing on bitbucket page.
        2. Fix http://example.com not same as https://example.com/ issue

    """
    # specify one or more website domain names
    start_urls = []

    wait_time_range = (1, 5)

    # stay at the same top level domain
    follow_external_links = False

    # TODO: implement a bloomfilter
    visit_history_limit = 2000

    respect_server = True

    read_robots_file = True

    # urlopen timeout in seconds
    timeout = 5

    # parse method is thread safe
    thread_safe_parse = True

    # max urls to put on queue every jump
    max_urls_per_level = 1000

    # total jumps before termination
    max_levels = 100

    # total urls before termination
    max_urls = 5000

    # debug mode
    debug = False

    def __init__(self, backend="Default"):
        assert len(self.start_urls) <= self.max_urls_per_level

        self.active_queue = Queue(self.max_urls_per_level)
        self.empty_queue = Queue(self.max_urls_per_level)
        self.tlds = [self.get_tld(url) for url in self.start_urls]
        self.robotparser = RobotFileParser()
        self.visited = deque(maxlen=self.visit_history_limit)
        self.lock = threading.Lock()

        # termination flags
        self.level = 0
        self.total_url_count = 0

        # backends for reading html and extracting urls
        try:
            self.backend = BACKENDS[backend]()
        except (KeyError, TypeError):
            self.backend = BACKENDS["Default"]()
            logging.warning("Using backend, %s" % "Default")

        # initialize queue
        for start_url in self.start_urls:
            self.active_queue.put(start_url)

        if self.debug:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)

    def get_tld(self, url):
        """Get the top level domain given the url"""
        return urlsplit(url).netloc

    def crawl(self, max_urls=None):
        if max_urls:
            self.max_urls = max_urls

        try:
            while True:
                ips = self.urls_by_ips()

                # spawn child thread for urls per ip basis
                self.spawn_reader_threads(ips)

                # main thread more responsive than when calling thread.join for
                # spawned thread, wait for spawned threads to terminate after
                # each jump
                while threading.active_count() > 1:
                    time.sleep(0.1)

                # must visit the max_level so max_level + 1
                self.swap_queues()
                self.level += 1

                # check termination
                if self.level == (self.max_levels + 1):
                    logging.info("Reached jump level %s" % self.max_levels)
                    break
                elif self.total_url_count == self.max_urls:
                    logging.info("Reached total read url count %s" %
                                 self.total_url_count)
                    break

        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    def swap_queues(self):
        logging.info("Swapping queues")
        full_queue = self.empty_queue
        self.empty_queue = self.active_queue
        self.active_queue = full_queue

    def spawn_reader_threads(self, ips):
        """Spawn a thread associated with each ip"""
        try:
            # for py27 support
            ipitems = ips.iteritems()
        except AttributeError:
            ipitems = ips.items()

        for ((ip, robot_url), urls) in ipitems:
            child_thread = threading.Thread(target=self.read,
                                            args=(ip, robot_url, urls))
            child_thread.daemon = True
            child_thread.start()

    def urls_by_ips(self):
        """Group urls by host ip address"""
        ips = defaultdict(set)  # remove duplicates

        while not self.active_queue.empty():

            url = self.active_queue.get()

            # for url in iter(self.active_queue.get, None):
            if url in self.visited:
                logging.info("Already visited url, %s" % url)
                continue

            # test if external link and skip
            if self.follow_external_links is False:
                try:
                    if self.get_tld(url) not in self.tlds:
                        logging.info("Skipping external url, %s" % url)
                        continue
                except:
                    logging.warning("Invalid top level url, %s" % url)
                    continue

            """robots.txt based on top level domain because one ip can host
            multiple sites
            """
            robots = {}
            try:
                loc = self.get_tld(url)
                base_url = urlsplit(url).geturl()

                # create robotparser object
                try:
                    scheme = base_url.split(":")[0]
                    robot_url = "".join([scheme, "://", loc])
                    robot = robots.setdefault(loc, robot_url)
                except IOError:
                    robot = None
                    logging.warning("Unable to read robots.txt",
                                    "for url, %s" % base_url)

                # the split(':') allows for port numbers including
                # localhost:8080
                ips[(gethostbyname(loc.split(":")[0]),
                    robot)].add((base_url, url))

            except:
                logging.warning("Unable to group url, %s" % url)
                continue

        return ips

    def read(self, ip, robot_url, urls):
        """Each thread reads and parses urls from one server ip. This allows
        for the thread to respect the server while going through the list
        sequentially.
        """

        if robot_url and self.read_robots_file:
            rp = RobotFileParser(robot_url)
            rp.read()

        for base_url, url in urls:
            try:
                # check robots file
                if rp.can_fetch("*", url) is False:
                    logging.info("robots.txt rejected url, %s" % url)
                    continue
            except:
                pass

            try:
                # download the raw html - note urls contains 'http' or 'https'
                html = self.backend.urlread(url, timeout=self.timeout)
                logging.info("Downloaded url, %s" % url)

                # note as visited - deques are threadsafe for append
                self.visited.append(url)

                if self.thread_safe_parse:
                    with self.lock:
                        self.parse(url, html)
                else:
                    self.parse(url, html)

                self.total_url_count += 1

            except:
                logging.warning("Unable to download and parse url, %s" % url)
                self.visited.append(url)

            # stop each thread if max count is reached
            if self.total_url_count == self.max_urls:
                break

            try:
                # extract new urls
                new_urls = self.backend.urlparse(html)

                # fill up the once empty queue with absolute urls
                for new_url in new_urls:
                    try:
                        # timeout when queue reaches max size
                        self.empty_queue.put(urljoin(base_url, new_url),
                                             timeout=0.1)
                    except Full:
                        logging.info("Queue is full, skipping remaining urls")
                        break
            except:
                logging.warning("Unable to extract urls from url, %s" % url)

            # wait to respect server before jumping expect if one url only
            if self.respect_server and len(urls) > 1:
                try:
                    # python 3.6 method
                    delay = self.robotparser.crawl_delay("*")
                    self.wait(delay=delay)
                except AttributeError:
                    self.wait()

    @abstractmethod
    def parse(self, url, html):
        """User code used to handle each url and corresponding html."""
        raise NotImplementedError("implement")

    def wait(self, delay=None):
        """Enter the total delay time in seconds"""
        if delay is None:
            delay = random.randrange(*self.wait_time_range)
        time.sleep(delay)
