import json
import numpy as np
import cv2
import random
import json
from abc import abstractmethod
from PyQt5.QtCore import Qt, QObject, QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal

import PreprocessedMediaSource as pms
from util.protocol import make_request
from util.digNetwork.tcpclient import TcpClient

class RemoteNeuralProcessor(pms.AsyncProcessor):
    onError = pyqtSignal(str)
    onServerConnected = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self._config = config
        self.ip = config.ip
        self.port = config.port
        self._connection = None
        self._image_buffer = {}
        self._response_cache = None
        self._is_connected = False

    def start_connection(self, ip, port):
        self.close_connection()
        try:
            self._connection = TcpClient(ip, port, self.server_connected, self.on_new_message, buffer_size=self._config.tcp_client_buffer_size)
            self._connection.start()
            self._is_connected = True
        except Exception as ex:
            print(ex)
            self.onError.emit(repr(ex))

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            self._is_connected = False

    def server_connected(self, hostname, port):
        print("Server connected")
        self._is_connected = True
        self.onServerConnected.emit()

    def on_new_message(self, data):
        """ Обработка сообщения от сервера """
        if self._config.verbose or True:
            pass
            #print("Received message from server: {}".format(data))
        json_string = data.decode()
        response = json.loads(json_string)
        event = response.get('event')
        success = response.get('status') == 'ok'

        if event == 'awaiting_authorization':
            self._connection.send(make_request({ 'command': 'authorize', 'key': self._config.secret_key }))
        elif event == 'authorize':
            pass
        elif event == 'ping':
            pass
            #TODO: self._event_handler.received_ping_reply(response)
        elif event == 'load_image':
            frame_index = response.get('frame_index', self._image_number)
            self.process_new_response(response, frame_index)
        elif event == 'upload_begin' and success:
            pass
            #TODO: self.begin_upload(response.get('filename', self._upload_filename), response.get('buffer_size', self._config.upload_buffer_max_size))
        elif event == 'upload_append' and success:
            pass
            #TODO: self.continue_upload(response.get('finished', False), response.get('filename', self._upload_filename), response.get('bytes', 0))
        elif event == 'error':
            if response.get('domain') == 'upload':
                self.cancel_upload()
            self.onError.emit("Server error")
        else:
            print("The server returned a response to an unknown command: {}".format(repr(response)))

    def process_new_response(self, response, frame_index):
        frame = self._image_buffer.pop(frame_index)
        self._last_frame = {'image':frame, 'response':response}
        self.nextDataLoaded.emit({'image':frame, 'response':response})

    def load_cache(self, file_name):
        with open(file_name, "r") as read_file:
            self._response_cache = json.load(read_file)["frame_annotations"]

    def try_load_response_from_cache(self, frame_number):
        """
        Попытка загрузить ответ сервера из кэша. В кэше должен быть сохранен полный ответ сервера
        """
        if self._response_cache is None:
            return None        
        try:
            return self._response_cache[str(frame_number)]
        except AttributeError:
            return {}
        except KeyError:
            return {"dogs":()} 

    def fuzzy_equal_frame(self, img_1, img_2, moving_threshold = 0.008):
        '''
        moving_threshold -- float [0 ... 1]
        '''
        # Convert to B&W image
        cur_frame = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
        prev_frame = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)

        # Blur cropped B&W image
        cur_frame = cv2.GaussianBlur(cur_frame, (11, 11), 0)
        prev_frame = cv2.GaussianBlur(prev_frame, (11, 11), 0)

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

        is_moving = False

        image_area = img_1.shape[0] * img_1.shape[1]

        # loop over the contours
        max_moving = 0
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c)/image_area > max_moving:
                max_moving = cv2.contourArea(c)/image_area

            if cv2.contourArea(c)/image_area < moving_threshold:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            is_moving = True
        #print(max_moving)
        return not is_moving

    @abstractmethod
    def run(self):
        """
        Функция вызывается при запуске потока, можно использовать, как конструктор
        """
        print("RemoteNeuralProcessor Start")
        self.start_connection(self.ip, self.port)

    @abstractmethod
    @pyqtSlot(np.ndarray, dict)
    def processFrame(self, frame, params):
        """
        Абстрактный метод для начала асинхронной обработки фрейма.
        frame -- ndarray с изображением для обработки
        params -- dict с необходимыми параметрами, м.б. пустым

        Для возвращения результатов обработки используется вызов сигнала nextDataLoaded,
        аргумнтом которого является dict с обязательным членом 'image'
        """
        try:
            self._image_number = params['image_number']
        except:
            self._image_number = int(random.random() * 100000)
        self._image_buffer[self._image_number] = frame

        cache_response = self.try_load_response_from_cache(self._image_number)
        if cache_response is not None:
            frame = self._image_buffer.pop(self._image_number)
            cur_frame = {'image':frame, 'response':cache_response}
            cur_frame['response']['frame_index'] = self._image_number
            self.nextDataLoaded.emit(cur_frame)    
            return

        #Если не подключен, то ничего более не делаем
        if not self._is_connected:
            return

        equal_frame = False
        try:
            equal_frame = self.fuzzy_equal_frame(self._last_frame['image'], frame)
        except AttributeError:
            pass        
        
        if(equal_frame):
            cur_frame = self._last_frame
            cur_frame['image'] = self._image_buffer.pop(self._image_number)
            cur_frame['response']['frame_index'] = params['image_number']
            self.nextDataLoaded.emit(cur_frame)
        else:
            success, encoded_image = cv2.imencode('.jpg', frame)
            # print('Processing frame {}'.format(self._image_number))
            header = { 'command': 'load_image', 'frame_index': self._image_number, 'detect_inner_objects': self._config.inner_detection }
            data_to_send = make_request(header, encoded_image.tobytes())
            self._connection.send(data_to_send)

    @abstractmethod
    def close(self):
        """
        Строго синхронный (в потоке) метод, вызываетмы при запросе завершения потока
        в этом методе необходимо освободать ресурсы, если это необходимо
        """
        self.close_connection()

class NNProcessedMediaSource(pms.PreprocessedMediaSource):
    """
    В классе реализован функционал обработки нейросетевой изображения на удаленном сервере
    Весь остальной функционал (включая отображение результатов на изображении) оставлен
    без изменения: загрузка изображения в вебкамеры, пост и предобработка отсутствуют
    """
    onServerConnected = pyqtSignal()
    onError = pyqtSignal(str)

    def __init__(self, config):
        self._config = config
        super().__init__()

    @abstractmethod
    def getFrameProcessor(self):
        """
        Возвращает объект для асинхронной обработки функции
        """
        return RemoteNeuralProcessor(self._config)
