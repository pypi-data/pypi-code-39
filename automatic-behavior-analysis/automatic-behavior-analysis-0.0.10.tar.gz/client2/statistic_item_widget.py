import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class StatisticItemWidget(QtWidgets.QWidget):
    nameChanged = pyqtSignal(str)

    def __init__ (self, parent = None):
        super(StatisticItemWidget, self).__init__(parent)
        self.id = None
        self.name = None

        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self._id    = QtWidgets.QLabel()
        self._state  = QtWidgets.QLabel()
        self._pos_x = QtWidgets.QLabel()
        self._pos_y = QtWidgets.QLabel()
        self._name_label = QtWidgets.QLabel()
        self._name_line_edit = QtWidgets.QLineEdit()
        self._name_button = QtWidgets.QPushButton("Set name")
        self._name_button.clicked.connect(self.nameEdit)
        self._space = QtWidgets.QLabel()

        self._id.setText("ID: ")
        self._state.setText("STATE: ")
        self._pos_x.setText("POS X: ")
        self._pos_y.setText("POS Y: ")
        self._name_label.setText("NAME: ")
        
        self.textQHBoxLayout = QtWidgets.QHBoxLayout()
        self.textQHBoxLayout.addWidget(self._name_label)
        self.textQHBoxLayout.addWidget(self._name_line_edit)
        self.textQHBoxLayout.addWidget(self._name_button)

        self.textQVBoxLayout.addWidget(self._id)
        self.textQVBoxLayout.addWidget(self._state)
        self.textQVBoxLayout.addWidget(self._pos_x)
        self.textQVBoxLayout.addWidget(self._pos_y)
        self.textQVBoxLayout.addLayout(self.textQHBoxLayout)
        self.textQVBoxLayout.addWidget(self._space)
  
        self.setLayout(self.textQVBoxLayout)


    def setStatistic (self, dog, name):
        # устанавливает статистику
        if dog:
            self.id = dog.get('id')

            self._id.setText("ID: "+ str(dog.get('id')))
            self._state.setText("STATE: "+ str(dog.get('state')))
            self._pos_x.setText("POS X: "+ str(round(dog.get('x1'), 3)) + " " + str(round(dog.get('x2'), 3)))
            self._pos_y.setText("POS Y: "+ str(round(dog.get('y1'), 3)) + " " + str(round(dog.get('y2'), 3)))
            self._name_label.setText("NAME: ")
            self._name_line_edit.setText(name)
        else:
            self.id = None
            self.name = None

            self._id.setText("ID: ")
            self._state.setText("STATE: ")
            self._pos_x.setText("POS X: ")
            self._pos_y.setText("POS Y: ")
            self._name_label.setText("NAME: ")
            self._name_line_edit.setText("")

    def clearRtStatistic(self):
        self._id.setText("ID: ")
        self._state.setText("STATE: ")
        self._pos_x.setText("POS X: ")
        self._pos_y.setText("POS Y: ")
        self._name_label.setText("NAME: ")

    @pyqtSlot()
    def nameEdit(self):
        self.name = self._name_line_edit.text()
        if self.name != "":
            self.nameChanged.emit(self.name)



