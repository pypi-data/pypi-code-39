import time
import math
import pygame
from north_c9.controller import C9Controller, C9Error
from ftdi_serial import SerialReadTimeoutException

pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

c9 = C9Controller(verbose=False)
c9.home(if_needed=True)

c9.elbow_bias(C9Controller.BIAS_CLOSEST)

print('READY')

wait_time = 0.1
delta = 10
max_delta = 100
min_delta = 0.5
max_velocity = 20000
gripper_scale = 100
z_scale = 0.5
probe_length = 41.5
probe_enabled = False

last_close = 0
last_swap = 0
last_speed_up = 0
last_speed_down = 0
last_print_position = 0
last_toggle_probe = 0
gripper_closed = False


def sign(value):
    if value < 0:
        return -1

    return 1


def deadzone(value, amount=0.02):
    if abs(value) < amount:
        return 0
    return scale(value)


def scale(value, base=20):
    return base ** abs(value) / base ** 1 * sign(value)


while True:
    x = joystick.get_axis(0)
    y = joystick.get_axis(1)
    z = joystick.get_axis(3)
    gripper = joystick.get_axis(2)
    close = joystick.get_button(1)  # B
    swap = joystick.get_button(3)  # X
    speed_down = joystick.get_button(8)  # L2
    speed_up = joystick.get_button(9)  # R2
    gripper_left = joystick.get_button(6)  # L1
    gripper_right = joystick.get_button(7)  # R1
    print_position = joystick.get_button(11)  # start
    toggle_probe = joystick.get_button(10)  # select

    dpad = joystick.get_hat(0)

    x_delta = -delta * deadzone(x) - dpad[0] * delta / 5
    y_delta = delta * deadzone(y) - dpad[1] * delta / 5
    z_delta = -delta * deadzone(z) * z_scale
    #gripper_delta = delta * deadzone(gripper) * gripper_scale - gripper_left * delta / 5 + gripper_right * delta / 5
    gripper_delta = (gripper_left * delta / 5 - gripper_right * delta / 5) * gripper_scale
    velocity = max_velocity * math.sqrt(deadzone(x)**2 + deadzone(y)**2) + 1
    #print(x_delta, y_delta, velocity)

    if last_close == 0 and close == 1:
        gripper_closed = not gripper_closed
        c9.output(0, gripper_closed)

    if last_swap == 0 and swap == 1:
        c9.swap_elbow()

    if last_speed_down == 0 and speed_down == 1:
        delta = max(delta / 2, min_delta)

    if last_speed_up == 0 and speed_up == 1:
        delta = min(delta * 2, max_delta)

    if print_position == 0 and last_print_position == 1:
        print('Position:', *c9.cartesian_position())

    if toggle_probe == 0 and last_toggle_probe == 1:
        probe_enabled = not probe_enabled
        if probe_enabled:
            print('Probe ON')
            c9.elbow_length(probe_length)
        else:
            print('Probe OFF')
            c9.elbow_length(0)

    try:
        c9.move_arm(x_delta, y_delta, z_delta, velocity=max_velocity, acceleration=max_velocity * 2,
                    relative=True)
        c9.move_axis(0, gripper_delta, relative=True, velocity=20000, acceleration=40000)
    except Exception as err:
        if isinstance(err, SerialReadTimeoutException) or \
           isinstance(err, C9Error) and err.error_number == C9Error.TIMEOUT:
            print('Timeout')

    last_close = close
    last_swap = swap
    last_speed_down = speed_down
    last_speed_up = speed_up
    last_print_position = print_position
    last_toggle_probe = toggle_probe
    pygame.event.pump()