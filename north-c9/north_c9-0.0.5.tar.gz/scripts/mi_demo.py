import time
import random
import threading
from datetime import datetime
from ftdi_serial import Serial
from north_c9.controller import C9Controller

# DEVICE_SERIAL = 'FT2FN5IE'
DEVICE_SERIAL = None

GRIPPER = 0
ELBOW = 1
SHOULDER = 2
Z = 3

VERBOSE = False
# VERBOSE = True

# TEST_NETWORK = False
TEST_NETWORK = True

# HOME_PUMPS = True
HOME_PUMPS = False

# VELOCITY = 30_000
# ACCELERATION = 30_000
VELOCITY = 40_000
ACCELERATION = 100_000

READ_TIMEOUT = 0.5
# READ_TIMEOUT = 0.3
RETRY_TIMEOUT = 0.3

CLAMP = 1

safe_position = [0, 250, 250]
# next_pipette = [0, 0]
next_pipette = [0, 2]
current_vial = [0, 0]
current_well = [0, 0]
running = True

test_positions = [
    [0, 150, 150],
    [150, 100, 200],
    [-150, -100, 100]
]


def move_safe():
    c9.move_axis(Z, safe_position[2], units=True)
    c9.move_arm(*safe_position)


class WellPlate:
    rows = 12
    cols = 8

    a = [220, 204, 92]
    b = [220, 105, 92]
    c = [157, 105, 92]
    d = [157, 204, 92]

    x_spacing = abs(b[0] - d[0]) / (cols - 1)
    y_spacing = abs(a[1] - b[1]) / (rows - 1)

    @staticmethod
    def position(x, y):
        return [WellPlate.c[0] + x * WellPlate.x_spacing, WellPlate.c[1] + y * WellPlate.y_spacing, WellPlate.c[2]]

    @staticmethod
    def move_to_well():
        c9.use_probe()
        c9.move_arm(*WellPlate.position(*current_well))
        c9.use_probe(False)

    @staticmethod
    def next_well():
        global current_well

        x, y = current_well
        new_x = x + 1
        new_y = y

        if new_x >= WellPlate.cols:
            new_y = y + 1
            new_x = 0

        if new_y >= WellPlate.rows:
            new_x = 0
            new_y = 0

        current_well = [new_x, new_y]

    @staticmethod
    def test_all():
        for i in range(96 * 2):
            WellPlate.move_to_well()
            WellPlate.next_well()


class Pumps:
    axes = [5, 6, 7]
    outputs = [6, 7, 4]

    velocity = 5000
    acceleration = 10000
    max_position = 28000

    @staticmethod
    def home():
        for axis in Pumps.axes:
            c9.move_axis(axis, Pumps.max_position, velocity=Pumps.velocity, acceleration=Pumps.acceleration, relative=True, wait=False)

        c9.wait_for_axes(Pumps.axes)
        c9.home(*Pumps.axes, if_needed=False)

    @staticmethod
    def pull(pump, counts, wait=True, from_pumps=False):
        c9.output(Pumps.outputs[pump], from_pumps)
        c9.move_axis(Pumps.axes[pump], -counts, relative=True, velocity=Pumps.velocity, acceleration=Pumps.acceleration, wait=wait)

    @staticmethod
    def push(pump, counts, wait=True, from_pumps=True):
        c9.output(Pumps.outputs[pump], from_pumps)
        c9.move_axis(Pumps.axes[pump], counts, relative=True, velocity=Pumps.velocity, acceleration=Pumps.acceleration, wait=wait)

    @staticmethod
    def prime(cycles=3):
        for cycle in range(cycles):
            for pump in range(3):
                Pumps.pull(pump, Pumps.max_position, wait=False)

            c9.wait_for_axes(Pumps.axes)

            for pump in range(3):
                Pumps.push(pump, Pumps.max_position, wait=False)

            c9.wait_for_axes(Pumps.axes)

    @staticmethod
    def test():
        Pumps.home()


class Carousel:
    axis = 4
    velocity = 10_000
    acceleration = 50_000

    home_position = 0
    a = 13000
    b = 16000

    @staticmethod
    def move_to_safe_position():
        c9.move_axis(Carousel.axis, 0, velocity=Carousel.velocity, acceleration=Carousel.acceleration)

    @staticmethod
    def move_to_a():
        c9.move_axis(Carousel.axis, Carousel.a, velocity=Carousel.velocity, acceleration=Carousel.acceleration)

    @staticmethod
    def dispense_a(counts):
        Carousel.move_to_a()
        Pumps.pull(1, counts)
        Pumps.push(1, counts)

    @staticmethod
    def dispense_b(counts):
        Carousel.move_to_b()
        Pumps.pull(2, counts)
        Pumps.push(2, counts)

    @staticmethod
    def move_to_b():
        c9.move_axis(Carousel.axis, Carousel.b, velocity=Carousel.velocity, acceleration=Carousel.acceleration)

    @staticmethod
    def test():
        Carousel.move_to_safe_position()
        time.sleep(1)
        Carousel.move_to_a()
        time.sleep(1)
        Carousel.move_to_b()
        time.sleep(1)
        Carousel.move_to_safe_position()


