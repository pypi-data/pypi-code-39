"""
Created by 復讐者 on 2/15/19
"""
__author__ = '復讐者'

import json
from CourseZero.FileSystemTools import getSystemRoot
from CourseZero import environment as env


def load_campus_id_data(data_json_path=env.DEFAULT_CSU_ID_FILE):
    with open( data_json_path, 'r' ) as fpp:
        return json.load(fpp)

# campus_ids = load_campus_id_data(csu_id_data)
# csu_names = [c['name'] for c in campus_ids]

if __name__ == '__main__':
    pass