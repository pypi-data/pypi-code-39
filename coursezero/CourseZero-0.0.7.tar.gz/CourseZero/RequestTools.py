"""
These are methods and functions to make queries to the site

Created by 復讐者 on 2/15/19
"""
__author__ = '復讐者'

import requests
import json
from bs4 import BeautifulSoup

import environment as env
import CourseZero.UrlMakers as U

ABCS = 'abcdefghijklmnopqrstuvwxyz'

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
HEADERS = { 'User-Agent': USER_AGENT }


def get_content( url, headers=HEADERS ):
    response = requests.get( url, headers=headers )
    return response.content


def get_docs_for_campus(campus_id, campus_name):
    data = []
    print( "Searching for {}".format(campus_name) )
    for letter in ABCS:
        try:
            url = U.make_course_search_url( letter, campus_id )
            r = requests.get( url, headers=HEADERS )
            data.append( r.json() )
        except:
            pass
    return data


def get_docs_for_campuses( campus_ids: list, data_json_path=None ):
    """Queries for all documents for each campus in campus_ids.
    Saves the results as a json to the provided path
    :param data_json_path:
    :param campus_ids: List of tuples with format (csu name, campus id)
    """

    data = [ ]

    for c in campus_ids:
        csu = c['name']
        csuid = c['campus_id']
        data += get_docs_for_campus(csuid, csu)
        # print( "Searching for {}".format(csu) )
        # for letter in ABCS:
        #     try:
        #         url = U.make_course_search_url( letter, csuid )
        #         r = requests.get( url, headers=HEADERS )
        #         data.append( r.json() )
        #     except:
        #         pass

    if data_json_path:
        with open( data_json_path, 'w+' ) as fpp:
            json.dump( data, fpp )

    return data


def get_file_links_from_course_page(course_page_url):
    """Retrieves the page that would be displayed if you went to the
    relevant page on the site, then filters out all the links to files
    since this is what you need to file the request
    Returns a list of tuples (file name, url)
    """
    files = []
    target_url = env.CH_BASE_URL.format(course_page_url)
    # print(target_url)
    html_content = get_content(target_url)
    soup = BeautifulSoup(html_content, 'html.parser')

    for j in soup.findAll('a'):
        try:
            dest = j['href']
            fnd = "/file/"
            if dest[: len(fnd)] == fnd:
                if j.string is not None:
                    files.append((j.string.strip(), env.CH_BASE_URL.format(dest)))
            # files.append((j['string'], env.CH_BASE_URL.format(dest)))
        except Exception as e:
            # print(dest, e)
            pass

    files = list(set(files))
    return files

if __name__ == '__main__':
    pass
