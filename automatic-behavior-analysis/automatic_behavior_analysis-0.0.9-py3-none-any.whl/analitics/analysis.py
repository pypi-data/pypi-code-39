#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Wed Oct 31 21:25:09 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

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

Created on Wed Oct 31 21:25:09 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Wed Oct 31 21:25:09 2018'
__version__ = '0.1'

import sys
import math
import numpy as np
import cv2
import analitics.annotation as annotation
from analitics.annotation import Video_Annotation
from util.video_tools import show_image
import pdb

def dog_ann2pos(dog_annotation):
    return (dog_annotation[annotation.KEY_X1],
            dog_annotation[annotation.KEY_X2],
            dog_annotation[annotation.KEY_Y1],
            dog_annotation[annotation.KEY_Y2])


def calc_box_center(box_pos):
    return ((box_pos[0]+box_pos[1])/2,
            (box_pos[2]+box_pos[3])/2 )

def preprocess_video_annotation(video_annotation,
                                restore_sleep=3,
                                restore_window=3):
    '''
        Предварительная обработка видео
        Этапы:
            1. Восстановление пропущенных кадров (аппроксимация положения boxes)
            2. Вычисление центров boxes
            3. Фильтрация высокочастотных движений boxes
            4. Коррекция индексов собак (по положенияю boxes)
            5. Коррекция ложноотрицательных sleep при наличии положительных
            срабатываний (заполнение состоянием расстояния между положительными
            вердиктами до порога)
    '''
    if not isinstance(video_annotation, Video_Annotation):
        raise TypeError('video_annotation should be Video_Annotation. \
                        But the type is: {}'.format(type(video_annotation)))
    frames = video_annotation.get_list_frames()

    #  Коррекция индексов собак
    last_dogs_pos = {}
    for i in range(len(frames)):
        # Добавляем новых собачек, если есть
        # Получаем центры boxes на текущем кадре для собачек
        cur_dog_position = {}

        for idx, dog_ann in enumerate(frames[i][annotation.KEY_DOGS]):
            if last_dogs_pos.get(idx) is None:
                last_dogs_pos[idx] = calc_box_center(dog_ann2pos(dog_ann))
            cur_dog_position[idx] = calc_box_center(dog_ann2pos(dog_ann))

        # Исправляем соответствие координат собакам
        for idx_i, dog_pos_i in last_dogs_pos.items():
            min_dist = sys.float_info.max
            min_dist_idx = None
            for idx_j, dog_pos_j in cur_dog_position.items():
                dist = math.sqrt((dog_pos_i[0] - dog_pos_j[0])**2 +
                                    (dog_pos_i[1] - dog_pos_j[1])**2)
                if dist < min_dist:
                    min_dist = dist
                    min_dist_idx = idx_j
            objects = frames[i][annotation.KEY_DOGS]
            # TODO: check if this fix works correctly with the logic
            if min_dist_idx != idx_i and idx_i < len(objects) and idx_j < len(objects):
                buf = objects[idx_i]
                objects[idx_i] = objects[idx_j]
                objects[idx_j] = buf

        # Сохраняем новые координаты собак
        for idx, dog_ann in enumerate(frames[i][annotation.KEY_DOGS]):
            last_dogs_pos[idx] = calc_box_center(dog_ann2pos(dog_ann))

        # Удаляем исчезнувших собак
        to_remove = set()
        for k in last_dogs_pos.keys():
            if k not in range(len(frames[i][annotation.KEY_DOGS])):
                to_remove.add(k)
        for k in to_remove:
            del last_dogs_pos[k]

    # Фильтрация ложноотрицательных вердиктов по сну
    last_dogs_state = {}
    last_dogs_state_counter = {}
    for i in range(len(frames)):
        for idx, dog_ann in enumerate(frames[i][annotation.KEY_DOGS]):
            # Добавляем собачек и счечик отрицательных вердиктов
            if last_dogs_state.get(idx) is None:
                last_dogs_state[idx] = dog_ann[annotation.KEY_STATE]
                last_dogs_state_counter[idx] = 0

            if dog_ann[annotation.KEY_STATE] == 'sleep':
                last_dogs_state_counter[idx] = 0
                last_dogs_state[idx] == 'sleep'
            elif (last_dogs_state[idx] == 'awake'
                    and last_dogs_state_counter[idx] < restore_sleep):
                dog_ann[annotation.KEY_STATE] = 'sleep'
                last_dogs_state_counter[idx] += 1
                last_dogs_state[idx] == 'awake'
    return video_annotation


