#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Wed Oct 31 21:30:05 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

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

Created on Wed Oct 31 21:30:05 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Wed Oct 31 21:30:05 2018'
__version__ = '0.1'

from plugins.base_plugin import Base_Plugin
from util.digNetwork.tcpclient import TcpClient
from util.protocol import make_request
import json
import cv2
import threading
from analitics.annotation import Annotation


class Packet_Video_Client(Base_Plugin):
    """
    Command:
        PVC_Plugin_CONNECT_TO_SERVER
        PVC_Plugin_DISCONNECT_FROM_SERVER
        PVC_Plugin_PROCESS_VIDEOS

    TODO: Because procedure may be very long, move into thread

    """
    def __init__(self):
        self.ID = "PVC_Plugin_"
        self._tcp_client = None
        self._response_cache = {}
        self._server_is_busy = threading.Event()

    def command(self, cmd, **kwargs):
        """
        Обработчик команд
        """
        if cmd == "CONNECT":
            if self._tcp_client is not None:
                self._tcp_client.close()
            self._tcp_client = TcpClient(kwargs['ip'],
                                         kwargs['port'],
                                         self.on_new_message,
                                         buffer_size=1024*1024)
        if cmd == self.ID+"DISCONNECT_FROM_SERVER":
            if self._tcp_client is not None:
                self._tcp_client.close()
                self._tcp_client = None

        if cmd == self.ID+"PROCESS_VIDEOS":
            if self._tcp_client is not None:
                videos = kwargs['videos']
                self.process_packet(videos)

    def close(self):
        if self._tcp_client is not None:
            self._tcp_client.close()
            self._tcp_client = None

    def update_cache(self, index, response):
        self._response_cache[index] = response

    def get_cached_item(self, index):
        return self._response_cache.get(index)

    def on_new_message(self, data):
        """
        Обработка сообщения от сервера
        """
        json_string = data.decode()
        response = json.loads(json_string)
        self._server_is_busy.clear()
        self.update_cache(response['frame_index'], response)

    def process_packet(self, videos):
        for vid in videos:
            self.process_video(vid)

    def process_video(self, video_path):
        """
        Обработать видео
        """
        image_number = 0
        self._response_cache = {}
        for encoded_image in self.images_from_video(video_path):
            self._server_is_busy.set()
            header = {'frame_index': image_number}
            image_number += 1
            data_to_send = make_request(header, encoded_image.tobytes())
            self._tcp_client.send(data_to_send)
            self._server_is_busy.wait()
        annotation = Annotation(video_path)
        annotation.set_frames_annotation(self._response_cache)
        # TODO: cut extention from video path and replace it by '.json'
        annotation.save_annotation(video_path+".json")


    def images_from_video(self, video_path):
        vidcap = cv2.VideoCapture(video_path)
        print("Start work with video: {}".format(video_path))
        self._image_number = 0
        while True:
            success, image = vidcap.read()
            if success:
                self._image_number += 1
                yield image
            else:
                break