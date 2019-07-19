from .api_module import ApiModule


class Polls(ApiModule):
    __slots__ = ()

    def addVote(self, poll_id, answer_ids, owner_id=None, id_board=0):
        return self._get_response(locals())

    def crate(self,
              question=None,
              is_anonymous=0,
              is_multiple=None,
              end_date=None,
              owner_id=None,
              add_answers=None,
              photo_id=None,
              background_id=None):
        return self._get_response(locals())

    def deleteVote(self, poll_id, answer_id, owner_id=None, is_board=None):
        return self._get_response(locals())

    def edit(self,
             poll_id,
             owner_id=None,
             question=None,
             add_answers=None,
             edit_answers=None,
             delete_answers=None,
             end_date=None,
             photo_id=None,
             background_id=None):
        return self._get_response(locals())

    def getBackgrounds(self):
        return self._get_response(locals())

    def getById(self,
                poll_id,
                owner_id=None,
                is_board=0,
                extended=None,
                fields_count=3,
                fields=None,
                name_case='nom'):
        return self._get_response(locals())

    def getPhotoUploadServer(self, owner_id=None):
        return self._get_response(locals())

    def getVoters(self,
                  poll_id,
                  answer_ids,
                  owner_id=None,
                  friends_only=0,
                  offset=0,
                  count=10,
                  fields=None,
                  name_case='nom'):
        return self._get_response(locals())

    def savePhoto(self, photo, _hash):
        return self._get_response(locals())
