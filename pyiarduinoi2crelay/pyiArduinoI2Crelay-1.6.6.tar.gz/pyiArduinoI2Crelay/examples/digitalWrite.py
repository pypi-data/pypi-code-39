#encoding=utf-8
# Данный пример поочерёдно включает и выключает каналы модуля.      # * Строки со звёздочкой являются необязательными.
                                                                    #
from pyiArduinoI2Crelay import *                                 #   Подключаем библиотеку для работы с реле и силовыми ключами.
from time import sleep                        # Подключаем метод sleep библиотеки time
relay = pyiArduinoI2Crelay(0x09);                          #   Создаём объект relay для работы с функциями и методами библиотеки Py_iarduino_I2C_Relay, указывая адрес модуля на шине I2C.
                                                                    #   Если объявить объект без указания адреса (iarduino_I2C_Relay relay;), то адрес будет найден автоматически.
relay.digitalWrite(ALL_CHANNEL,LOW);                              # * Выключаем все каналы модуля.
while True:                                                       #   Входим в бесконечный цикл
#Включаем и выключаем каналы модуля:                              #
  relay.digitalWrite(1,HIGH)                    # Включаем 1 канал
  relay.digitalWrite(4,LOW)                         #   и выключаем 4.
  sleep(.5)                                                       #   Ждём   500 мс.
  relay.digitalWrite(2,HIGH)                    # Включаем 2 канал
  relay.digitalWrite(1,LOW)                         #   и выключаем 1.
  sleep(.5)                                                       #   Ждём   500 мс.
  relay.digitalWrite(3,HIGH)                    # Включаем 3 канал
  relay.digitalWrite(2,LOW)                         #   и выключаем 2.
  sleep(.5)                                                     #   Ждём   500 мс.
  relay.digitalWrite(4,HIGH)                    # Включаем 4 канал
  relay.digitalWrite(3,LOW)                         #   и выключаем 3.
  sleep(.5)                                                       #   Ждём   500 мс.  
