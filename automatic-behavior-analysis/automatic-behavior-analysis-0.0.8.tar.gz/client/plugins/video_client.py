#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Mon Oct 29 19:05:00 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Created on Mon Oct 29 19:05:00 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'Proprietary'
__date__ = 'Mon Oct 29 19:00:00 2018'
__version__ = '0.2'

import os
import cv2
import json
import numpy as np
from pprint import pprint
import pdb

from plugins.base_plugin import Base_Plugin
from util.protocol import make_request
from util.digNetwork.tcpclient import TcpClient
from util.websocket_client import WebSocketClient
from util.object_dict import ObjectDict
from analitics.annotation import Video_Annotation
from analitics.analysis import preprocess_video_annotation, RT_frame_processing
from analitics.summary import summarize_video_annotation
from analitics.saver import save_annotation, FrameSaver
from util.video_tools import FrameDecorator, VideoSaver, show_image

JSON_EXAMPLE = (
        '{"dogs": \
[{"id": 0, "rate":0.6, "x1": 0.5, "y1": 0.5, "x2": 0.6, "y2": 0.6, "state": "sleep"}, \
 {"id": 1, "rate":0.8, "x1": 0.2, "y1": 0.2, "x2": 0.3, "y2": 0.3, "state": "awake"}]}')

