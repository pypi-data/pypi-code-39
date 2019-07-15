
import requests

class Slack(object):
    def __init__(self, api_token, slack_url="https://api.slack.com", ssl_verify=True, timeout=None):
        self.slack_url = slack_url
        self.rest_url = slack_url.rstrip('/') + "/api"
        self.ssl_verify = ssl_verify
        self.api_token = api_token
        self.timeout = timeout

        self.session = self._build_session(content_type='json')
    
    def __str__(self):
        return "Slack API Client at {}".format(self.slack_url)
        
    def _build_session(self, content_type="json"):
        headers = {
            'Content-Type': 'application/{}'.format(content_type),
            'Accept': 'application/{}'.format(content_type),
            'Authorization': 'Bearer ' + self.api_token
        }

        session = requests.Session()
        session.verify = self.ssl_verify
        session.headers.update(headers)
        return session

    def _get(self, *args, **kwargs):
        """ Wrapper around Requests for GET requests

        Returns:
            Response:
                A Requests Response Object
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        req = self.session.get(*args, **kwargs)
        return req
    
    def _post(self, *args, **kwargs):
        """ Wrapper around Requests for POST requests

        Returns:
            Response:
                A Requests Response Object
        """
        print(kwargs)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        
        req = self.session.post(*args, **kwargs)
        return req

    def _patch(self, *args, **kwargs):
        """ Wrapper around Requests for PATCH requests

        Returns:
            Response:
                A Requests Response Object
        """
        req = self.session.patch(*args, **kwargs)
        return req

    def _delete(self, *args, **kwargs):
        """ Wrapper around Requests for DELETE requests

        Returns:
            Response:
                A Requests Response Object
        """

        req = self.session.delete(*args, **kwargs)
        return req
