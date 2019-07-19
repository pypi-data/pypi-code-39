import sys
import serial
import minimalmodbus
import pywemo
import time
from datetime import datetime

COMPORT = 'COM30'
SWITCH = 'http://192.168.1.109:49153/setup.xml'

minimalmodbus.BAUDRATE = 115200
minimalmodbus.STOPBITS = 2
minimalmodbus.PARITY = serial.PARITY_NONE
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = False

invalid_responses = 0
cycles = 0

devices = [
    minimalmodbus.Instrument(COMPORT, 4),
    minimalmodbus.Instrument(COMPORT, 5),
]

switch_device = pywemo.discovery.device_from_description(SWITCH, None)


def request(device, method, *args):
    global invalid_responses
    for i in range(0, 10):
        try:
            return getattr(device, method)(*args)

        # retry the message if we run into a recoverable error (up to 9 times)
        except Exception as err:
            if str(err).startswith('Checksum error') or \
                    str(err).startswith('Too short') or \
                    str(err).startswith('No communication') or \
                    str(err).startswith('Wrong return slave'):
                if i >= 9:
                    raise err

                invalid_responses += 1
                print('!', end='')
                sys.stdout.flush()
                # flush the input buffers so minimalmodbus doesn't go out of sync
                device.serial.reset_input_buffer()
            else:
                raise err


def check_devices():
    for device in devices:
        try:
            get_status_word(device)
        except:
            print()
            print('Error communicating with address', device.address)

    print('Device communication successful!')


def start(device, enabled_bits=0):
    set_control_word(device, 6)
    set_control_word(device, 7)
    set_enabled(device, enabled_bits)


def set_enabled(device, enabled_bits=0):
    set_control_word(device, 15 | enabled_bits)


def set_control_word(device, value):
    request(device, 'write_register', 6000, value)


def set_operation_mode(device, value):
    request(device, 'write_register', 6001, value)


def get_status_word(device):
    return request(device, 'read_register', 5000)


def home(device):
    set_operation_mode(device, 6)
    start(device, 1 << 4)
    set_enabled(device)


while True:
    switch_device.on()
    time.sleep(5)

    check_devices()
    test_start = datetime.now()

    try:
        while True:
            for device in devices:
                home(device)

            for i in range(100):
                for device in devices:
                    get_status_word(device)

            #if cycles % 10 == 0 or cycles == 0:
            #    print()
            #    print(cycles, end=' ')

            cycles += 1
            #print('.', end='')
            #sys.stdout.flush()

    except:
        print()
        check_devices()
        print('- duration:', datetime.now() - test_start)
        print('- cycles:', cycles)
        switch_device.off()
        time.sleep(5)