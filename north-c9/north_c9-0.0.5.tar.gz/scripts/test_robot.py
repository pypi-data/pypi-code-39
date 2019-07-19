from PyQt5.QtGui import QVector3D as Vector3
from north_c9.controller import C9Controller
from north_robots.n9 import N9Robot

c9 = C9Controller()
n9 = N9Robot(c9, velocity_counts=20_000, acceleration_counts=50_000)
n9.home()
while True:
    n9.move_to_location(Vector3(50, 150, 150))
    n9.move_to_location([150, 200, 200], order=N9Robot.MOVE_XYZ)
    n9.move_to_location(Vector3(200, 250, 250))
print(n9)
