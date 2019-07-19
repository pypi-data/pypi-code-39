import time
from north_c9.robot import N9Robot

n9 = N9Robot()
n9.home()
elbow_motor_home_pos = n9.controller.axis_position(0, motor=True)

n9.column.move_mm(100, wait=False)
n9.elbow.move_degrees(0, wait=False)
n9.shoulder.move_degrees(0)

n9.elbow.move_degrees(-45)
elbow_motor_pos = n9.controller.axis_position(0, motor=True)
drift = 0

while True:
    time.sleep(5)
    n9.elbow.move_degrees(-40)
    for i in range(-40, 45):
        n9.elbow.move_degrees(i)

    n9.elbow.move_degrees(-45)

    elbow_pos = n9.controller.axis_position(0, motor=True)
    drift = elbow_pos - elbow_motor_pos
    diff = n9.elbow.position_counts - (elbow_pos - elbow_motor_home_pos)
    print('Drift: ', drift)
    print()