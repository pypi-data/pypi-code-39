import logging
import os
import time

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
import requests

log = logging.getLogger('allgo')
__version__ = '0.1.11'


def local_token():
    from os.path import expanduser
    home = expanduser("~")
    filetoken = os.path.join(home, '.allgo_token')
    if os.path.exists(filetoken):
        with open(filetoken) as f:
            return f.read()


class App:
    """
    AllGo app submission object
    """

    def __init__(self, name, token=None):
        """
        Constructor
        :param name: name of the application in lower case
        :param token: if not provided, we check ALLGO_TOKEN env variable and notebook parameters
        """
        self.name = name
        if token:
            self.token = token
        elif 'ALLGO_TOKEN' in os.environ.keys():
            self.token = os.environ.get('ALLGO_TOKEN')
        elif local_token():
            self.token = local_token()
        else:
            err_msg  = "You must provide a token in parameter"
            err_msg += " or define an environment variable 'ALLGO_TOKEN'"
            raise Exception(err_msg)

    def run(self, files, outputdir='.', params='', verify_tls=True):
        """
        Submit the job
        :param files: input files
        :param outputdir: by default current directory
        :param params: a string parameters see the application documentation
        :param verify_tls: [True] the value is pass to the verify arg of requests.post
        :return:
        """
        headers = {'Authorization': 'Token token={}'.format(self.token)}
        data = {"job[webapp_name]": self.name,
                "job[webapp_id]": self.name,
                "job[param]": params}
        ALLGO_URL = os.environ.get('ALLGO_URL', "https://allgo.inria.fr")
        url = '%s/api/v1/jobs' % ALLGO_URL
        r = requests.post(url, headers=headers, files=files, data=data, verify=verify_tls)
        r.raise_for_status()
        r = r.json()
        if 'id' in r.keys():
            jobid = r['id']
        else:
            jobid = list(r.keys())[0]
        results = None
        while True:
            url = '{}/api/v1/jobs/{}'.format(ALLGO_URL, jobid)
            r = requests.get(url, headers=headers, verify=verify_tls)
            r.raise_for_status()
            results = r.json()
            if 'status' in results.keys():
                status = results['status']
            else:
                status = list(results.values())[0]['status']
            if status in ['created', 'waiting', 'running', 'in progress']:
                log.info("wait for job %s in status %s", jobid, status)
                time.sleep(2)
            else:
                break

        if status != 'done':
            raise Exception('Job %s failed with status %s', (jobid, status))

        elif status == 'done' and results:
            if 'id' in results.keys():
                files = results[str(jobid)].items()
            else:
                files = results[str(jobid)]['files'].items()
            for filename, url in files:
                filepath = os.path.join(outputdir, filename)
                with requests.get(url, headers=headers, verify=verify_tls, stream=True) as r:
                    r.raise_for_status()
                    with open(filepath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): 
                            if chunk: 
                                f.write(chunk)
