#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Mon Nov 05 19:14:09 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Mon Nov 05 19:14:09 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Mon Nov 05 19:14:09 2018'
__version__ = '0.1'

import os
import json
import saver

KEY_VIDEO_NAME = "video_name"
KEY_SUMMARY = "summary"
KEY_FRAMES_ANNOTATIONS = "frame_annotations"
KEY_DOGS = "dogs"
KEY_RATE = "rate"
KEY_ID = "id"
KEY_X1 = "x1"
KEY_X2 = "x2"
KEY_Y1 = "y1"
KEY_Y2 = "y2"
KEY_STATE = "state"
KEY_CHILDREN = "children"
KEY_CATEGORY = "category"
'''
JSON_EXAMPLE
{
"video_name":"video.mp4",
"summary":"",
"frame_annotations":
    {
        "1":{
            "dogs":{
                "0":{
                    "rate":0.6,
                    "x1": 0.5,
                    "y1": 0.5,
                    "x2": 0.6,
                    "y2": 0.6,
                    "state": "sleep"
                },
                "1":{
                    "rate":0.8,
                    "x1": 0.2,
                    "y1": 0.2,
                    "x2": 0.3,
                    "y2": 0.3,
                    "state": "awake"
                }
            }
        },
        "2":{
            "dogs":{
                "0":{
                    "rate":0.6,
                    "x1": 0.5,
                    "y1": 0.5,
                    "x2": 0.6,
                    "y2": 0.6,
                    "state": "sleep"
                },
                "1":{
                    "rate":0.8,
                    "x1": 0.2,
                    "y1": 0.2,
                    "x2": 0.3,
                    "y2": 0.3,
                    "state": "awake"
                }
            }
        }
    }
}
'''

class Video_Annotation():
    """
    Класс для реализации аннотации видео.
    """
    def __init__(self, video_name = None, src_file = None):
        """
        При создании объекта аннотации возможна ее автоматическа загрузка из
        json файла. При этом имя файла, переданное программно имеет приоритет
        перед сохраненным в файле.
        """

        self.annotation = {}
        self.annotation[KEY_FRAMES_ANNOTATIONS] = {}
        if src_file is not None:
            self.annotation = saver.load_annotation(src_file)
        if video_name is not None:
            self.annotation[KEY_VIDEO_NAME] = video_name

    def annotate_dog(self, frame_id, **kwargs):
        self._annotate_dog(frame_id, kwargs)

    # Same as annotate_dog, but without using **kwargs
    def _annotate_dog(self, frame_id, entry):
        """
        Записать аннотацию отдельного фрейма
        entry:
            id,
            rate,
            x1,
            x2,
            y1,
            y2,
            state
        """
        dog_annotation = {}
        dog_annotation[KEY_ID] = entry['id']
        dog_annotation[KEY_RATE] = entry['rate']
        dog_annotation[KEY_X1] = entry['x1']
        dog_annotation[KEY_X2] = entry['x2']
        dog_annotation[KEY_Y1] = entry['y1']
        dog_annotation[KEY_Y2] = entry['y2']
        dog_annotation[KEY_STATE] = entry['state']
        dog_annotation[KEY_CHILDREN] = entry.get('children')
        dog_annotation[KEY_CATEGORY] = entry['category']

        if self.annotation[KEY_FRAMES_ANNOTATIONS].get(frame_id) is None:
            self.annotation[KEY_FRAMES_ANNOTATIONS][frame_id] = {}
        if self.annotation[KEY_FRAMES_ANNOTATIONS][frame_id].get(KEY_DOGS) is None:
            self.annotation[KEY_FRAMES_ANNOTATIONS][frame_id][KEY_DOGS] = []

        self.annotation[KEY_FRAMES_ANNOTATIONS][frame_id][KEY_DOGS].insert(entry['id'], dog_annotation)

    def frame_annotations(self):
        """
        Упорядоченный по ключу генератор, возвращающий фреймы
        """
        for idx in sorted(self.annotation[KEY_FRAMES_ANNOTATIONS].keys()):
            yield (idx, self.annotation[KEY_FRAMES_ANNOTATIONS][idx])

    def get_list_frames(self):
        frames = []
        for _, frame in self.frame_annotations():
            frames.append(frame)
        return frames

    def get_frame_annotation(self, frame_id):
        return self.annotation[KEY_FRAMES_ANNOTATIONS][frame_id]

    def set_frame_annotations(self, data):
        for index, entry in data.items():
            for item in entry['dogs']:
                self._annotate_dog(index, item)

    def get_frame_count(self):
        return len(self.annotation[KEY_FRAMES_ANNOTATIONS])

    def save_annotation(self, file_name, **kwargs):
        """
        Сохранение аннотации в файл
        """
        saver.save_annotation(file_name, self.annotation, **kwargs)
