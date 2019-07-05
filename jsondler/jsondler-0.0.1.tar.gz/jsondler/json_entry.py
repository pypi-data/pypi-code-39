from functools import reduce
from operator import getitem
from abc import ABCMeta, abstractmethod


class JsonEntry(object, metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def attr_scheme(cls):
        """
        json scheme (the keys must match attribute names defined in __init__)
        CAUTION: if attribute is not defined in __init__ method (sublevel key in a json)
        don't include it to the result dict
        :return: {attr_name: (path, in, json, entry,), ...}
        """
        return dict()

    def get_json(self):
        res_json = dict()
        for attr in self.attr_scheme():
            keys = self.attr_scheme()[attr]
            keys_l = len(keys)
            for i in range(keys_l):
                if i > 0:
                    if i == keys_l - 1:
                        sub_res_json = reduce(getitem, keys[:i], res_json)
                        sub_res_json[keys[i]] = self.__dict__[attr]
                    else:
                        sub_res_json = reduce(getitem, keys[:i], res_json)
                        if keys[i] not in sub_res_json:
                            sub_res_json[keys[i]] = dict()
                else:
                    if i == keys_l - 1:
                        res_json[keys[i]] = self.__dict__[attr]
                    elif keys[i] not in res_json:
                        res_json[keys[i]] = dict()
            keys = None
        return res_json

    @classmethod
    def load_from_dict(cls, in_dict):
        json_entry = cls()
        for attr in cls.attr_scheme():
            try:
                json_entry.__dict__[attr] = reduce(getitem, cls.attr_scheme()[attr], in_dict)
            except KeyError:
                print("WARNING: the path '%s' is absent in the input dict - cannot find a value for '%s'" %
                      (str(cls.attr_scheme()[attr]), attr))
                continue
        return json_entry
