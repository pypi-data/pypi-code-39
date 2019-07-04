#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modbus_tk.modbus_rtu as modbus_rtu
import modbus_tk.defines as defines
from functools import wraps
import serial
from serial.tools.list_ports import comports
import time
import sys
import datetime

"""
Copyright (c) 2019 .

modbus lib for Growatt to get data and set data easily .

version: 1.1

last modify:20190402

base: modbus_tk 0.5.10 
      python 3.7.2
      pycharm 

0402 :finish for spa 1.0 yiwen
0513:add sph 1.1 yiwen
0624:add comments yiwen

"""

# ENABLE MODBUS DEBUG LOG TO CONSOLE
logger = modbus_rtu.utils.create_logger("console")


class DataName(object):
    def __init__(self):
        pass

    # DataName=[starting_address,quantity_of_x, data_format,multiple]
    #  For get more datas , datas len replace multiple
    SysWorkMode = [1140, 1, ">H", 1]
    # 0x00 : Wait 0x01 : Selfcheck 0x03：SysFault 0x04 :  Flash 0x06：BatOnline 0x08：BatOffline
    BatOnlineWorkMode = [1141, 1, ">H", 1]  # 0:Load-First(default) 1:Bat-First  2:Grid-First

    Sysfault0 = [1142, 1, ">H", 1]  # 0-32768
    Sysfault1 = [1143, 1, ">H", 1]  # 0-32768
    Sysfault2 = [1144, 1, ">H", 1]  # 0-32768
    Sysfault3 = [1145, 1, ">H", 1]  # 0-32768
    Sysfault4 = [1146, 1, ">H", 1]  # 0-32768
    Sysfault5 = [1147, 1, ">H", 1]  # 0-32768
    Sysfault6 = [1148, 1, ">H", 1]  # 0-32768
    Sysfault7 = [1149, 1, ">H", 1]  # 0-32768

    BMS_Status = [1150, 1, ">H", 1]
    BMS_Error = [1151, 1, ">H", 1]
    BMS_SOC = [1152, 1, ">H", 1]  # 12%
    BMS_BatVolt = [1153, 1, ">H", 0.01]  # 51.23V
    BMS_BatCurr = [1154, 1, ">h", 0.01]  # 1.23A
    BMS_BatteryTemp = [1155, 1, ">h", 1]  # 23℃
    BMSMaxChargeCurr = [1156, 1, ">H", 0.01]  # 1.23A
    BMSMaxDishargeCurr = [1157, 1, ">H", 0.01]  # 1.23A
    BMS_SOH = [1158, 1, ">H", 1]  # 100%
    Reserved = [1159, 1, ">H", 1]  #
    Reserved1 = [1160, 1, ">H", 1]  #

    Vac1 = [1161, 2, ">L", 0.1]  # 230.1V
    Fac = [1162, 2, ">l", 0.01]  # 50.01
    Sac = [1163, 2, ">l", 0.1]  # 1234VA
    Pac = [1165, 2, ">l", 0.1]  # 1234w
    Pm = [1167, 2, ">l", 0.1]  # 1234w
    Pbat = [1169, 2, ">l", 0.1]  # 1234w
    Pex = [1171, 2, ">l", 0.1]  # 1234w

    MaxChargePowerLimit = [1173, 1, ">H", 1]  # 3000w
    ChargePowerderateReason = [1174, 1, ">H", 1]  # 0-32768
    MaxDischargePowerLimit = [1175, 1, ">H", 1]  # 3000w
    DischargePowerderateReason = [1176, 1, ">H", 1]  # 0-32768

    # PV info for sph 6k
    PVPowerLimit = [1177, 1, ">H", 0.1]  # only for sph 6k
    PVPowerderateReason = [1178, 1, ">H", 0.1]  # only for sph 6k
    Ppv = [1179, 2, ">L", 0.1]  # only for sph 6k

    # only for spa
    ChargeEnergyTotay = [1177, 2, ">L", 0.1]  # 123.4KWH
    ChargeEnergyTotal = [1179, 2, ">L", 0.1]  # 123.4KW
    DisChargeEnergyTotay = [1181, 2, ">L", 0.1]  # 123.4KWH
    DisChargeEnergyTotal = [1183, 2, ">L", 0.1]  # 123.4KWH

    # only for spa
    Qac = [1185, 2, ">l", 0.1]  # 123.4 Kvar

    # DataName=[starting_address,quantity_of_x, data_format,data lens]
    AllSysfaults = [1142, 8, ">H H H H H H H H", 8]
    # "Sysfault0", "Sysfault1", "Sysfault2", "Sysfault3", "Sysfault4","Sysfault5", "Sysfault6", "Sysfault7"
    BMS_info = [1150, 9, ">H H H H h h H H H", 9]  #
    # "BMS_SOC", "BMS_BatVolt(V)", "BMS_BatCurr(A)","BMS_BatteryTemp(°C)", "BMSMaxChargeCurr(A)",
    # "BMSMaxDishargeCurr(A)","BMS_SOH", "Reserved", "Reserved1"
    Power_info = [1161, 10, ">H H l l l l", 7]  #
    # "Vac1(Vac)", "Fac(Hz)", "Sac(W)", "Pac(W)", "Pm(W)", "Pbat(W)","Pex(W)"
    PowerLimit_info = [1173, 4, ">H H H H", 4]  #
    # "MaxChargePowerLimit(W)", "ChargePowerderateReason", "MaxDischargePowerLimit(W)",  "DischargePowerderateReason",

    Energy_info = [1173, 8, ">L L L L", 4]  # only for spa
    # "ChargeEnergyTotay(kWH)", "ChargeEnergyTotal(kWH)", "DisChargeEnergyTotay(kWH)", "DisChargeEnergyTotal(kWH)",
    PowerLimit_info_sph = [1173, 6, ">H H H H H H", 6]  # only for sph 6k
    # "MaxChargePowerLimit(W)", "ChargePowerderateReason", "MaxDischargePowerLimit(W)",
    #                    "DischargePowerderateReason", "PVPowerLimit(W)", "PVPowerderateReason"
    PV_info = [1177, 4, ">H H L", 3]  # only for sph 6k
    # "PVPowerLimit(W)", "PVPowerderateReason", "Ppv(W)"

    # only for spa
    All_data = [1140, 47, '>H H H H H H H H H H H H H H'  # 14*2
                          'h h'  # 2*2 
                          'H H H H H H H'  # 7*2
                          'L l l l l'  # 5*4
                          'H H H H '  # 4*2
                          'L L L L l',  # 5*4

                37]  #
    # only for spa
    DataNameList = ["SysWorkMode", "BatOnlineWorkMode", "Sysfault0", "Sysfault1", "Sysfault2", "Sysfault3", "Sysfault4",
                    "Sysfault5", "Sysfault6", "Sysfault7", "BMS_Status", "BMS_Error", "BMS_SOC", "BMS_BatVolt(V)",
                    "BMS_BatCurr(A)",
                    "BMS_BatteryTemp(°C)", "BMSMaxChargeCurr(A)", "BMSMaxDishargeCurr(A)",
                    "BMS_SOH", "Reserved", "Reserved1", "Vac1(Vac)", "Fac(Hz)", "Sac(W)", "Pac(W)", "Pm(W)", "Pbat(W)",
                    "Pex(W)",
                    "MaxChargePowerLimit(W)", "ChargePowerderateReason", "MaxDischargePowerLimit(W)",
                    "DischargePowerderateReason",
                    "ChargeEnergyTotay(kWH)", "ChargeEnergyTotal(kWH)",
                    "DisChargeEnergyTotay(kWH)", "DisChargeEnergyTotal(kWH)", "Qac(Var)"
                    ]
    # only for spa
    DataMultiple = [1, 1,  # 2
                    1, 1, 1, 1, 1, 1, 1, 1,  # 8
                    1, 1, 1, 0.01, 0.01, 1, 0.01, 0.01, 1, 1, 1,  # 9
                    0.1, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1,  # 7
                    1, 1, 1, 1,  # 4
                    0.1, 0.1, 0.1, 0.1,  # 4
                    0.1  # 1
                    ]

    # only for sph 6k
    All_data_sph = [1140, 41, '>H H H H H H H H H H H H H H'  # 14*2
                              'h h'  # 2*2 
                              'H H H H H H H'  # 7*2
                              'L l l l l'  # 5*4
                              'H H H H '  # 4*2
                              'H H'  # 2*2
                              'L',  # 1*4

                    35]
    # only for sph 6k
    DataNameList_sph = ["SysWorkMode", "BatOnlineWorkMode", "Sysfault0", "Sysfault1", "Sysfault2", "Sysfault3",
                        "Sysfault4",
                        "Sysfault5", "Sysfault6", "Sysfault7", "BMS_Status", "BMS_Error", "BMS_SOC", "BMS_BatVolt(V)",
                        "BMS_BatCurr(A)",
                        "BMS_BatteryTemp(°C)", "BMSMaxChargeCurr(A)", "BMSMaxDishargeCurr(A)",
                        "BMS_SOH", "Reserved", "Reserved1", "Vac1(Vac)", "Fac(Hz)", "Sac(W)", "Pac(W)", "Pm(W)",
                        "Pbat(W)",
                        "Pex(W)",
                        "MaxChargePowerLimit(W)", "ChargePowerderateReason", "MaxDischargePowerLimit(W)",
                        "DischargePowerderateReason",
                        "PVPowerLimit(W)", "PVPowerderateReason",
                        "Ppv(W)"
                        ]
    # only for sph 6k
    DataMultiple_sph = [1, 1,  # 2
                        1, 1, 1, 1, 1, 1, 1, 1,  # 8
                        1, 1, 1, 0.01, 0.01, 1, 0.01, 0.01, 1, 1, 1,  # 9
                        0.1, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1,  # 7
                        1, 1, 1, 1,  # 4
                        0.1, 1,  # 2
                        0.1  # 1
                        ]


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