class SummaryStatisticItemWidget(QtWidgets.QWidget):
    def __init__ (self, parent = None):
        super(SummaryStatisticItemWidget, self).__init__(parent)
        # переменные, хранящие статистику
        self._total_frames    = 0
        self._frames_with_dogs  = 0
        self._frames_with_dog_1 = 0
        self._frames_with_dog_1_asleep = 0
        self._frames_with_dog_2 = 0
        self._frames_with_dog_2_asleep = 0

        # переменные, хранящие виджеты QLabel со статистикой
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self._total_frames_w    = QtWidgets.QLabel()
        self._frames_with_dogs_w  = QtWidgets.QLabel()
        self._frames_with_dog_1_w = QtWidgets.QLabel()
        self._frames_with_dog_1_asleep_w = QtWidgets.QLabel()
        self._frames_with_dog_2_w = QtWidgets.QLabel()
        self._frames_with_dog_2_asleep_w = QtWidgets.QLabel()

        self._total_frames_w.setText("TOTAL FRAME: ")
        self._frames_with_dogs_w.setText("FRAMES WITH DOGS: ")
        self._frames_with_dog_1_w.setText("FRAMES WITH DOG 1: ")
        self._frames_with_dog_1_asleep_w.setText("FRAMES WITH DOG 1 ASLEEP: ")
        self._frames_with_dog_2_w.setText("FRAMES WITH DOG 2: ")
        self._frames_with_dog_2_asleep_w.setText("FRAMES WITH DOG 2 ASLEEP: ")

        self.textQVBoxLayout.addWidget(self._total_frames_w)
        self.textQVBoxLayout.addWidget(self._frames_with_dogs_w)
        self.textQVBoxLayout.addWidget(self._frames_with_dog_1_w)
        self.textQVBoxLayout.addWidget(self._frames_with_dog_1_asleep_w)
        self.textQVBoxLayout.addWidget(self._frames_with_dog_2_w)
        self.textQVBoxLayout.addWidget(self._frames_with_dog_2_asleep_w)
  
        self.setLayout(self.textQVBoxLayout)

    def setSummaryStatistic(self, data):
        self._total_frames += 1
        dogs = data.get('dogs')
        if dogs:
            self._frames_with_dogs += 1

            dog_id = dogs[0].get('id')
            dog_state = dogs[0].get('state')
            if dog_id == 0:
                self._frames_with_dog_1 += 1
                if dog_state == 'sleep':
                    self._frames_with_dog_1_asleep += 1
            elif dog_id == 1:
                self._frames_with_dog_2 += 1
                if dog_state == 'sleep':
                    self._frames_with_dog_2_asleep += 1
            if len(dogs) == 2:
                dog_id = dogs[1].get('id')
                dog_state = dogs[1].get('state')
                if dog_id == 0:
                    self._frames_with_dog_1 += 1
                    if dog_state == 'sleep':
                        self._frames_with_dog_1_asleep += 1
                elif dog_id == 1:
                    self._frames_with_dog_2 += 1
                    if dog_state == 'sleep':
                        self._frames_with_dog_2_asleep += 1


        self._total_frames_w.setText("TOTAL FRAME: " + str(self._total_frames))
        self._frames_with_dogs_w.setText("FRAMES WITH DOGS: " + str(self._frames_with_dogs))
        self._frames_with_dog_1_w.setText("FRAMES WITH DOG 1: " + str(self._frames_with_dog_1))
        self._frames_with_dog_1_asleep_w.setText("FRAMES WITH DOG 1 ASLEEP: " + str(self._frames_with_dog_1_asleep))
        self._frames_with_dog_2_w.setText("FRAMES WITH DOG 2: " + str(self._frames_with_dog_2))
        self._frames_with_dog_2_asleep_w.setText("FRAMES WITH DOG 2 ASLEEP: " + str(self._frames_with_dog_2_asleep))

    def clearSummaryStatistic(self):
        self._total_frames    = 0
        self._frames_with_dogs  = 0
        self._frames_with_dog_1 = 0
        self._frames_with_dog_1_asleep = 0
        self._frames_with_dog_2 = 0
        self._frames_with_dog_2_asleep = 0

        self._total_frames_w.setText("TOTAL FRAME: ")
        self._frames_with_dogs_w.setText("FRAMES WITH DOGS: ")
        self._frames_with_dog_1_w.setText("FRAMES WITH DOG 1: ")
        self._frames_with_dog_1_asleep_w.setText("FRAMES WITH DOG 1 ASLEEP: ")
        self._frames_with_dog_2_w.setText("FRAMES WITH DOG 2: ")
        self._frames_with_dog_2_asleep_w.setText("FRAMES WITH DOG 2 ASLEEP: ")