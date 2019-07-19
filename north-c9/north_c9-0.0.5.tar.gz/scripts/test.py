import time
from north_c9.controller import C9Controller

VELOCITY = 5000
ACCELERATION = 50000

start = 60
stroke = 15
paused = True

c9 = C9Controller(device_serial='A505PD7K')
#c9.home()

#c9.move_axis(1, 0, units=True)
#c9.move_axis(2, 0, units=True)


def parse_speed(key):
    global VELOCITY
    try:
        speed = int(key)
        if speed == 0:
            speed = 10

        VELOCITY = 5000 + (speed - 1) * 4000
    except:
        return None


def parse_stroke(key):
    global stroke
    if key == '=':
        stroke += 5
    elif key == '-':
        stroke -= 5


def pause():
    key = input()
    parse_speed(key)
    parse_stroke(key)

    print(VELOCITY, stroke)


while True:
    #c9.move_arm(*n9_deck.J9.to_list(), velocity=VELOCITY, acceleration=ACCELERATION, wait=True)
    pause()
    #c9.move_axis(*n9_deck.N14.to_list(), velocity=VELOCITY, acceleration=ACCELERATION, wait=True)
    pause()