class RT_annotation_processing():
    def __init__(self, 
                max_memory_len=100, 
                restore_sleep=3,
                object_count_limit=10):
        """ """
        self._max_memory_len = max_memory_len
        self._object_count_limit = object_count_limit
        self.restore_sleep=restore_sleep
        self.frames = []
        self.last_dogs_pos = {}
        self.last_dogs_coord = {}
        self.last_dogs_state = {}
        self.last_dogs_state_counter = {}

    @staticmethod
    def low_pass_filter(data):
        '''
        data -- list
        return -- last point
        '''
        order = 5
        order = min((order, len(data)))
        r = 0
        for i in range(order):
            r += 1/order * data[-(i+1)]
        return r

    def process_frame_annotation(self, frame_annotation):
        self.frames.append(frame_annotation)

        # Добавляем новых собачек, если есть
        # Получаем центры boxes на текущем кадре для собачек
        cur_dog_position = {}
        ids4delete = []

        for i, dog_ann in enumerate(self.frames[-1][annotation.KEY_DOGS]):
            idx = dog_ann['id']
            #if self.last_dogs_pos.get(idx) is None:
            #    self.last_dogs_pos[idx] = calc_box_center(dog_ann2pos(dog_ann))
            cur_dog_position[idx] = calc_box_center(dog_ann2pos(dog_ann))

        # Удаление пересекающихся рамок
        for i, dog_ann in enumerate(self.frames[-1][annotation.KEY_DOGS]):
            idx = dog_ann['id']
            for idy in list(cur_dog_position):
                dist = math.sqrt((cur_dog_position[idy][0]-cur_dog_position[idx][0])**2 +
                                    (cur_dog_position[idy][1]-cur_dog_position[idx][1])**2)
                if dist < 0.09 and idx != idy and not(idy in ids4delete):
                    if (self.frames[-1][annotation.KEY_DOGS][idx]['rate'] > self.frames[-1][annotation.KEY_DOGS][idy]['rate']):
                        ids4delete.append(idy)
                    else:
                        ids4delete.append(idx)

        for i in reversed(ids4delete):
            try:
                d = self.frames[-1][annotation.KEY_DOGS].pop(i)
                self.last_dogs_pos.pop(d['id'])
            except IndexError:
                pass
            except KeyError:
                pass
        # Исправляем соответствие координат собакам
        for dog_ann in self.frames[-1][annotation.KEY_DOGS]:
            min_dist = sys.float_info.max
            min_dist_idx = dog_ann['id']
            dog_pos_j = calc_box_center(dog_ann2pos(dog_ann))
            for idx_last, dog_pos_last in self.last_dogs_pos.items():
                dist = math.sqrt((dog_pos_last[0] - dog_pos_j[0])**2 +
                                 (dog_pos_last[1] - dog_pos_j[1])**2)
                if dist <= min_dist:
                    min_dist = dist
                    min_dist_idx = idx_last
            if min_dist_idx != dog_ann['id'] and dist<0.1: #Костыль, чтобы не детектить ближайших к новому объекту
                for k in range(len(self.frames[-1][annotation.KEY_DOGS])):#TODO: Сменить тип с массива на Map
                    if self.frames[-1][annotation.KEY_DOGS][k]['id'] == dog_ann['id']:
                        obj1_ind = k
                    elif self.frames[-1][annotation.KEY_DOGS][k]['id'] == min_dist_idx:
                        obj2_ind = k
                buff = self.frames[-1][annotation.KEY_DOGS][obj1_ind]['id']
                self.frames[-1][annotation.KEY_DOGS][obj1_ind]['id'] = min_dist_idx
                try:
                    self.frames[-1][annotation.KEY_DOGS][obj2_ind]['id'] = buff
                except UnboundLocalError: # Если на текущем кадре нет объекта с распознаным номером
                    pass

        # Сохраняем новые координаты собак
        self.last_dogs_pos = {}
        for dog_ann in self.frames[-1][annotation.KEY_DOGS]:
            self.last_dogs_pos[dog_ann['id']] = calc_box_center(dog_ann2pos(dog_ann))

        # Фильтрация вердиктов по сну
        for dog_ann in self.frames[-1][annotation.KEY_DOGS]:
            # Добавляем собачек и счечик отрицательных вердиктов
            if self.last_dogs_state.get(dog_ann['id']) is None:
                self.last_dogs_state[dog_ann['id']] = dog_ann[annotation.KEY_STATE]
                self.last_dogs_state_counter[dog_ann['id']] = 0

            if dog_ann[annotation.KEY_STATE] != self.last_dogs_state[dog_ann['id']]:
                self.last_dogs_state_counter[dog_ann['id']] += 1
                if self.last_dogs_state_counter[dog_ann['id']] < self.restore_sleep:
                    dog_ann[annotation.KEY_STATE] = self.last_dogs_state[dog_ann['id']]
                else:
                    self.last_dogs_state_counter[dog_ann['id']] = 0
                    self.last_dogs_state[dog_ann['id']] = dog_ann[annotation.KEY_STATE]

        # Фильтрация координат собак

        for i, dog_ann in enumerate(self.frames[-1][annotation.KEY_DOGS]):
            idx = dog_ann['id']
            if self.last_dogs_coord.get(idx) is None:
                self.last_dogs_coord[idx] = {}
                self.last_dogs_coord[idx][annotation.KEY_X1] = []
                self.last_dogs_coord[idx][annotation.KEY_X2] = []
                self.last_dogs_coord[idx][annotation.KEY_Y1] = []
                self.last_dogs_coord[idx][annotation.KEY_Y2] = []
            self.last_dogs_coord[idx][annotation.KEY_X1].append(dog_ann[annotation.KEY_X1])
            self.last_dogs_coord[idx][annotation.KEY_X2].append(dog_ann[annotation.KEY_X2])
            self.last_dogs_coord[idx][annotation.KEY_Y1].append(dog_ann[annotation.KEY_Y1])
            self.last_dogs_coord[idx][annotation.KEY_Y2].append(dog_ann[annotation.KEY_Y2])

            dog_ann[annotation.KEY_X1] = RT_annotation_processing.low_pass_filter(self.last_dogs_coord[idx][annotation.KEY_X1])
            dog_ann[annotation.KEY_X2] = RT_annotation_processing.low_pass_filter(self.last_dogs_coord[idx][annotation.KEY_X2])
            dog_ann[annotation.KEY_Y1] = RT_annotation_processing.low_pass_filter(self.last_dogs_coord[idx][annotation.KEY_Y1])
            dog_ann[annotation.KEY_Y2] = RT_annotation_processing.low_pass_filter(self.last_dogs_coord[idx][annotation.KEY_Y2])
            # Delete old points
            if len(self.last_dogs_coord[idx]) > self._max_memory_len:
                self.last_dogs_coord[idx] = self.last_dogs_coord[idx][-self._max_memory_len:]

        # Удаление объектов свыше лимита
        while len(self.frames[-1][annotation.KEY_DOGS]) > self._object_count_limit:
            min_rate_index = -1
            min_rate_value = 1
            for i, dog_ann in enumerate(self.frames[-1][annotation.KEY_DOGS]):
                if dog_ann[annotation.KEY_RATE] < min_rate_value:
                    min_rate_value = dog_ann[annotation.KEY_RATE]
                    min_rate_index = i
            self.frames[-1][annotation.KEY_DOGS].pop(min_rate_index)
            
        # Удаляем старые данные
        if len(self.frames) > self._max_memory_len:
            self.frames = self.frames[-self._max_memory_len:]
        return self.frames[-1]

