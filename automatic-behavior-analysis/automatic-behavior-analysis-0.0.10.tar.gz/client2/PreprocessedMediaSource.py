from abc import abstractmethod
from PyQt5.QtCore import Qt, QObject, QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage
from videowidget import MediaSource


import cv2
import numpy as np
import queue

class AsyncProcessor(QObject):
    """
    Базовый класс для асинхронного обработчика изоборажений.
    """
    finished = pyqtSignal()
    nextDataLoaded = pyqtSignal(dict)

    @abstractmethod
    def run(self):
        """
        Функция вызывается при запуске потока, можно использовать, как конструктор
        """

    @abstractmethod
    def close(self):
        """
        Строго синхронный (в потоке) метод, вызываетмы при запросе завершения потока
        в этом методе необходимо освободать ресурсы, если это необходимо
        """
        pass

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
        # Вызов необходим для возвращения результата обработки. Поле 'image' -- обязательное
        self.nextDataLoaded.emit({'image':frame})

    @pyqtSlot()
    def stopRequest(self):
        self.close()
        QThread.currentThread().exit()

class PreprocessedMediaSource(MediaSource):
    """
    Базовый класс для источника медиапотока с использованием потоковой асинхронной обработки.
    Класс предполагает потоковую обработку видео, однако поддерживает методы перехода по потоку.
    Буферизация отображенных кадров не осуществляется, обработка асинхронная может быть быстрее,
    чем скорость отображения (возвращения).

    При переходе по видео при наличии буферизации необходимо сбрасывать очередь кадров.

    При наследовании можно переопределить следующие абстрактные методы:
        def run(self) -- метод вызывается при старте потока
        def getFrameLoader(self) -- метод, возвращающий функциюполучения следующего кадра
            для обработки. По умолчанию возвращает изображение с Web камеры. Стоит
            обратить внимание на то, что в текущей реализации обработанный кадр помещается
            в конец очереди на отображение.
        def getFramePreprocessor(self) -- метод, возвращающий функцию предобработки изображения
            при отсутствии переопределения, предобработка отсутствует
        def getFrameProcessor(self) -- метод, возвращающий асинхронный обработчик изображения.
            При реализации обязательно наследование от AsyncProcessor (или его наследников)
        def getFramePostProcessor(self) -- метод, возвращающий функцию, для постобработки
            изображения и/или аннотации, может использоваться для сохранения прогресса
    """
    requestDataProcess = pyqtSignal(np.ndarray, dict)

    def __init__(self):
        super().__init__()

        self.frame_buffer = queue.Queue()

        self._frameLoad = self.getFrameLoader()
        self._framePreprocess = self.getFramePreprocessor()
        self._frameProcessor = self.getFrameProcessor()
        self._framePostProcess = self.getFramePostProcessor()

        self._processorThread = QThread()

        self._frameProcessor.finished.connect(self._processorThread.quit)
        self._frameProcessor.nextDataLoaded.connect(self.nextDataLoaded)
        self._frameProcessor.moveToThread(self._processorThread)

        self.requestDataProcess.connect(self._frameProcessor.processFrame)

        self._processorThread.started.connect(self._frameProcessor.run)
        #self._processorThread.finished.connect(self.mediaFinished)
        self._processorThread.finished.connect(self._processorThread.deleteLater)
        self._processorThread.start()

    @abstractmethod
    def run(self):
        print("PreprocessedMediaSource run")
        self.stage_1()

    def stage_1(self):
        """
        Загрузка, предобработка и отправка для асинхронной обработки
        """
        pos, frame = self._frameLoad()
        if frame is None: return
        frame = self._framePreprocess(frame)
        self.requestDataProcess.emit(frame, {'image_number':pos})

    def stage_2(self, data):
        """
        Постобработка и буфреризация в очередь отображения
        """
        frame = self._framePostProcess(data)
        self.stage_1()


    @pyqtSlot(dict)
    def nextDataLoaded(self, data):
        self.stage_2(data)

    # Инициализация обработчиков и источников данных
    def defaultPreProcess(self, image):
        return image

    def defaultPostProcess(self, data):
        self.frame_buffer.put(data['image'])
        self.newStatisticData.emit(data)
        return data['image']

    def defaultLoader(self):
        try:
            self.defaultLoader_cap
        except AttributeError:
            self.defaultLoader_cap = cv2.VideoCapture(0)
        ret, frame = self.defaultLoader_cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.copy(frame)
            return None, frame
        return None, None

    # Методы для переопределения в наследниках при необходимости
    @abstractmethod
    def getFrameLoader(self):
        """
        Возвращает функцию(!) для загрузки следующего фрейма
        """
        return self.defaultLoader

    @abstractmethod
    def getFramePreprocessor(self):
        """
        Возвращает функцию для синхронной предобработки фрейма
        """
        return self.defaultPreProcess

    @abstractmethod
    def getFrameProcessor(self):
        """
        Возвращает объект для асинхронной обработки функции
        """
        return AsyncProcessor()

    @abstractmethod
    def getFramePostProcessor(self):
        """
        Возвращает функцию для синхронной постобработки фрейма после его получения
        """
        return self.defaultPostProcess

    #Inherit from MediaSource
    @abstractmethod
    def loadNextFrame(self):
        try:
            return None, self.frame_buffer.get(False)
        except queue.Empty as e:
            return None, None
