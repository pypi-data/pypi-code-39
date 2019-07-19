from north_c9.controller import C9Controller
from north_c9.joints import Axis

c9 = C9Controller()

pump = Axis(4, velocity_counts=100, acceleration_counts=100, max_position_counts=30000, home_reversed=True,
            max_current=400)
pump.home()