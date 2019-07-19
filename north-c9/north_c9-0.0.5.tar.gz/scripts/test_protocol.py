import threading
import random
from ftdi_serial import Serial
from north_c9.controller import C9Controller

positions = [
    [0, 150, 150],
    [150, 100, 200],
    [-150, -100, 100]
]

running = True

serial = Serial(device_serial='FT2FT5C1')
c9_a = C9Controller(address=1, connection=serial)
c9_b = C9Controller(address=2, connection=serial)


def run_a():
    while running:
        c9_a.ping()
        c9_a.home(if_needed=True, skip=True)
        c9_a.move_arm(*random.choice(positions))


def run_b():
    while running:
        c9_b.info()
        c9_b.home(if_needed=True, skip=True)
        c9_b.move_arm(*random.choice(positions))


thread_a = threading.Thread(target=run_a)
thread_b = threading.Thread(target=run_b)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()

print('done')