class Video_Client(Base_Plugin):
    def __init__(self, event_handler, config):
        """
        EventHandler interface:
        - handle_error(error: Exception)
        - received_ping_reply(response: dict{message: str})
        - set_image(image: cv2.Image, frame_index: int)
        - video_started(video_params: dict{width: int, height: int, frame_count: int, filename: str}, first_frame: cv2.Image)
        - server_connected(hostname: str, port: int)
        - after(ms: int, func: function, *args: ...)
        - upload_started(filename: str, total: int)
        - upload_progress(filename: str, completed: int, total: int)
        - upload_finished(filename: str, success: bool)
        """
        self._config = config
        self._event_handler = event_handler
        self._response_cache = {}
        self._image = None
        self._max_scale = 1.0
        # self._max_scale = 0.98
        self._image_scale = self._max_scale
        self._vidcap = None
        self._connection = None
        self._upload_file = None
        self._upload_filename = ''
        self._upload_buffer_size = config.upload_buffer_max_size
        self._upload_size = 0
        self._frame_decorator = FrameDecorator(config)
        self._frame_saver = FrameSaver(config)
        self._request_postprocessor = None
        self._rt_processing_enabled = config.detect_motion
        self._inner_detection_enabled = config.inner_detection
        self._saving_output_video = False
        self._video_saver = None
        self._processing_mode = False
        self._processing_mode_original_frame = 0
        self._processing_mode_should_finish = False
        self._send_grayscale = config.get('send_grayscale', False)
        self._object_names = {}

    def run(self):
        return

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

        if self._video_saver is not None:
            self._video_saver.close()

    def start(self, ip, port, server_type):
        try:
            if server_type == 'tcp':
                self._connection = TcpClient(ip, port, self._event_handler.server_connected, self.on_new_message, buffer_size=self._config.tcp_client_buffer_size)
            elif server_type == 'websocket':
                self._connection = WebSocketClient(ip, port, self._event_handler.server_connected, self.on_new_message)
            else:
                raise RuntimeError("Invalid server type: {}".format(server_type))
            self._connection.start()
            self.reset_cache()
        except Exception as ex:
            self._event_handler.handle_error(ex)

    def connect(self, ip, port, server_type):
        self.close()
        self.start(ip, port, server_type)

    def send_ping(self):
        self._connection.send(make_request({ 'command': 'ping' }))

    def update_cache(self, index, response):
        if 'frame_index' not in response:
            # response = dict(response)
            response['frame_index'] = index
        self._response_cache[index] = response

    def get_cached_item(self, index):
        return self._response_cache.get(index)

    def reset_cache(self):
        self._response_cache = {}

    def request_upload(self):
        self._upload_file = file = open(self._video_path, 'rb')
        self._upload_filename = filename = os.path.basename(self._video_path)
        self._upload_size = size = file.seek(0, 2)
        file.seek(0, 0)

        self._connection.send(make_request({
            'command': 'upload_init',
            'sha1sum': None,
            'size': size,
            'filename': filename,
            'max_buffer': self._config.upload_buffer_max_size
        }))

    def begin_upload(self, filename, buffer_size):
        self._upload_buffer_size = buffer_size
        self._event_handler.upload_started(filename, self._upload_size)
        self.continue_upload(False, filename, 0)

    def continue_upload(self, finished, filename, bytes_completed):
        self._event_handler.upload_progress(filename, bytes_completed, self._upload_size)

        if finished:
            self.end_upload(True, filename)
            return

        chunk = self._upload_file.read(self._upload_buffer_size)
        self._connection.send(make_request({ 'command': 'upload_append', 'filename': self._upload_filename }, chunk))

    def end_upload(self, status, filename):
        if self._upload_file:
            self._upload_file.close()
            self._upload_file = None
        self._upload_filename = None
        self._event_handler.upload_finished(filename, True)

    def cancel_upload(self):
        self.end_upload(self._upload_filename, False)

    def processing_mode_start(self):
        self._processing_mode = True
        self._processing_mode_should_finish = False
        self._processing_mode_original_frame = self._image_number
        self._event_handler.processing_mode_status(event='started')
        self.request_image(skip=0)

    def processing_mode_step(self, response, image, frame_index):
        if self._processing_mode_should_finish or frame_index >= self._frame_count - 1:
            self.processing_mode_end()
        else:
            self._event_handler.processing_mode_status(event='progress', frame_index=frame_index, frame_count=self._frame_count)
            self.request_image(skip=0)

    def processing_mode_end(self):
        self._processing_mode = False
        self._processing_mode_should_finish = False
        annotation = Video_Annotation(self._video_path)
        annotation.set_frame_annotations(self._response_cache)
        annotation = preprocess_video_annotation(annotation) # Fix sleep detection
        for index, frame in annotation.frame_annotations():
            self.update_cache(index, frame)
        self.seek_to_frame(self._processing_mode_original_frame)
        self._event_handler.processing_mode_status(event='done')

    def processing_mode_request_end(self):
        self._processing_mode_should_finish = True

    @staticmethod
    def resize_image(image, scale):
        im_height, im_width, *_ = image.shape
        return cv2.resize(image, (round(im_width * scale), round(im_height * scale)))

    def process_new_response(self, response, frame_index):
        # Предобработка response
        # print("image.shape:", self._image.shape)
        if self._rt_processing_enabled:
            response = self.get_request_postprocessor().process_frame(self._image, response)
        self.update_cache(frame_index, response)
        self.process_response(response, self._image, frame_index)

    def process_response(self, response, image, frame_index):
        if self._processing_mode:
            self.processing_mode_step(response, image, frame_index)
            return

        if self._saving_output_video:
            # The frames for saving the video output file have to be in a constant resolution, so we need to decorate twice
            image_copy = image.copy()
            self.save_output_video_frame(self._frame_decorator.decorate(image_copy, response, self._object_names, self._inner_detection_enabled))

        # print("Resizing image to scale: {}".format(self._image_scale))
        image = self.resize_image(image, self._image_scale)
        image = self._frame_decorator.decorate(image, response, self._object_names, self._inner_detection_enabled)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self._event_handler.set_image(image, frame_index)
        # print('Sending frame {} to client'.format(frame_index))

    def on_click(self, event):
        # Find current response
        print("Click event: {}".format(event))
        x, y = event.x, event.y
        response = self.get_cached_item(self._image_number)
        if not response: return
        nrm_x = x / self._display_width
        nrm_y = y / self._display_height
        for dog in response['dogs']:
            if dog['x1'] <= nrm_x and nrm_x <= dog['x2'] and dog['y1'] <= nrm_y and nrm_y <= dog['y2']:
                if event.num == 1:
                    dog['state'] = 'awake' if dog['state'] == 'sleep' else 'sleep'
                    self._event_handler.after(50, lambda: self.process_response(response, self._image, self._image_number))
                    return
                elif event.num == 3: # TODO: button 2 on Mac
                    self._event_handler.popup_object_menu(event, dog, self._image_number)

    def set_object_name(self, id, name, frame_index):
        print("set_object_name({}, {}, {})".format(id, name, frame_index))
        self._object_names[id] = name

    def get_request_postprocessor(self):
        if self._request_postprocessor is None:
            self._request_postprocessor = RT_frame_processing(
                max_memory_len=self._config.frame_processing_max_memory,
                sleep_thr=self._config.frame_processing_sleep_threshold)
        return self._request_postprocessor

    def calculate_scale(self, available_height):
        if not self._vidcap: return self._max_scale
        return max(0.1, min(self._max_scale, available_height / self._source_height))

    def update_scale(self, available_height):
        self._image_scale = scale = self.calculate_scale(available_height)
        self._display_width = round(self._source_width * scale)
        self._display_height = round(self._source_height * scale)

    def refresh_frame(self, available_height=None):
        if self._image is None: return
        if available_height is not None:
            self.update_scale(available_height)
        response = self.get_cached_item(self._image_number)
        image = self.resize_image(self._image, self._image_scale)
        if response is not None:
            image = self._frame_decorator.decorate(image, response, self._object_names)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self._event_handler.set_image(image, self._image_number, refresh=True)

    def set_source(self, video_path, available_height):
        """ Установка источника видео (пути к видеофайлу) """
        if not os.path.exists(video_path):
            raise RuntimeError("File does not exist: '{}'".format(video_path))

        if not os.path.isfile(video_path):
            raise RuntimeError("'{}' is not a file".format(video_path))

        vidcap = cv2.VideoCapture(video_path)
        if not vidcap.isOpened():
            raise RuntimeError("Invalid file format")

        self._vidcap = vidcap
        self._video_path = video_path
        self._image_number = 0
        self._source_width = int(self._vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._source_height = int(self._vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._display_width = self._source_width
        self._display_height = self._source_height
        self._frame_count = int(self._vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._object_names = {}
        self.reset_cache()

        self._request_postprocessor = None
        self._request_postprocessor = self.get_request_postprocessor()

        print("Opened video: {}".format(video_path))
        video_params = {
            'width': self._source_width,
            'height': self._source_height,
            'frame_count': self._frame_count,
            'filename': video_path
        }

        self.update_scale(available_height)
        first_frame = self.get_next_image(0) # Used for a preview when loading the video
        first_frame = self.resize_image(first_frame, self._image_scale)
        self.seek_to_frame(0) # Go back to beginning after reading one frame for the preview
        first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
        self._event_handler.video_started(video_params, first_frame)
        self.reset_output_video()

    def set_video_output_mode(self, state):
        self._saving_output_video = state

    def save_output_video_frame(self, frame):
        if self._video_saver is None:
            base_filename = os.path.splitext(os.path.basename(self._video_path))[0]
            self._video_saver = VideoSaver.create(self._config, None, base_filename, self._vidcap)
        self._video_saver.add_frame(frame)

    def reset_output_video(self):
        if self._video_saver is not None:
            self._video_saver.close()
            self._video_saver = None

    def load_image(self, raw_img):
        """ Получение изображения из сырых данных, полученных от сервера """
        nparr = np.fromstring(raw_img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img_np

    def get_next_image(self, skip):
        """ Получение следующего кадра из источника видео """
        if skip > 0:
            pos = round(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
            self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, pos + skip)
        frame_index = int(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
        success, image = self._vidcap.read()
        if not success: return None
        self._image_number = frame_index
        self._image = image
        # print('Current frame: {}'.format(self._image_number))
        return image

    def request_image(self, skip):
        """ Запросить у сервера обработку изображения """
        img = self.get_next_image(skip)
        if img is None: return

        # If we already received a response for this frame,
        # immediately return the cached result to the client UI
        # without making a new server request
        response = self.get_cached_item(self._image_number)
        if response:
            # print("Retrieved cached response: {}".format(response))
            self._event_handler.after(50, lambda: self.process_response(response, img, self._image_number))
            return

        # There was no cached response -> make a new server request
        max_dim = max(img.shape)
        threshold = self._config.get('resize_threshold', 640)

        if max_dim > threshold:
            # print("Image shape before resizing:", img.shape)
            img = self.resize_image(img, threshold / max_dim)
            # print("Image shape after resizing:", img.shape)
            # show_image(img, "Resized image")

        # FIXME: imencode makes it 3 channels again
        # if self._send_grayscale and img.shape[2] > 1:
        #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #     print("image shape after conversion:", img.shape)
        #     # show_image(img, "Grayscale image")

        success, encoded_image = cv2.imencode('.jpg', img)
        # print('Processing frame {}'.format(self._image_number))

        header = { 'command': 'load_image', 'frame_index': self._image_number, 'detect_inner_objects': self._inner_detection_enabled }
        data_to_send = make_request(header, encoded_image.tobytes())
        self._connection.send(data_to_send)

    def seek_to_frame(self, frame):
        self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def request_summary(self, handler):
        """ Запросить статистику по обработанным данным """
        # Produce annotation file
        annotation = Video_Annotation(self._video_path)
        annotation.set_frame_annotations(self._response_cache)
        annotation = preprocess_video_annotation(annotation) # Fix sleep detection
        annotation.save_annotation(os.path.splitext(self._video_path)[0]+".json", indent=2, sort_keys=True)

        # Produce summary
        summary_config = ObjectDict({
            'object_names': self._object_names,
            'max_detection_targets': self._config.max_detection_targets,
            'video_fps': self._vidcap.get(cv2.CAP_PROP_FPS) })
        statistic = summarize_video_annotation(annotation, summary_config)

        # Invoke the UI callback
        handler(statistic, self._video_path)

    def save_current_frame(self):
        if self._image is None: return
        video_filename = os.path.splitext(os.path.basename(self._video_path))[0]
        response = self.get_cached_item(self._image_number)
        self._frame_saver.save(video_filename, self._image_number, self._image, response)

    def set_realtime_processing(self, enabled):
        if not enabled:
            self._request_postprocessor = None
        self._rt_processing_enabled = enabled

    def set_box_limit(self, enabled):
        if self._frame_decorator:
            self._frame_decorator.set_box_limit(enabled, self._config.max_detection_targets)

    def set_inner_detection(self, enabled):
        self._inner_detection_enabled = enabled

    def on_new_message(self, data):
        """ Обработка сообщения от сервера """
        if self._config.verbose:
            print("Received message from server: {}".format(data))
        json_string = data.decode()
        response = json.loads(json_string)
        event = response.get('event')
        success = response.get('status') == 'ok'

        if event == 'awaiting_authorization':
            self._connection.send(make_request({ 'command': 'authorize', 'key': self._config.secret_key }))
        elif event == 'authorize':
            pass
        elif event == 'ping':
            self._event_handler.received_ping_reply(response)
        elif event == 'load_image':
            frame_index = response.get('frame_index', self._image_number)
            self.process_new_response(response, frame_index)
        elif event == 'upload_begin' and success:
            self.begin_upload(response.get('filename', self._upload_filename), response.get('buffer_size', self._config.upload_buffer_max_size))
        elif event == 'upload_append' and success:
            self.continue_upload(response.get('finished', False), response.get('filename', self._upload_filename), response.get('bytes', 0))
        elif event == 'error':
            if response.get('domain') == 'upload':
                self.cancel_upload()
            self._event_handler.handle_error(RuntimeError(response.get('message', "Server error")))
        else:
            print("The server returned a response to an unknown command: {}".format(repr(command))) # Maybe response?

    def command(self, cmd, **kwargs):
        """Handle a UI command"""
        if cmd == 'PING':
            self.send_ping()
        elif cmd == 'NEXT_FRAME':
            self.request_image(kwargs['skip'])
        elif cmd == 'SEEK_FRAME':
            self.seek_to_frame(kwargs['frame'])
        elif cmd == 'GET_SUMMARY':
            self.request_summary(kwargs['Handler'])
        elif cmd == 'SET_FILE':
            self.set_source(kwargs['FileName'], kwargs['available_height'])
        elif cmd == 'SET_SCALE':
            self._image_scale = kwargs['scale']
        elif cmd == 'CALC_SCALE':
            self._image_scale = self.calculate_scale(kwargs['available_height'])
        elif cmd == 'REFRESH_FRAME':
            self.refresh_frame(kwargs.get('available_height'))
        elif cmd == 'CONNECT':
            self.connect(kwargs['ip'], kwargs['port'], kwargs['server_type'])
        elif cmd == 'VIDEO_CLICKED':
            self.on_click(kwargs['event'])
        elif cmd == 'SET_OBJECT_NAME':
            self.set_object_name(kwargs['id'], kwargs['name'], kwargs['frame_index'])
        elif cmd == 'CLEAR_CACHE':
            self.reset_cache()
        elif cmd == 'BEGIN_UPLOAD':
            self.request_upload()
        elif cmd == 'BEGIN_PROCESSING':
            self.processing_mode_start()
        elif cmd == 'END_PROCESSING':
            self.processing_mode_request_end()
        elif cmd == 'DUMP_FRAME':
            self.save_current_frame()
        elif cmd == 'DUMP_VIDEO':
            self.set_video_output_mode(kwargs['enabled'])
        elif cmd == 'REALTIME_PROCESSING':
            self.set_realtime_processing(kwargs['enabled'])
        elif cmd == 'BOX_LIMIT':
            self.set_box_limit(kwargs['enabled'])
        elif cmd == 'INNER_DETECTION':
            self.set_inner_detection(kwargs['enabled'])
