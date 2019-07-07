from PyQt5.QtCore import pyqtSlot, pyqtSignal
import cv2
import os
import shutil
import numpy as np
from abc import abstractmethod

from NNPreprocessedMediaSource import NNProcessedMediaSource
from analitics.analysis import RT_frame_processing
from util.video_tools import FrameDecorator, VideoSaver

class Video2nnMediaSource(NNProcessedMediaSource):
    onNewFrameAnnotation = pyqtSignal(dict)

    def __init__(self, config):
        super().__init__(config)  # self._config = config
        self._frame_decorator = FrameDecorator(config)

        self._request_postprocessor = RT_frame_processing(
                max_memory_len=self._config.frame_processing_max_memory,
                sleep_thr=self._config.frame_processing_sleep_threshold,
                object_count_limit=self._config.max_detection_targets)

        self._saving_output_video = self._config.save_annotated_video
        self._video_saver = None

    @abstractmethod
    def run(self):
        print("Video2nnMediaSource run")

    def seek_to_frame(self, frame):
        self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)

    @abstractmethod 
    def get_next_image(self):
        """ Получение следующего кадра из источника видео """
        check = True
        while check:
            frame_index = int(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
            success, image = self._vidcap.read()
            if not success: return None, None
            self._image_number = frame_index
            check = self.has_cached_image(self._image_number)
        return frame_index, image

    def postProcess(self, data):
        image = data['image']
        response = data['response']

        response = self._request_postprocessor.process_frame(image, response)

        self._object_names = {}
        image = self._frame_decorator.decorate(image, response, self._object_names)
        
        if self._saving_output_video:
            # The frames for saving the video output file have to be in a constant resolution, so we need to decorate twice
            self.save_output_video_frame(image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.save_frame(image, data['response']['frame_index'])

        try:
            self.onNewFrameAnnotation.emit(response)
        except:
            pass
        return image

    def save_output_video_frame(self, frame):
        #vidcap = cv2.VideoCapture(video_path)
        if self._video_saver is None:
            dir_path = os.path.dirname(self._video_path)
            base_filename = os.path.splitext(os.path.basename(self._video_path))[0]
            self._video_saver = VideoSaver.create(self._config, dir_path, base_filename, self._vidcap)
        self._video_saver.add_frame(frame)

    def reset_output_video(self):
        if self._video_saver is not None:
            self._video_saver.close()
            self._video_saver = None

    @pyqtSlot(str)
    def set_source(self, video_path):
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
        self.drop_cache()
        self._image_number = 0
        self._current_position = 0
        self._source_width = int(self._vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._source_height = int(self._vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._frame_count = int(self._vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._fps = int(self._vidcap.get(cv2.CAP_PROP_FPS))
        self.reset_output_video()
        self.set_video_param()
        filename, _ = os.path.splitext(video_path)
        cache_path = filename + '.json'
        if os.path.isfile(cache_path):
            self._frameProcessor.load_cache(cache_path)

        print("Opened video: {}".format(video_path))
        self.video_params = {
            'width': self._source_width,
            'height': self._source_height,
            'frame_count': self._frame_count,
            'filename': video_path
        }
        self.metaDataChanged.emit(self.video_params)

        # После получения источника можно начать обработку
        self.stage_1()#by signal
        
    @abstractmethod
    def set_video_param(self):
        pass

    @abstractmethod
    def getFrameLoader(self):
        """
        Возвращает функцию(!) для загрузки следующего фрейма
        """
        return self.get_next_image

    @abstractmethod
    def getFramePostProcessor(self):
        """
        Возвращает функцию для синхронной постобработки фрейма после его получения
        """
        return self.postProcess

    @abstractmethod
    def getMediaMetaData(self):
        return self.video_params

    @abstractmethod
    def changePosition(self, position):
        #TODO: Переход на новую позицию в файле. Обработка кэша.
        print('changePosition', position)
        self._image_number = position
        self._current_position = position
        self.seek_to_frame(position)

    #Inherit from MediaSource
    @abstractmethod    
    def loadPrevFrame(self):
        try:
            frame = self.load_frame(self._current_position - 1)
            if frame is not None:
                self._current_position -= 1
                return self._current_position-1, frame
            else:
                return None, None
        except:
            return None, None

    @abstractmethod
    def loadNextFrame(self):
        try:
            frame = self.load_frame(self._current_position)
            if frame is not None:
                self._current_position += 1
                return self._current_position-1, frame
            else:
                return None, None
        except:
            return None, None

    def save_frame(self, frame, pos):
        try:
            os.makedirs('./.aba/frames')
        except :
            pass
        cv2.imwrite('./.aba/frames/'+ str(pos) + '.jpg', frame)
        self._video[pos] = pos
        #self._video[pos] = frame

    def load_frame(self, pos):
        #return self._video[pos]
        return cv2.imread('./.aba/frames/'+ str(pos) + '.jpg')

    def drop_cache(self):
        self._video = {}
        try:
            shutil.rmtree('./.aba/frames')
        except:
            pass

    def has_cached_image(self, pos):
        return self._image_number in self._video.keys()