class Vials:
    rows = 3
    cols = 2
    safe_height = 135

    a = [-168, 177, 58]
    b = [-168, 97, 58]
    c = [-208, 97, 58]
    d = [-208, 177, 58]

    clamp = [-187, -13.4, 115]
    clamp_safe = [-187, -13.4, 250]

    clamp_pipette = [-187, -14, 124]
    clamp_pipette_safe = [-187, -14, 200]

    x_spacing = abs(b[0] - d[0]) / (cols - 1)
    y_spacing = abs(a[1] - b[1]) / (rows - 1)

    @staticmethod
    def move_to_safe_height():
        c9.move_axis(Z, Vials.safe_height)

    @staticmethod
    def position(x, y):
        return [Vials.c[0] + x * Vials.x_spacing, Vials.c[1] + y * Vials.y_spacing, Vials.c[2]]

    @staticmethod
    def next_position(x, y):
        new_x = x + 1
        new_y = y

        if new_x >= Vials.cols:
            new_y = y + 1
            new_x = 0

        if new_y >= Vials.rows:
            new_x = 0
            new_y = 0

        return [new_x, new_y]

    @staticmethod
    def next_vial():
        global current_vial
        current_vial = Vials.next_position(*current_vial)

    @staticmethod
    def clamp_state(state=True):
        c9.output(CLAMP, state)
        time.sleep(0.2)

    @staticmethod
    def pull_from_vial(counts):
        c9.use_probe()
        c9.move_arm(*Vials.clamp_pipette_safe)
        c9.move_arm(*Vials.clamp_pipette)
        Pumps.pull(0, counts, from_pumps=True)
        c9.move_arm(*Vials.clamp_pipette_safe)
        c9.use_probe(False)

    @staticmethod
    def pickup(pos):
        c9.use_probe(False)
        c9.move_arm(pos[0], pos[1], Vials.safe_height)
        c9.move_arm(*pos)
        c9.output(GRIPPER, True)
        time.sleep(0.2)
        c9.move_arm(pos[0], pos[1], Vials.safe_height)

    @staticmethod
    def pickup_current():
        Vials.pickup(Vials.position(*current_vial))

    @staticmethod
    def dropoff(pos):
        c9.use_probe(False)
        c9.move_arm(pos[0], pos[1], Vials.safe_height)
        c9.move_arm(*pos)
        c9.output(GRIPPER, False)
        c9.move_axis(Z, -2, units=True, relative=True)
        c9.move_arm(pos[0], pos[1], Vials.safe_height)

    @staticmethod
    def dropoff_current():
        Vials.dropoff(Vials.position(*current_vial))

    @staticmethod
    def uncap_vial():
        c9.use_probe(False)
        c9.move_axis(Z, Vials.clamp_safe[2], units=True)
        c9.move_arm(*Vials.clamp_safe)
        c9.move_arm(*Vials.clamp)
        Vials.clamp_state(True)
        c9.move({
            GRIPPER: -720,  # 2 revolutions / 720 degrees
            Z: 5,  # 5mm
        }, units=True, relative=True)
        c9.move_arm(*Vials.clamp_safe)

    @staticmethod
    def recap_vial():
        c9.use_probe(False)
        c9.move_arm(*Vials.clamp_safe)
        c9.move_arm(Vials.clamp[0], Vials.clamp[1], Vials.clamp[2] + 5)
        c9.move({
            GRIPPER: 720,
            Z: -5
        }, units=True, relative=True)
        Vials.clamp_state(False)
        c9.move_arm(*Vials.clamp_safe)

    @staticmethod
    def test(pos):
        Vials.pickup(pos)
        Vials.uncap_vial()
        Vials.recap_vial()
        Vials.dropoff(pos)

    @staticmethod
    def test_all():
        for i in range(12):
            Vials.pickup_current()
            Vials.uncap_vial()
            Vials.recap_vial()
            Vials.dropoff_current()
            Vials.next_vial()


class PipettesEmpty(Exception):
    pass


