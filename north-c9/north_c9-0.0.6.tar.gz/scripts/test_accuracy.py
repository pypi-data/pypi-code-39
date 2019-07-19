import time
from north_c9.controller import C9Controller

c9 = C9Controller()
c9.home()

test_position = [-140, 200, 100]
test_position2 = [-155, 200, 100]
positions = [
    [-100, 200, 100],
    [100, 200, 100],
    [-50, 150, 200]
]
last_home_time = 0
home_interval = 30 * 60  # 30 minutes
axis1_home_position = 0
axis1_motor_position = 0
drift = 0
moves = 0

def home():
    global last_home_time
    global axis1_home_position
    if time.time() - last_home_time > home_interval:
        #c9.home()
        last_home_time = time.time()
        #axis1_home_position = c9.axis_position(0, motor=True)

def check_position():
    time.sleep(1)
    nanotec_pos = c9.axis_positions(0, 1, 2, 3, test=True)
    print(nanotec_pos)

while True:
    #home()
    c9.move_arm(*test_position, 0)
    c9.move_arm(*test_position2, 0)
    moves += 2
    check_position()
    #last_axis1_motor_position = axis1_motor_position or (c9.axis_position(0, motor=True) - axis1_home_position) / 4
    #axis1_motor_position = (c9.axis_position(0, motor=True) - axis1_home_position) / 4
    #drift = axis1_motor_position - last_axis1_motor_position
    #print('Axis 1 motor position:', axis1_motor_position)
    #print('C9 position:', c9.axis_position(1))
    #print('Drift:', drift)
    #print()

    time.sleep(5)
    for pos in positions:
        for x in range(0, 100, 1):
            c9.move_arm(pos[0] + x, pos[1], pos[2], 0)
            #print(pos[0] + x, pos[1], pos[2])
            #print(c9.axis_position(1))
            #print()
            #moves += 1
            #check_position()