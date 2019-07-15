import logging
import requests
import urllib3
from bs4 import BeautifulSoup
import re


log = logging.getLogger(__name__)


class OAMSSO():
    """Easily access pages protected with Oracle Access Management SSO"""

    def __init__(self,
                 protected_url,               # protected URL is required to catch the redirect to SSO
                 sso_credentials,             # dictionary containing 'sso_user' and 'sso_password'
                 sso_url,                     # URL for the OAM login
                 verify=True,
                 protected_url_method='get'  # some pages only support POST method. Set this to determine which
                                              # method to use in order to catch the SSO redirect
                 ):
        self.protected_url = protected_url
        self.sso_url = sso_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
        self.sso_credentials = sso_credentials
        self.session = requests.session()
        self.data = {}
        if not verify:
            self.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        else:
            self.verify = verify
        self.protected_url_method = protected_url_method

    def login(self):
        """Attempt to login. A protected URL is required here to catch the redirect."""
        log.info('Initializing requests session')
        self.session.headers.update(self.headers)
        log.info('Initialization complete')

        log.info('Gathering JSESSIONID...')
        log.info('GET request to {}'.format(self.protected_url))

        # post vs get logic

        r = self.post(self.protected_url)
        if r.status_code != requests.codes.ok:
            log.error('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
            Exception('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
        elif 'you must press the button below once' in r.text:
            log.warning('No javascript detection triggered! Must use interim page')
            svars = self.build_csrf_vars(r)
            soup = BeautifulSoup(r.content, 'lxml')
            postURL = soup.find('form', method=re.compile('post', re.IGNORECASE)).get('action')
            log.warning('Interim POST URL {}'.format(postURL))
            r = self.post(postURL, data=svars)
            if r.status_code != requests.codes.ok:
                log.error('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
                Exception('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
        log.debug(r.cookies)
        log.debug(r.content)
        if r.cookies.get_dict()['JSESSIONID']:
            log.info('Done gathering JSESSIONID')
        else:
            log.error('JSESSIONID not found!')
            Exception('JSESSIONID not found!')

        log.info('Generating svars from SSO login page')
        svars = self.build_csrf_vars(r)  # TODO maybe need to save SAMLrequest if no-javascript is detected
        svars['userid'] = self.sso_credentials['sso_user']
        svars['password'] = self.sso_credentials['sso_password']

        log.info('POSTing credentials to SSO')
        r = self.post(self.sso_url, data=svars)
        log.debug(r.content)

        if r.status_code != requests.codes.ok:
            log.error('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
            Exception('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
        elif 'saml2-acs.php' in r.text:
            """ More javascript funny business"""
            log.warning('No javascript detection triggered! Must use interim page')
            svars = self.build_csrf_vars(r)
            soup = BeautifulSoup(r.content, 'lxml')
            postURL = soup.find('form', method=re.compile('post', re.IGNORECASE)).get('action')
            log.warning('Interim POST URL {}'.format(postURL))
            r = self.post(postURL, data=svars)
            if r.status_code != requests.codes.ok:
                log.error('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
                Exception('Received HTTP {0} when attempting to access {1}'.format(r.status_code, self.protected_url))
        else:
            log.info('Successfully logged in')
            return True

    def build_csrf_vars(self, response):
        """ Takes response body as input and returns all hidden input fields/values as a dictionary"""

        log.info('CSRF: Building svars database')
        c = response.content
        soup = BeautifulSoup(c, 'lxml')
        svars = {}
        for var in soup.findAll('input', type="hidden"):
            svars[var['name']] = var['value']
            log.debug('CSRF: {}'.format(var))
        log.debug('CSRF: Returning csrf list: {}'.format(svars))

        return svars

    def get(self, url, data=None, params=None):
        """Method utilizes existing requests session for repeated GET requests"""
        return self.session.get(url, data=data, params=params, verify=self.verify)

    def post(self, url, data=None, params=None):
        """Method utilizes existing requests session for repeated POST requests"""
        return self.session.post(url, data=data, params=params, verify=self.verify)
