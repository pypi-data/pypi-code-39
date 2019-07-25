"""Simple Web Downloader"""

__version__ = "0.0.6"
__author__ = "Aditya Kelvianto Sidharta"

import os
import random
import string
from multiprocessing.dummy import Pool as ThreadPool
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger


class Keruk:
    def __init__(
        self, timeout=3, save_path=None, use_proxy=True, num_workers=100, verbose=False
    ):
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.num_workers = num_workers
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"}
        self.workdir = os.getcwd()
        self.logger = logger
        self.verbose = verbose

        if save_path is None:
            self.save_path = os.path.join(self.workdir, "keruk_result_{}".format(self._get_datetime()))
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        else:
            self.save_path = save_path
        self.logger.info("Saving files at {}".format(self.save_path))

        self.ip_address, self.port, self.n_proxy = self._init_proxy()

    @staticmethod
    def _get_datetime():
        return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def _is_bad_proxy(self, pip):
        proxy = {"http": "http://{}".format(pip), "https": "http://{}".format(pip)}
        response = self._get_url("http://example.com", proxy=proxy)
        if response is None:
            return True
        elif response.status_code != 200:
            return True
        else:
            return False

    def _init_proxy(self):
        response = requests.get("https://www.sslproxies.org/")
        assert response.status_code == 200
        soup = BeautifulSoup(response.text, "html.parser")

        result_list = []
        tr_values = soup.find_all("tr")
        assert len(tr_values) > 0
        for tr_value in tr_values:
            td_values = tr_value.find_all("td")
            if len(td_values) == 8:
                result_list.append(
                    {
                        "ip_address": td_values[0].get_text(),
                        "port": td_values[1].get_text(),
                        "code": td_values[2].get_text(),
                        "country": td_values[3].get_text(),
                        "anonymity": td_values[4].get_text(),
                        "google": td_values[5].get_text(),
                        "https": td_values[6].get_text(),
                        "last_checked": td_values[7].get_text(),
                    }
                )
            else:
                continue
        proxy_df = pd.DataFrame(result_list)
        proxy_df["port"] = proxy_df["port"].astype(int)
        proxy_df = proxy_df[proxy_df.https == "yes"]

        ip_addresses, ports = proxy_df.ip_address.tolist(), proxy_df.port.tolist()
        full_addresses = ["{}:{}".format(ip_address, port) for ip_address, port in zip(ip_addresses, ports)]
        bad_proxies = self._parallel(full_addresses, self._is_bad_proxy)
        assert len(bad_proxies) == len(ip_addresses)
        assert len(bad_proxies) == len(ports)

        result_ip_address = []
        result_port = []

        for idx in range(len(bad_proxies)):
            if not bad_proxies[idx]:
                result_ip_address.append(ip_addresses[idx])
                result_port.append(ports[idx])
        return result_ip_address, result_port, len(result_ip_address)

    def _parallel(self, data, fn):
        with ThreadPool(self.num_workers) as p:
            result = p.map(fn, data)
        return result

    def _sample_proxy(self):
        random_idx = random.choice(range(self.n_proxy))
        sample_ip = self.ip_address[random_idx]
        sample_port = self.port[random_idx]

        return {
            "http": "http://{}:{}".format(sample_ip, sample_port),
            "https": "http://{}:{}".format(sample_ip, sample_port),
        }

    def _get_url(self, url, proxy=None):
        try:
            if proxy is not None:
                response = requests.get(url, headers=self.header, proxies=proxy, timeout=self.timeout)
            elif self.use_proxy and proxy is None:
                response = requests.get(url, headers=self.header, proxies=self._sample_proxy(), timeout=self.timeout)
            else:
                response = requests.get(url, headers=self.header, timeout=self.timeout)
            if self.verbose:
                self.logger.info("URL : {}, STATUS_CODE : {}".format(url, response.status_code))
            return response
        except Exception as e:
            if self.verbose:
                self.logger.info("URL : {}, ERROR : {}".format(url, e))
            return None

    def save_url(self, url):
        response = self._get_url(url)
        if response is None:
            return False
        if response.status_code == 200:
            path = os.path.join(self.save_path, url.translate(str.maketrans("", "", string.punctuation)))
            with open(path, "w+") as f:
                f.write(response.text)
            return True
        else:
            return False

    def open_url(self, url):
        path = os.path.join(self.save_path, url.translate(str.maketrans("", "", string.punctuation)))
        assert os.path.exists(path)
        with open(path, "r") as f:
            response_text = f.read()
        return response_text

    def save_urls(self, urls):
        return self._parallel(urls, self.save_url)
