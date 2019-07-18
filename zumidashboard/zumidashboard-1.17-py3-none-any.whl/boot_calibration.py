'''
#Testing calibration code
import smbus #for I2C communication
#import RPi.GPIO as GPIO #for the Pin Input reading
from PIL import Image
'''
import time
from zumi.zumi import Zumi
from zumi.util.screen import Screen
import zumidashboard.scripts as scripts
import os
import subprocess
from socket import gethostname
import zumidashboard.sounds as sound


def _start_threading(*args):
    for thread in args:
        thread.start()
    time.sleep(1)
    for thread in args:
        thread.join()


def _average(lst):
    sum_value = 0
    for data in lst:
        sum_value += data
    avg = sum_value / len(lst)
    return avg


def _calibrated_sound(zumi):
    tempo = 60
    zumi.play_note(41, tempo)
    zumi.play_note(43, tempo)
    zumi.play_note(45, tempo)


def _happy_sound(zumi):
    time.sleep(1)
    tempo = 75
    zumi.play_note(Note.C5, tempo)
    zumi.play_note(Note.G5, tempo)
    zumi.play_note(Note.E5, tempo)
    time.sleep(0.5)


def _try_calibrate_sound(zumi):
    for i in range(2):
        tempo = 75
        zumi.play_note(Note.G5, tempo)
        time.sleep(0.1)
        zumi.play_note(Note.G5, tempo)
        time.sleep(0.1)
        zumi.play_note(Note.D6, tempo)
        time.sleep(0.1)
        zumi.play_note(Note.D6, tempo)
        time.sleep(1.5)


def _celebrate_sound(zumi):
    time.sleep(.25)
    zumi.play_note(48, 100)
    time.sleep(.005)
    zumi.play_note(52, 100)
    time.sleep(.005)
    zumi.play_note(55, 100)
    time.sleep(.005)
    zumi.play_note(55, 100)
    time.sleep(.20)
    zumi.play_note(52, 125)
    time.sleep(.005)
    zumi.play_note(55, 125)


def run():
    zumi = Zumi()
    screen = Screen()

    if os.path.isfile('/home/pi/recalibrate'):
        screen.draw_text_center("Place me on a flat surface.")
        sound.happy_sound(zumi)
        time.sleep(5)

        screen.calibrating()
        sound.try_calibrate_sound(zumi)
        subprocess.Popen(['sudo', 'rm', '-rf', '/home/pi/recalibrate'])
        zumi.mpu.calibrate_MPU()

        screen.draw_image_by_name("calibrated")
        sound.calibrated_sound(zumi)

    time.sleep(1)
    screen.draw_text_center("Find \"" + gethostname() + "\" in your WiFi list")

    while not scripts.is_device_connected():
        time.sleep(.2)
    screen.draw_image_by_name("foundme")
    sound.celebrate_sound(zumi)
    time.sleep(2)
    screen.draw_text_center("Go to \"zumidashboard.ai\" in your browser")
    time.sleep(1)


if __name__ == '__main__':
    run()
