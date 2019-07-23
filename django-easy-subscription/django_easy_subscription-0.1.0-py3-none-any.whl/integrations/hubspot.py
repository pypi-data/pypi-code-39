import logging
import requests
from .base import BaseIntegration


logger = logging.getLogger(__name__)


class HubSpot(BaseIntegration):
    required_credentials = ['api_key']

    def get_contact_vid(self, email):
        url = 'https://api.hubapi.com/contacts/v1/contact/email/{}/profile?hapikey={}'.format(
            email, self.api_key
        )

        r = requests.get(url=url)
        if r.status_code == 200:
            return r.json()['vid']
        else:
            raise Exception(r.text)

    def subscribe(self, subscriber):
        """
        Create a contact if it doesn't exist, or update it
        with the latest property values if it does.
        Created contacts are automatically subscribed.
        """
        url = 'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{}/?hapikey={}'.format(
            subscriber.email, self.api_key
        )
        data = {
            'properties': [
                {'property': 'email', 'value': subscriber.email},
                {'property': 'firstname', 'value': subscriber.email},
                {'property': 'lastname', 'value': subscriber.last_name},
                {'property': 'hs_language', 'value': subscriber.language},
            ]
        }

        r = requests.post(url=url, json=data)
        if r.status_code == 200:
            return True
        else:
            logger.error(r.text)
            return False

    def unsubscribe(self, subscriber, delete=False):
        if not delete:
            url = 'https://api.hubapi.com/email/public/v1/subscriptions/{}'.format(
                subscriber.email
            )
            data = {'unsubscribeFromAll': True}

            r = requests.put(url=url, json=data)
            if r.status_code == 200:
                return True
            else:
                logger.error(r.text)
                return False
        else:
            vid = self.get_contact_vid(subscriber.email)
            url = 'https://api.hubapi.com/contacts/v1/contact/vid/{}?hapikey={}'.format(
                vid, self.api_key
            )

            r = requests.delete(url=url)
            if r.status_code == 200:
                return True
            else:
                logger.error(r.text)
                return False


integration_class = HubSpot