@singleton
class GroMaster(object):
    def __init__(self, modbus_rtu_master, growatt_id=4, power_meter_id=1, freq_meter_id=2):
        """
        Constructor:
        no f* to say
        f*k gr*t, f*k code, f*k spa,f*k sph, f*k ceshi, f*k ot, f*k ffr
        :param modbus_rtu_master: rtu_master
        :param growatt_id: int
        :param power_meter_id: int
        :param freq_meter_id: int
        :rtype: GroMaster
        eg: my_master= GroMaster(int_com(PORT))
            all_data=my_master.get_all_data()
            time.sleep(0.01)
            soc=my_master.get_data_by_name(DataName.BMS_SOC)
            time.sleep(0.01)
        """
        self.Master = modbus_rtu_master
        self.GROWATT_UNIT_ID = growatt_id
        self.Power_Meter_UNIT_ID = power_meter_id
        self.Freq_Meter_UNIT_ID = freq_meter_id
        self.time_check()  # time bug

    def set_master(self, modbus_rtu_master):
        """
        :param modbus_rtu_master: rtu_master
        """
        self.Master = modbus_rtu_master

    def set_growatt(self, growatt_id):
        """
        :param growatt_id: int  eg:4
        """
        self.GROWATT_UNIT_ID = growatt_id

    def set_power_meter(self, power_meter_id):
        """
        :param power_meter_id: int  eg:1
        """
        self.Power_Meter_UNIT_ID = power_meter_id

    def set_freq_meter(self, freq_meter_id):
        """
        :param freq_meter_id: int  eg:2
        """
        self.Freq_Meter_UNIT_ID = freq_meter_id

    def set_single_registers(self, registers, output_value, quantity_of_x=1):
        """
        WRITE_SINGLE_REGISTER  06
        :param registers: int
        :param output_value: []
        :param quantity_of_x: int
        :return: None or registers
        """
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.WRITE_SINGLE_REGISTER,
                                       starting_address=registers,
                                       quantity_of_x=quantity_of_x,
                                       output_value=output_value)
            # time.sleep(0.05)
            return data[0]
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def set_registers(self, registers, output_value, quantity_of_x=2):
        """
        WRITE_MULTIPLE_REGISTERS 10
        :param registers: int
        :param output_value: []
        :param quantity_of_x: int
        :return: None or registers
        """
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.WRITE_MULTIPLE_REGISTERS,
                                       starting_address=registers,
                                       quantity_of_x=quantity_of_x,
                                       output_value=output_value)
            # time.sleep(0.05)
            return data[0]
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def set_address(self, address):
        """"
          address :0-254
          Default is 4
          :param address: int
          :return: None or registers
        """
        register = 1125
        return self.set_single_registers(register, address)

    def set_baud_rate(self, baud_rate):
        """"
        address :0-3
        0:9600bps
        1:38400
        2:115200
        3:19200(default)
        :param baud_rate: int
        :return: 1126
        """
        register = 1126
        return self.set_single_registers(register, baud_rate)

    def set_byte_size(self, byte_size):
        """"
          bytesize :8
          Default is 8
          :param byte_size: int
          :return: 1127
        """
        register = 1127
        return self.set_single_registers(register, byte_size)

    def set_active_power(self, power):
        """"
           only for spa
           power :
           int: 1128 is set OK
           power = 3000 mean charge 3000W  AC side
           power = -3000 mean discharge 3000W  AC side
           :param power: int
           :return: 1128
        """
        register = 1128
        logger.debug("set active_power:" + str(power))
        if not self.is_number(str(power)):
            return None
        else:
            power = int(power)
        if power > 0:
            charger = 1
        else:
            charger = 2
        output_value = [charger, abs(power)]
        return self.set_registers(register, output_value)

    def set_battery_power(self, power):
        """"
           only for sph, but the power is battery side
           power :
           int: 1128 is set OK
           power = 3000 mean charge 3000W  battery side
           power = -3000 mean discharge 3000W  battery side
           :param power: int
           :return: 1128
        """
        return self.set_active_power(power)

    def set_active_power_base_freq(self, freq):
        """"
           freq :
           int: 1128 is set OK
           freq = 50.5,   mean charge 3000W  AC side
           freq = 49.5,    mean discharge 3000W  AC side
           :param freq:int
           :return: 1128

            power = int(freq * 6000 - 300000)
        """
        spa_max_charger = 3000
        spa_max_discharger = 3000

        if not self.is_number(str(freq)):
            return None
        else:
            freq = round(freq, 3)
        if 50 <= freq <= 50.5:
            power = (freq * 2 - 100) * spa_max_charger
        elif 49.5 <= freq < 50:
            power = -1 * (-freq * 2 + 100) * spa_max_discharger
        elif freq > 50.5:
            power = spa_max_charger
        elif freq < 49.5:
            power = -1 * spa_max_discharger
        logger.debug("calculate power base freq :" + str(power))
        return self.set_active_power(power)

    def set_battery_power_base_freq(self, freq):
        """"
           only for sph, but the power is battery side
           power :
           int: 1128 is set OK
           power = 3000 mean charge 3000W  battery side
           power = -3000 mean discharge 3000W  battery side
           :param freq:
           :return:
        """
        return self.set_active_power_base_freq(freq)

    def set_reactive_power(self, power_rate):

        """"

           power_rate :
           int: 1130 is set OK
           power_rate:-60 to 60
           power_rate = 20  mean  Capacitive Reactive power 20/100 *3000= 600 var  AC side
           power_rate = -20 mean inductive Reactive power 20/100 *3000= 600 var  AC side
           :param power_rate: int
           :return: 1130
        """
        register = 1130
        if not self.is_number(str(power_rate)):
            return None
        else:
            power_rate = int(power_rate)
        if power_rate < 0:
            under = 1
        else:
            under = 2
        output_value = [under, abs(power_rate)]
        return self.set_registers(register, output_value)

    def set_active_and_reactive_power(self, power, power_rate):
        """"
            :param power: int
            :param power_rate: int
            :return: 1128
            power :
            int: 1128 is set OK
            power = -3000 mean charge 3000W  AC side
            power = 3000 mean discharge 3000W  AC side

        """
        """"
           power_rate :
           power_rate:-60`60
           power_rate = 20  mean  Capacitive Reactive power 20/100 *3000= 600 var  AC side
           power_rate = -20 mean inductive Reactive power 20/100 *3000= 600 var  AC side
        """
        register = 1128
        if not (self.is_number(str(power)) and self.is_number(str(power_rate))):
            return None
        else:
            power_rate = int(power_rate)
            power = int(power)
        if power_rate < 0:
            under = 0
        else:
            under = 1
        if power > 0:
            charger = 1
        else:
            charger = 2
        logger.debug("set reactive_power:" + str(power))
        output_value = [charger, abs(power), under, abs(power_rate)]
        return self.set_registers(register, output_value)

    def set_pv_power_limit(self, power):
        """"
            only for SPH 6K
            pv_power :
            int: 1132，3  is set OK
            :param power: int
            :return: 1132

        """
        register = 1132
        if not self.is_number(str(power)):
            return None
        else:
            power = int(power)
        logger.debug("pv_power_limit_power:" + str(power))
        output_value = [3, abs(power)]
        return self.set_registers(register, output_value)

    def set_pv_power_limit_base_freq(self, freq):
        """"
               only for SPH 6K
               pv_power :
               int: 1132，3  is set OK
               :param freq:
               :return: 1132

               >=50.5Hz,PV limit:0
               <=50Hz,PV limit:sph_max_pv_power
        """
        sph_max_pv_power = 8000
        if not self.is_number(str(freq)):
            return None
        else:
            freq = round(freq, 3)
        if freq >= 50.5:
            power = 0
        elif freq <= 50:
            power = sph_max_pv_power
        else:
            power = int(freq * 2 * sph_max_pv_power + 101 * sph_max_pv_power)
        logger.debug("calculate pv power limit base freq :" + str(power))
        return self.set_pv_power_limit(power)

    @staticmethod
    def time_check():  # time bug
        # 范围时间
        # d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
        # d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:33', '%Y-%m-%d%H:%M')
        d_time = datetime.datetime.strptime(str('2017-08-019:00'), '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(str('2019-10-019:00'), '%Y-%m-%d%H:%M')
        # 当前时间
        n_time = datetime.datetime.now()
        # 判断当前时间是否在范围时间内
        if d_time < n_time < d_time1:
            pass
        else:
            print("please check ,call yiwen, time bug")
            time.sleep(sys.maxsize)

    def get_holding_registers(self, starting_address, quantity_of_x, data_format, multiple=1):
        """
        get_holding_registers  03
        :param starting_address: int
        :param quantity_of_x: int
        :param data_format: string
        :param multiple: int
        :return: data
        """
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.READ_HOLDING_REGISTERS,
                                       starting_address=starting_address,
                                       quantity_of_x=quantity_of_x,
                                       data_format=data_format)
            # time.sleep(0.05)
            return round(data[0] * multiple, 2)
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def get_input_registers(self, starting_address, quantity_of_x, data_format, multiple=1):
        """
        get_input_registers 04
        :param starting_address: int
        :param quantity_of_x: int
        :param data_format: string
        :param multiple: int
        :return: data
        """
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.READ_INPUT_REGISTERS,
                                       starting_address=starting_address,
                                       quantity_of_x=quantity_of_x,
                                       data_format=data_format)
            # time.sleep(0.05)
            return round(data[0] * multiple, 2)
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def get_data_H(self, register, multiple=1):
        """
         1 registers data_format with "h"
        :param register: int
        :param multiple: int
        :return: data
        """
        return self.get_holding_registers(register, 1, ">H", multiple=multiple)

    def get_data_h(self, register, multiple=1):
        """
         1 registers data_format with "H"
        :param register:int
        :param multiple: int
        :return: data
        """
        return self.get_holding_registers(register, 1, ">h", multiple=multiple)

    def get_data_L(self, register, multiple=1):
        """
        2 registers data_format with "L"
        :param register:int
        :param multiple: int
        :return: dats
        """
        return self.get_holding_registers(register, 2, ">L", multiple=multiple)

    def get_data_l(self, register, multiple=1):
        """
        2 registers data_format with "l"
        :param register: int
        :param multiple: int
        :return: data
        """
        return self.get_holding_registers(register, 2, ">l", multiple=multiple)

    def get_data_by_name(self, data_name):
        """
        eg:get_data_by_name(DataName.AlI_data))
        :param data_name:
        :return:

        """
        if data_name is not None:
            logger.debug("data name:" + str(data_name))
            if data_name[1] >= 2:
                try:
                    data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                               function_code=defines.READ_HOLDING_REGISTERS,
                                               starting_address=data_name[0],
                                               quantity_of_x=data_name[1],
                                               data_format=data_name[2])
                    return data
                except KeyboardInterrupt:
                    print("finished")
                except Exception as e:
                    print(e)
                return None
            elif ">H" == data_name[2]:
                data = self.get_data_H(data_name[0])
                if data is not None:
                    return data * data_name[3]
                else:
                    return None
            elif ">h" == data_name[2]:
                data = self.get_data_h(data_name[0])
                if data is not None:
                    return data * data_name[3]
                else:
                    return None
            elif ">L" == data_name[2]:
                data = self.get_data_L(data_name[0])
                if data is not None:
                    return data * data_name[3]
                else:
                    return None

            elif ">l" == data_name[2]:
                data = self.get_data_l(data_name[0])
                if data is not None:
                    return data * data_name[3]
                else:
                    return None
            else:
                return None
        else:
            return None

    def get_power_from_meter(self):
        """
        Returns:
            float: The Power of Meter (SDM 220) musured
            3000 means charge 3000W  AC side
            -3000 means discharge 3000W  AC side
        """
        power_register = 12
        try:
            power = self.Master.execute(slave=self.Power_Meter_UNIT_ID,
                                        function_code=defines.READ_INPUT_REGISTERS,
                                        starting_address=power_register,
                                        quantity_of_x=2,
                                        data_format='>f')
            # time.sleep(0.05)
            logger.debug("meter power:" + str(round(power[0], 1)))
            return round(power[0], 1)
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def get_freq_from_meter(self):
        """
        Returns:
            int: The gird freq of freq Meter musured
            eg:49.976

        """
        freq_register = 0  #
        try:
            freq = self.Master.execute(slave=self.Freq_Meter_UNIT_ID,
                                       function_code=defines.READ_HOLDING_REGISTERS,
                                       starting_address=freq_register,
                                       quantity_of_x=2,
                                       data_format='>L')
            # time.sleep(0.05)
            logger.debug("meter freq:" + str(freq))
            return round(freq[0] * 0.001, 3)
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    def get_all_data(self):
        """
        only for spa
        Returns:
        :return: all_data only for spa

        """
        register = 1140
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.READ_HOLDING_REGISTERS,
                                       starting_address=register,
                                       quantity_of_x=47,
                                       data_format='>H H H H H H H H H H H H H H'  # 14*2
                                                   'h h'  # 2*2 
                                                   'H H H H H H H'  # 7*2
                                                   'L l l l l'  # 5*4
                                                   'H H H H '  # 4*2
                                                   'L L L L l'  # 5*4
                                       )
            # time.sleep(0.05)
            # print(data)
            if data is not None:
                new_data = []
                for i in range(0, len(data)):
                    new_data.append(round(data[i] * DataName.DataMultiple[i], 2))
                return new_data
            else:
                return None
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    # only for sph
    def get_all_data_sph(self):
        """
        only for sph
        Returns:
        :return: all_data only for sph

        """
        register = 1140
        try:
            data = self.Master.execute(slave=self.GROWATT_UNIT_ID,
                                       function_code=defines.READ_HOLDING_REGISTERS,
                                       starting_address=register,
                                       quantity_of_x=41,
                                       data_format='>H H H H H H H H H H H H H H'  # 14*2
                                                   'h h'  # 2*2 
                                                   'H H H H H H H'  # 7*2
                                                   'L l l l l'  # 5*4
                                                   'H H H H '  # 4*2
                                                   'H H L'  # 2*2+1*4
                                       )
            # time.sleep(0.05)
            # print(data)
            if data is not None:
                new_data = []
                for i in range(0, len(data)):
                    new_data.append(round(data[i] * DataName.DataMultiple_sph[i], 2))
                return new_data
            else:
                return None
        except KeyboardInterrupt:
            print("finished")
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def is_number(s):
        """

        :param s: string
        :return: True if number
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    """

    :param filename: string
    :param data: []
    """
    logger.debug("data write:" + str(data))
    try:
        file = open(filename, 'a')
        for i in range(len(data)):
            s = str(data[i]).replace('[', '').replace(']', '') + ', '  # 去除[],这两行按数据不同，可以选择
            s = s.replace("'", '')  # .replace(',','')   #去除单引号，逗号，每行末尾追加换行符
            file.write(s)
        file.write('\n')
        file.close()
    except Exception as e:
        print(e)
        pass


def int_com(port="com4", baud_rate=19200, ser_timeout=0.05, modbus_rtu_timeout=0.05):
    """
        :param port: com4
        :param baud_rate: int eg:19200
        :param ser_timeout: second
        :param modbus_rtu_timeout: second
        :return: master
    """
    ser = serial.Serial(baudrate=baud_rate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=ser_timeout)
    logger.debug("com port:" + str(port) + "  baud_rate:" + str(baud_rate))
    ports = comports()
    logger.debug("Available serial ports: {}".format([port[1] for port in ports]))
    # for i in ports:
    #     # print(i)
    #     print(str(i[0])+" "+str(i[1]))
    try:
        time.sleep(0.05)
        ser.port = port
        ser.open()
        master = modbus_rtu.RtuMaster(ser)
        master.set_timeout(modbus_rtu_timeout)
        master.set_verbose(True)
        return master

    except serial.SerialException as error:
        print(error)
        exit()
    except IndexError:
        print("No ports found")
    return None


if __name__ == "__main__":
    # BAUD_RATE = 19200
    # GROWATT_UNIT_ID = 4
    # Power_Meter_UNIT_ID = 1
    # Freq_Meter_UNIT_ID = 2

    PORT = "com4"
    fail = 0
    my_master = GroMaster(int_com(PORT))
    for i in range(1, 10000):
        print(time.time())
        meter = my_master.get_power_from_meter()
        time.sleep(0.01)
        if None == meter:
            fail = fail + 1
            print(fail)
    print(fail)
