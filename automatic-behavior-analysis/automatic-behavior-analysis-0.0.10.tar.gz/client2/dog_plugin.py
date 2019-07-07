from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QImage
from abc import abstractmethod
from video2nnMediaSource import Video2nnMediaSource
from statistic_item_widget import StatisticItemWidget, SummaryStatisticItemWidget
from statistic_holder import StatisticHolder

import base_plugin
import cv2
import os

class SleepDogPlugin(base_plugin.BasePlugin):
    setVideoSrc = pyqtSignal(str)

    def __init__(self, config=None, parent=None):
        super().__init__(config=config, parent=parent)

        self._MAX_OBJECTS = 2

        self._current_viewed_frame = None

        self._rt_statistic_widget = QListWidget()
        self._summary_statistic_widget = QListWidget()

        self.status_bar = None

        self._statistic_holder = None
        # создание объекта виджета статистики и его установка в QListWidget

        self._statistic_items = []
        for i in range(self._MAX_OBJECTS):
            self._statistic_items.append(StatisticItemWidget())
            myQListWidgetItem = QListWidgetItem(self._rt_statistic_widget)
            myQListWidgetItem.setSizeHint(self._statistic_items[i].sizeHint())
            self._rt_statistic_widget.addItem(myQListWidgetItem)
            self._rt_statistic_widget.setItemWidget(myQListWidgetItem, self._statistic_items[i])
            self._statistic_items[i].nameChanged.connect(self.nameChanged)

        # создание объекта виджета суммарной статистики и его установка в QListWidget
        self._summary_statistic_item = SummaryStatisticItemWidget()
        myQListWidgetItem = QListWidgetItem(self._summary_statistic_widget)
        myQListWidgetItem.setSizeHint(self._summary_statistic_item.sizeHint())
        self._summary_statistic_widget.addItem(myQListWidgetItem)
        self._summary_statistic_widget.setItemWidget(myQListWidgetItem, self._summary_statistic_item)

    def set_status_bar(self, status_bar):
        self.status_bar = status_bar

    def set_menu(self, root_menu):
        action = root_menu.addAction("Save statistic")
        action.triggered.connect(self.save_all_statistic)
        action = root_menu.addAction("Go to unnamed objects")
        action.triggered.connect(self.go_to_unnamed_obj)

    def save_all_statistic(self):
        try:
            self._statistic_holder.save_all_history()
        except:
            pass


    def go_to_unnamed_obj(self):
        unnamed_obj_list = self._statistic_holder.get_unnamed_objects_position()
        if unnamed_obj_list:
            next_unnamed_obj_list = list(filter(lambda x: x > self._current_viewed_frame, unnamed_obj_list))
            if len(next_unnamed_obj_list) > 0:
                self._media_source.changePosition(next_unnamed_obj_list[0])
            else:
                self._media_source.changePosition(unnamed_obj_list[0])

    def update_rt_statistic(self, pos):
        dogs = self._statistic_holder.annotation_buffer[pos].objects

        for stat_widget in self._statistic_items:
            stat_widget.clearRtStatistic()

        for dog in dogs.values():
            dog_id = dog.get('id')
            if dog_id >= self._MAX_OBJECTS:
                continue
            name = self._statistic_holder.get_object_name(pos, dog_id)
            self._statistic_items[dog_id].setStatistic(dog, name)

    @pyqtSlot(str)
    def nameChanged(self, name):
        sender = self.sender()
        if sender.id != None:
            self._statistic_holder.set_object_name(self._current_viewed_frame, sender.id, name)


    @abstractmethod
    def get_media_source_processor(self):
        self._media_source = Video2nnMediaSource(self._config)
        self._media_source.onNewFrameAnnotation.connect(self.add_frame_annotation)
        self._media_source.changePixmap.connect(self.frameChanged)
        self._media_source.newStatisticData.connect(self.add_frame_annotation)
        self.setVideoSrc.connect(self._media_source.set_source)

        return self._media_source

    @abstractmethod
    def get_rt_statistic_widget(self):
        return self._rt_statistic_widget

    @abstractmethod
    def get_summary_statistic_widget(self):
        return self._summary_statistic_widget

    @pyqtSlot(dict)
    def add_frame_annotation(self, summary):
        """
        На этом уровне должно сохраняться соответствие введенного имени/индекса
        в виджете статистики и собакам на кадрах. При необходимости обновляться и
        распространяться (вперед и назад до момента отсутствия объектов в кадре) при смене.
        Также необходимо подготовить данные для сохранения статистики.
        """
        self._statistic_holder.add_frame_annotation(summary)
        self._summary_statistic_item.setSummaryStatistic(summary)

    @pyqtSlot(int, QImage)
    def frameChanged(self, position, image):
        """

        """
        # TODO: Обновление содержимого виджетов статистики
        print("Frame changed")
        self._current_viewed_frame = position
        self.update_rt_statistic(position)

    @pyqtSlot(str)
    @abstractmethod
    def onOpenFile(self, filename):
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist: '{}'".format(filename))

        if not os.path.isfile(filename):
            raise RuntimeError("'{}' is not a file".format(filename))

        vidcap = cv2.VideoCapture(filename)
        if not vidcap.isOpened():
            raise RuntimeError("Invalid file format")

        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        vidcap.release()

        self._current_file = filename
        self.setVideoSrc.emit(filename)
        self.status_bar.showMessage(filename)

        self._statistic_holder = StatisticHolder(filename, fps)

        for stat_widget in self._statistic_items:
            stat_widget.clearRtStatistic()

        self._summary_statistic_item.clearSummaryStatistic()
