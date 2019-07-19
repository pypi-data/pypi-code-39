import sys
import random
import time
from ftdi_serial import Serial
from north_c9.controller import C9Controller

SERIAL = 'FT2FN5IE'
VERBOSE = False

serial = Serial(device_serial=SERIAL)
controllers = [
    C9Controller(serial, 1, verbose=VERBOSE),
    #C9Controller(serial, 2, verbose=VERBOSE)
]

cycles = 0
errors = 0

messages = [
    lambda c: c.address() == controller.address(),
    lambda c: c.axis_position(0) == 0,
    lambda c: c.ping() or True,
]

while True:
    try:
        for i in range(100):
            for controller in controllers:
                try:
                    method = random.choice(messages)
                    result = method(controller)
                    if not result:
                        errors += 1
                        print('Message Error!', controller._address)
                        print('- cycles', cycles)
                        print('- errors', errors)
                except Exception as err:
                    errors += 1
                    print('Error!', err)
                    print('- cycles', cycles)
                    print('- errors', errors)

        #if cycles % 10 == 0 or cycles == 0:
        #    print()
        #    print(cycles, end=' ')

        cycles += 1
        #print('.', end='')
        #sys.stdout.flush()
    except Exception as err:
        print(err)
        print('- cycles', cycles)
        print('- errors', errors)
