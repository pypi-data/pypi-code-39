import json
from .. import exceptions


class UserAdmin(object):
    def __init__(self, slackAPIClient):
        self.api_client = slackAPIClient
        self.api_client.rest_url = slackAPIClient.slack_url + "/scim/v1"

    def test(self):
        return(self.api_client)

    def add(self, email, givenName=None, familyName=None):
        """ Adds a user to the workspace.

        Inputs:
            email (required)
            givenName (optional)
            familyName (optional)
        """

        userJson = {
            "schemas": [
                "urn:scim:schemas:core:1.0",
                "urn:scim:schemas:extension:enterprise:1.0"
            ],
            "name": {
                "familyName": familyName,
                "givenName": givenName
            },
            "userName": email,
            "emails": [
                {
                    "value": email,
                    "type": "work",
                    "primary": True
                }
            ]
        }
        response = self.api_client._post(self.api_client.rest_url + "/Users",
                                         data=json.dumps(userJson))
        return(response.json())

    def list(self):
        """ Lists all users (up to 300) in the workspace

        Returns:
            Response:
                JSON formatted blob of users
        """

        params = {'count': 300}
        response = self.api_client._get(self.api_client.rest_url + "/Users", params=params)  # noqa: E501
        return(response.json())

    def find(self, searchParams):
        """ Searches Slack users for the included key that matches a value

        Inputs:
            A single entry sized dictionary that has one of the following keys:
                email,
                givenName,
                familyName,
                id
        Returns:
            A slack user json blob

        Raises Exceptions:
            UserNotFound:
                A use has not been found that matches the included requirements
            UnimplementedSearchMethod:
                The key does match one of the required values
        """
        for user in self.list()['Resources']:
            if 'email' in searchParams.keys():
                sEmail = None
                for email in user['emails']:
                    if email['value'] == searchParams['email']:
                        sEmail = email['value']
                        break

                if sEmail is not None:
                    return(user)
            elif 'givenName' in searchParams.keys() or 'familyName' in searchParams.keys():  # noqa: E501
                for (key, value) in searchParams.items():
                    if user['name'][key] == value:
                        return(user)
            elif 'id' in searchParams.keys():
                if user['id'] == searchParams['id']:
                    return(user)
            else:
                raise exceptions.UnimplementedSearchMethod()
        raise exceptions.UserNotFound()

    def deactivate(self, id):
        """ Deactivates a particular user using their email address

        Inputs:
            email

        Returns:
            Not sure yet
        """
        response = self.api_client._delete(self.api_client.rest_url + "/Users/{}".format(id))  # noqa: E501
        return(response)

    def list_inactive(self):
        """ Lists users who have been marked as inactive

        Inputs: None
        Returns: a list of json blobs from Slack
        """
        inactive_users = []
        for user in self.list()['Resources']:
            if user['active'] is False:
                inactive_users.append(user)

        return inactive_users
