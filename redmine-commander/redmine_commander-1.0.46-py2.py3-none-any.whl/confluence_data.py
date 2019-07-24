#!/usr/bin/env python
from redmine_commander.config import *
from dateutil import parser
from dateutil import relativedelta
from datetime import datetime, date, timedelta
from pprint import pprint
from requests.auth import HTTPBasicAuth
import rofi
import re
import webbrowser
import logging
import requests
import json

def pager(base_url, *args, cert=False, user=None, passw=None):
    c=0
    while True:
        try:
            ret = req(base_url, *args, 'start=%s' % c, cert=cert, user=user, passw=passw)
            yield ret
            c+=100
        except Exception as e:
            print("paging error %s" % e)
            pass

def req(base_url, *kwargs, cert=False, user=None, passw=None):
    try:
        f_req = '&'.join([*kwargs])
        f_req = os.path.join(base_url, "content?%s" % f_req)
        print(f_req)
        if cert:
            return requests.get(f_req, cert=cert, auth=HTTPBasicAuth(user, passw))
        else:
            return requests.get(f_req)
    except Exception as e:
        logging.log(logging.ERROR, "REST Call failed\n%s" %  e)


def fetch_confluence_documents(f_src, cert, user, passw):

    rofi.Rofi().status("downloading issues ... ")

    fltr = [ "type=page", "expand=version,body.view", "limit=99999"]
    base_url="https://confluence.openinfrastructure.de/rest/api"

    documents=[]
    for index, page in enumerate(pager(base_url, *fltr, cert=cert, user=user, passw=passw)):
        i = json.loads(page.text)["results"]
        documents.extend(sorted(i, key=lambda k: k['id']))
        if len(i)<100:
            break

    with shelve.open(f_src) as db:
        db['confluence'] = documents

    rofi.Rofi().status(" ... done!")
    return len(documents)

def get_confluence_documents(f_src):
    with shelve.open(f_src) as db:
        documents = db['confluence']

    tmp={}
    documents={document['id']: document for document in documents}
#    documents=(sorted(i, key=lambda k: k['id']))

    for index, document in enumerate(reversed(sorted(documents.values(), key=lambda k: k['version']['when']))):
        t_id=document['id']
        name=str(document['title']).lower()
        space=str(document['_expandable']['space']).split('/')[-1].lower()
        link=document['_links']['webui']
        content=str(document['body']['view']['value']).lower()
        who=str(document['version']['by']['displayName']).lower()
        when=str(document['version']['when']).split('.')[0]
        tmp[index]=[t_id, '{:8s} {:30.25s} {:85.80s} {:20.20s} {:>20s}'.format(
            str(t_id).strip(),
            str(space[:25]).strip().ljust(25),
            str(name[:80]).strip(),
            str(who[:20]).strip(),
            when)]
    return tmp

def confluence_open_in_browser(f_src, t_id):
    with shelve.open(f_src) as db:
        documents = db['confluence']
    tmp={}
    data=[d['_links']['webui'] for d  in documents if d['id'] in str(t_id)]
    link="https://confluence.openinfrastructure.de%s" % data[0]
    webbrowser.open_new_tab(link)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def preview_document(f_src, t_id):
    with shelve.open(f_src) as db:
        documents = db['confluence']

    tmp={}
    data={d['title']: d['body']['view']['value'] for d  in documents if d['id'] in str(t_id)}
    title=list(data.keys())[0]
    prev=list(data.values())[0]
    prev=cleanhtml(prev)

    tmp[0]=[t_id, '{:^170s}'.format(str(title))]
    tmp[1]=[t_id, '{:170s}'.format(str('-'*170))]

    i=2
    while len(prev) > 120:
        tmp[i]=[t_id, '{:^170s}'.format(
            str(prev[:120]))]
        prev=prev[120:]
        i+=1
    return tmp


