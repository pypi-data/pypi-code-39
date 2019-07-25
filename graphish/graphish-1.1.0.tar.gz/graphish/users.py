

class Users(object):
    """
    This class allows you to retrieve all users within your organization.  Your Azure AD application will need to have the User.Read.All permissions granted for this application.
    """
    def __init__(self, graphConnector):
        """The Users class allows you to:
           * Get all email address within your Azure tenant
        
        Args:
            graphConnector (GraphConnector): A generated GraphConnector object
        """
        self.connector = graphConnector

    @property
    def get(self):
        return_list = []
        uri = 'users'
        for user in self.connector.invoke('GET', uri).json()['value']:
            # Adding logic hear to attempt to catch mailboxes not in Exchange Online
            if user['userPrincipalName'] == user['mail']:
                return_list.append(user['userPrincipalName'])
        return return_list