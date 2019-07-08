# -*- coding: utf-8 -*-
from time import sleep
import urllib.request, urllib.error, urllib.parse
import os
from pprint import pprint
import configparser
from os.path import expanduser
import functools
import operator


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from bs4 import BeautifulSoup as BSoup

def get_credentials(filepath='~/.russianpodcast'):
    filepath = expanduser(filepath)
    config = configparser.ConfigParser()
    config.read(expanduser('~/.russianpodcast'))
    config = config['russianpodcast']
    return config['emailadress'], config['password']





def get_links(page_source):
    soup = BSoup(page_source, 'html.parser')
    balises = [x.find_all('a')
               for x in soup.find_all(
               class_="wpb_text_column wpb_content_element")
               if len(x.find_all('p')) == 3]
    return balises



from selenium.webdriver.firefox.options import Options

headless = Options()
headless.add_argument("--headless")

print_pdfs_with_default_printer = False  # Uses default printer on linux
target_folder = expanduser("~/klimova_posdcasts")
quiet = True


class PodcastGetter(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(20)

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        os.chdir(target_folder)  # Use proper context manager instead
        self.present_files = [f for f in os.listdir(".") if os.path.isfile(f)]
        print("init done")

    def log_in(self):
        print("logging in ", end=" ")
        import sys
        emailaddress, password = get_credentials()
        sys.stdout.flush()
        driver = self.driver
        driver.get("https://russianpodcast.eu/russian-dacha-club")
        driver.find_element_by_name("email").send_keys(emailaddress)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_name("LoginDAPLoginForm").click()
        print("logged in")

    def refreshed_page_source(self, delay=2):
        """ This is a heck because getting the content right after login
        gives you le login page content """
        driver = self.driver

        sleep(delay)
        driver.refresh()  # The url is the same so you need to re-fetch the content
        print("refresed")
        sleep(0.5)
        source = driver.page_source
        return source

    def __call__(self):
        self.log_in()
        page_source = self.refreshed_page_source()
        print("got source")
        print(os.getcwd())
        #page_source = open('../sample.html').read()
        links = get_links(page_source)
        self.driver.quit()
        print("quitted driver")
        links = functools.reduce(operator.iconcat, links, [])
        to_do = self.filter_files([link['href'] for link in links])
        print(to_do)
        self.process_files(to_do)



    def filter_files(self, links):
        def filename(link):
            return link.split("/")[-1]

        def is_there(link_title):
            return filename(link_title) in self.present_files

        return [
            (link, filename(link))

            for link in links
            if not is_there(link)
        ]

    def process_files(self, files_to_get):
        for link, filename in files_to_get:
            print("processing:\n", "\n".join([link, filename]))
            with open(filename, "wb") as f:
                f.write(urllib.request.urlopen(link).read())
                if filename.lower().endswith("pdf") and print_pdfs_with_default_printer:
                    print((os.system("lp %s" % filename)))

def main():
    try:
        print("Checking firefox driver is here")
        if quiet:
            driver = webdriver.Firefox(firefox_options=headless)
        else:
            driver = webdriver.Firefox()
    except Exception as E:
        import logging

        logging.exception(E)

        print("Looks like firefox webdriver is not installed")
        print(
            "See https://github.com/mozilla/geckodriver/releases go to assets todownload"
        )
        print(
            "https://stackoverflow.com/questions/42204897/how-to-setup-selenium-python-environment-for-firefox for more help"
        )
    else:
        print("Yey firefox driver seems installed")
        PodcastGetter(driver)()

if __name__ == "__main__":
    main()

