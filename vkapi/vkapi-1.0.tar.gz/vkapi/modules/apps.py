from .api_module import ApiModule


class Apps(ApiModule):
    __slots__ = ()

    def deleteAppRequests(self):
        return self._get_response(locals())

    def get(self,
            app_id=None,
            app_ids=None,
            platform='web',
            extended=0,
            return_friends=0,
            fields=None,
            name_case='nom'):
        return self._get_response(locals())

    def getCatalog(self,
                   sort=None,
                   offset=None,
                   count=None,
                   platform='web',
                   extended=None,
                   return_friends=0,
                   fields=None,
                   name_case='nom',
                   q=None,
                   genre_id=None,
                   _filter=None):
        return self._get_response(locals())

    def getFriendsList(self, extended=0, count=20, offset=0, _type='invite', fields=None):
        return self._get_response(locals())

    def getLeaderboard(self, _type, _global=1, extended=0):
        return self._get_response(locals())

    def getScopes(self, _type='user'):
        return self._get_response(locals())

    def getScore(self, user_id):
        return self._get_response(locals())

    def sendRequest(self,
                    user_id,
                    text=None,
                    _type='request',
                    name=None,
                    key=None,
                    separate=0):
        return self._get_response(locals())