class Pipettes:
    rows = 3
    cols = 16
    safe_height = 260

    a = [236, -169, 165]
    b = [236, -187, 165]
    c = [101, -187, 165]
    d = [101, -169, 165]

    x_spacing = abs(b[0] - d[0]) / (cols - 1)
    y_spacing = abs(a[1] - b[1]) / (rows - 1)

    remover_safe = [170, -110, 250]
    remover_approach = [170, -110, 115]
    remover_contact = [170, -119, 115]
    remover_remove = [170, -119, 150]

    @staticmethod
    def move_to_safe_height():
        c9.move_axis(Z, Pipettes.safe_height, units=True)

    @staticmethod
    def position(x, y):
        return [Pipettes.c[0] + x * Pipettes.x_spacing, Pipettes.c[1] + y * Pipettes.y_spacing, Pipettes.c[2]]

    @staticmethod
    def next_position(x, y, auto_refill=False):
        new_x = x + 1
        new_y = y

        if x >= Pipettes.cols - 1:
            new_x = 0
            new_y -= 1

        if new_y < 0:
            # if not auto_refill:
            #     raise PipettesEmpty()

            new_y = Pipettes.rows - 1

        return [new_x, new_y]

    @staticmethod
    def pickup(pos):
        c9.use_probe()
        Pipettes.move_to_safe_height()
        c9.move_arm(pos[0], pos[1], Pipettes.safe_height)
        c9.move_arm(*pos)
        c9.move_arm(pos[0], pos[1], Pipettes.safe_height)
        c9.use_probe(False)

    @staticmethod
    def pickup_next():
        global next_pipette
        Pipettes.pickup(Pipettes.position(*next_pipette))
        next_pipette = Pipettes.next_position(*next_pipette)

    @staticmethod
    def remove():
        c9.use_probe()
        Pipettes.move_to_safe_height()
        c9.move_arm(*Pipettes.remover_safe)
        c9.move_arm(*Pipettes.remover_approach)
        c9.move_arm(*Pipettes.remover_contact)
        c9.move_arm(*Pipettes.remover_remove)
        c9.use_probe(False)

    @staticmethod
    def test(pos):
        Pipettes.pickup(pos)
        Pipettes.remove()

    @staticmethod
    def test_all():
        global next_pipette
        try:
            while True:
                Pipettes.pickup_next()
        except PipettesEmpty:
            pass


def run_a():
    c9_a = C9Controller(address=2, connection=serial, verbose=VERBOSE, read_timeout=READ_TIMEOUT,
                        retry_timeout=RETRY_TIMEOUT)
    c9_a.speed(VELOCITY / 4, ACCELERATION / 4)
    c9_a.home(if_needed=True, skip=True)
    while running:
        c9_a.move_arm(*random.choice(test_positions))


def run_b():
    c9_b = C9Controller(address=3, connection=serial, verbose=VERBOSE, read_timeout=READ_TIMEOUT,
                        retry_timeout=RETRY_TIMEOUT)
    c9_b.speed(VELOCITY / 4, ACCELERATION / 4)
    c9_b.home(if_needed=True, skip=True)
    while running:
        c9_b.move_arm(*random.choice(test_positions))


serial = Serial(device_serial=DEVICE_SERIAL)
c9 = C9Controller(address=1, connection=serial, verbose=VERBOSE, read_timeout=READ_TIMEOUT, retry_timeout=RETRY_TIMEOUT)

thread_a = threading.Thread(target=run_a)
thread_b = threading.Thread(target=run_b)

if TEST_NETWORK:
    thread_a.start()
    thread_b.start()

# c9 = C9Controller(verbose=True)
start_time = time.time()
c9.home(if_needed=True)
if time.time() - start_time > READ_TIMEOUT:
    time.sleep(5)
if HOME_PUMPS:
    Pumps.home()
print(f'Test start: {datetime.now()}')
# Pumps.prime()
c9.speed(VELOCITY, ACCELERATION)
c9.output(GRIPPER, False)
c9.output(CLAMP, False)

amount = 2000
while True:
    Vials.pickup_current()
    Vials.uncap_vial()
    Carousel.dispense_a(amount)
    Carousel.dispense_b(amount)
    Carousel.move_to_safe_position()
    Pipettes.pickup_next()
    Vials.pull_from_vial(amount * 2)
    WellPlate.move_to_well()
    Pumps.push(0, amount * 2, from_pumps=True)
    Pipettes.remove()
    Vials.recap_vial()
    Vials.dropoff_current()

    Vials.next_vial()
    WellPlate.next_well()

