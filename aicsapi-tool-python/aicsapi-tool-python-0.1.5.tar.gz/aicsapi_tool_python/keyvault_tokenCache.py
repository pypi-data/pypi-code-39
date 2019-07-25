import json
import os, time

CACHE_EXPIRE_TIME = 60 * 59

class TokenCache(object):
    ''' 
    Utility Class to cache credentials required by KeyVaultAuthentication
    ''' 

    def __init__(self, filepath):
        '''
        Creates instance with cache filepath
        '''
        self.filepath = filepath

    def valid(self):
        '''
        Checks the validity/existence of cache

        Returns
        -------
        bool
            Whether a valid cache is present
        '''
        self.delete_old()
        return os.path.exists( self.filepath )

    def delete_old(self):
        '''
        Deletes expired token cache
        '''

        if ( os.path.exists( self.filepath ) and
             (time.time() - os.stat( self.filepath ).st_mtime) > CACHE_EXPIRE_TIME ):
            print ('Cache expired')
            print ('--------------------')
            print ('Now:', time.time(), 'Cached:', os.stat( self.filepath ).st_mtime)
            os.remove( self.filepath )

    def save(self, token_tup):
        '''
        Saves token cache as a JSON file

        Parameters
        ----------
        token_tup : tuple
            contains (tokenType, accessToken) acquired via device-code login
        '''
        token = { 'tokenType': token_tup[0],
                  'accessToken': token_tup[1] }
        with open(self.filepath, 'w') as json_fp:
            json.dump(token, json_fp)

    def load(self):
        '''
        Loads token cache for caller

        Returns
        -------
        dict
            contains credentials required by KeyVaultAuthentication
        '''
        
        return json.load( open(self.filepath) )
