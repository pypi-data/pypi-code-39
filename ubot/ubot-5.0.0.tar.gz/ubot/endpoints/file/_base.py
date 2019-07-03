from abc import ABC

from libmediainfo_cffi import MediaInfo

from ._attributes import attributes
from ..._utils.casing import camel_to_snake
from ..._utils.multipart_encoder import MultipartEncoder
from ...settings import json_lib as json


cache = {}


class FileMixin(ABC):
    __slots__ = []
    file_type: str
    attributes: dict

    args: dict
    value: str or list
    is_data: bool
    use_cache: bool


class File(ABC):
    __slots__ = ['file_type', 'attributes', 'args', 'value', 'is_data', 'use_cache']

    def __init__(self, file, is_path=True):
        """Generic File class, supports automatic metadata reading via MediaInfo bindings and caching

        :param file: a path (default) or a valid string recognizable by the Telegram endpoint (an url or a file id)
        :param is_path: whether file is a path (default) or anything else
        """

        # cache is a dict {file_path: file_id} and should be updated with the trigger callback
        classname = self.__class__.__name__
        self.file_type = camel_to_snake(classname)
        self.args = {}
        self.file = file
        self.attributes = {}
        self.use_cache = False

        # if we received a path we first check we have the file inside the cache dict
        # if we do then we treat this as a File with "is_path" set to false and we use the file_id we've found as
        # else we store encode the file as multipart/form-data
        if is_path is True:
            file_id = cache.get(self.file)
            if file_id is not None:
                self.is_data = False
                self.value = file_id
            else:
                self.is_data = True
                self.value = [MultipartEncoder.encode_file(self.file_type, self.file)]
        else:
            self.is_data = False
            self.value = self.file

    def read_metadata(self):
        """Read metadata from the file (if it's a file)"""

        if not self.is_data or self.attributes:
            return self

        data = MediaInfo.read_metadata(self.file, Inform='JSON')

        data = json.loads(data)
        data_dict = {}

        # redrder the data to avoid O(tracks number) behavior while checking for tracks of a given type
        # also we use only the first track found, you can override this method if this doesn't work for you
        for track in data['media']['track']:
            _type = track['@type']

            if data_dict.get(_type) is None:
                data_dict[_type] = track

        for attribute, _type, key in attributes[self.file_type]:
            if callable(_type):
                attribute_value = _type(data)
            else:
                track = data_dict.get(_type)
                if track is None:
                    continue

                attribute_value = track.get(key)

            if attribute_value is None:
                continue

            self.attributes[attribute] = attribute_value

        return self

    def with_cache(self):
        """Check if a file_id can be used instead of a multipart/form-data request"""

        if not self.is_data:
            return self

        if not self.use_cache:
            self.use_cache = True
            return self

        file_id = cache.get(self.file)

        if file_id is not None:
            self.is_data = False
            self.value = file_id
            self.attributes = {}

        return self

    @staticmethod
    def _get_file_id(response):
        """If the telegram response is (for example) an array or a map, here you can return the correct entry to the
        update_cache function
        """

        return response

    def update_cache(self, response, index=None):
        """Updates the object cache with the file ids"""

        # the index param is used for media groups
        # add correct file type automatically or ask the user to pass the type using bot.find_update_type

        file_id = cache.get(self.file)
        if file_id is None:
            response = response['result']
            if index is not None:
                response = response[index][self.file_type]
            else:
                response = response[self.file_type]

            cache[self.file] = self._get_file_id(response)['file_id']