class RT_frame_processing():
    def __init__(self, 
                max_memory_len=100, 
                sleep_thr=0.5, 
                move_thr=0.10, 
                state_change_delay=5,
                object_count_limit=10,
                verbose=False,
                log2file=False):
        self._verbose = verbose
        self._log2file = log2file
        self._max_memory_len = max_memory_len
        self._sleep_thr = sleep_thr
        self._object_count_limit = object_count_limit
        self.move_thr = move_thr
        self.im_frames = []
        self.annotation_processor = RT_annotation_processing(max_memory_len, 
                    restore_sleep=state_change_delay,
                    object_count_limit=object_count_limit)

    def process_frame(self, np_frame, fr_annotation):
        annot = fr_annotation
        self.im_frames.append(np_frame)
        if len(self.im_frames) > self._max_memory_len:
            self.im_frames = self.im_frames[-self._max_memory_len:]

        for dog in annot[annotation.KEY_DOGS]:
            try:
                if self._log2file:
                    with open("raw.csv", "a") as myfile:
                        myfile.write(str(dog[annotation.KEY_X1]) + ";" +
                                    str(dog[annotation.KEY_X2]) + ";" +
                                    str(dog[annotation.KEY_Y1]) + ";" +
                                    str(dog[annotation.KEY_Y2]) + "\n")
                is_not_sleep, moving_rate = self.analise_dog((dog[annotation.KEY_X1],
                                                    dog[annotation.KEY_X2],
                                                    dog[annotation.KEY_Y1],
                                                    dog[annotation.KEY_Y2]))
                dog["moving_rate"] = moving_rate
                if is_not_sleep:
                    dog[annotation.KEY_STATE] = "awake"
            except IndexError as identifier:
                pass
        annot = self.annotation_processor.process_frame_annotation(fr_annotation)

        for dog in annot[annotation.KEY_DOGS]:
            if self._log2file:
                with open("processed.csv", "a") as myfile:
                    myfile.write(str(dog[annotation.KEY_X1]) + ";" +
                                str(dog[annotation.KEY_X2]) + ";" +
                                str(dog[annotation.KEY_Y1]) + ";" +
                                str(dog[annotation.KEY_Y2]) + "\n")

        return annot

    def analyse_moving(self, img_1, img_2, moving_threshold = 0.03):
        '''
        moving_threshold -- float [0 ... 1]
        '''
        # Convert to B&W image
        cur_frame = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
        prev_frame = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)

        # Blur cropped B&W image
        cur_frame = cv2.GaussianBlur(cur_frame, (21, 21), 0)
        prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)

        frameDelta = cv2.absdiff(prev_frame, cur_frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # pdb.set_trace()
        try:
            cnts, _ = res
        except ValueError:
            _, cnts, _ = res


        # show_image(thresh)

        is_moving = False

        image_area = img_1.shape[0] * img_1.shape[1]

        # loop over the contours
        mr = 0
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c)/image_area > moving_threshold:
                mr += cv2.contourArea(c)/image_area
                is_moving = True
                print(cv2.contourArea(c)/image_area, moving_threshold)
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            #(x, y, w, h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return is_moving, mr

    def analise_dog(self, dog_pos):
        (x1, x2, y1, y2) = dog_pos

        # Get and Crop dog
        cur_frame = self.im_frames[-1]
        size = cur_frame.shape
        x1 = int(x1 * size[1])
        x2 = int(x2 * size[1])
        y1 = int(y1 * size[0])
        y2 = int(y2 * size[0])

        cur_frame = cur_frame[y1:y2, x1:x2]
        prev_frame = self.im_frames[-2]
        prev_frame = prev_frame[y1:y2, x1:x2]

        return self.analyse_moving(prev_frame, cur_frame, self.move_thr)
