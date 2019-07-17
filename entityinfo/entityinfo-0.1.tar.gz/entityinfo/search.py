import json
import numpy as np
import pandas as pd
import requests


class gs:
    url_part1 = "https://www.googleapis.com/customsearch/v1?key="
    key = "AIzaSyDBWxwAqAWVN_tATgXYDMW23a8vmqVkfbI"
    cse = '&cx=008704893209736821023:mvugnwefaea&q='
    suggestion = 'None'

    def __init__(self, search):
        self.search = search
        self.url = gs.url_part1 + gs.key + gs.cse + self.search
        gs.suggestion = 'None'

    def get_suggestion(self):
        r = requests.get(url=self.url)
        r_json = r.json()
        if 'spelling' in r_json.keys():
            gs.suggestion = r_json.get('spelling').get('correctedQuery')
        return gs.suggestion

    def get_sr(self):
        '''Extract search result from Google'''
        r = requests.get(url=self.url)
        r_json = r.json()
        suggestion = gs(self.search).get_suggestion()
        if (suggestion not in 'None') and (gs.suggestion[0] == self.search[0]):
            correct_spelling = gs.suggestion
            self.url = gs.url_part1 + gs.key + gs.cse + correct_spelling
            r = requests.get(self.url)  # requesting information
            r_json = r.json()
            return r_json
        return r_json

    def get_sr_df(self):
        r_json = gs(self.search).get_sr()
        r_json_str = json.dumps(r_json)
        sr_df = pd.DataFrame({'search': [self.search],
                              'suggestion': gs.suggestion,
                              'search_result': [r_json_str]})
        return sr_df
