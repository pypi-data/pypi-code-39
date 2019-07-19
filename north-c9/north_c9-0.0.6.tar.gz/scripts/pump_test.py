from time import sleep
from north_c9.controller import C9Controller
from north_c9.joints import PrismaticJoint

controller = C9Controller(verbose=True)
#controller.move_axis(4, 20000, 50000, -10 * 1000)
controller.output(0, True)
sleep(1)
controller.output(0, False)
print('finished')