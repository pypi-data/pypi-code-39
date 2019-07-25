

class Rules(object):
    """
    This class allows you to interact with and search mailboxes using Microsoft Graph API.  It's parent class is GraphConnector which handles all authentication.
    """
    def __init__(self, graphConnector, userPrincipalName='me'):
        """The Search class allows you to:
           * Create a new Search
           * Update an existing Search
           * Retrieve messages identified during a search
           * Find search folders on mailboxes
           * Delete a search
        
        Args:
            graphConnector (GraphConnector): A generated GraphConnector object
            includeNestedFolders (bool, optional): When creating a search you can define if you want to search all nested folders or not. Defaults to True.
            userPrincipalName (str, optional): Defaults to the current user, but can be any user defined or provided in this parameter. Defaults to 'me'.
        """
        self.connector = graphConnector
        if userPrincipalName is not 'me':
            self.user = 'users/%s' % userPrincipalName
        else:
            self.user = userPrincipalName

    def get(self):
        uri = '%s/mailFolders/inbox/messageRules' % (self.user)
        return self.connector.invoke('GET', uri).json()

