from north_c9.controller import C9Controller
from north_c9.joysticks import N9Joystick

c9 = C9Controller(verbose=True)
c9.home(if_needed=True)
joystick = N9Joystick(c9, moving=True)
