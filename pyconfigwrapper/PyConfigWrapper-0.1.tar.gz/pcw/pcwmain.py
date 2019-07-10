import json
import os

# Main Class for Config connection #
class Config(object):
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.__config_dict = {}
        self.refresh()
    
    def refresh(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as fp:
                fp.write("{}")
                self.__config_dict = {}
        else:
            with open(self.filename, 'r', encoding='utf-8') as fp:
                self.__config_dict = json.load(fp)

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as fp:
            json.dump(self.__config_dict, fp, indent=4, ensure_ascii=False)
            fp.truncate()

    def __getitem__(self, key):
        return self.__config_dict.get(key)
    
    def __setitem__(self, key, value):
        self.__config_dict[key] = value
    
    def __delitem__(self, key):
        del self.__config_dict[key]

    def __len__(self):
        return len(self.__config_dict)

    def __contains__(self, item):
        return True if self[item] else False