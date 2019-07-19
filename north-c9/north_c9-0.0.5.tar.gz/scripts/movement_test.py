import time
from north_c9.controller import C9Controller
from north_c9.robot import N9Robot
from north_c9.util import Vector3

controller = C9Controller()
controller.home()
robot = N9Robot(controller)

robot.move_to_location(Vector3(200, 200, 300))
time.sleep(2)
robot.move_to_location(Vector3(-150, 200, 300))
print(robot.configuration)