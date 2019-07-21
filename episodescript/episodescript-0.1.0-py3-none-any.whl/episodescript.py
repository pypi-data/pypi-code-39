# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


def scrape_episode_scripts(show, season, episode):
    baseurl = "https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=%s&episode=s%02de%02d"
    url = baseurl % (show, season, episode)
    #print("Reading {} ...".format(url))

    x = urlopen(url).read()
    soup = bs(x, features="html5lib")

    div = soup.find("div", "main-content-left")
    if div is None:
        print("Filed scraping")
        return None, None

    title = div.find("h3")
    if title is None:
        print("Failed to find episode title")
        title = "TITLE NOT FOUND"
    else:
        title = title.text

    script = div.find("div", "scrolling-script-container")
    if script is None:
        print("Failed to find script")
        script = "SCRIPT NOT FOUND"
    else:
        for br in script.find_all("br"):
            br.replace_with("\n")
        script = script.get_text().strip()

    return title, script


def episode_script_command():
    parser = ArgumentParser(description="TV Show Script")
    parser.add_argument("show", type=str, help="TV show name")
    parser.add_argument("season", type=int, help="Season number")
    parser.add_argument("episode", type=int, help="Episode number")
    args = parser.parse_args()

    print("TV show script for {}, Season {}, Episode {}".format(args.show, args.season, args.episode))
    sys.stdout.flush()
    title, script = scrape_episode_scripts(args.show, args.season, args.episode)
    print("-------------------------------------------------")
    print(title)
    print("-------------------------------------------------")
    print(script)
    print("-------------------------------------------------")

    return 0

    #return title + "\n\n" + script
    #print(title)
    #for line in script.split("\n"):
    #    print(line)
    #return 0

