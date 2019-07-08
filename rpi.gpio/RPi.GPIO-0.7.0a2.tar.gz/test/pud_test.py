#!/usr/bin/env python3.8
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    for i in range(1000):
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        time.sleep(0.001)
        if GPIO.input(23) != GPIO.LOW:
            print('Error')
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        time.sleep(0.001)
        if GPIO.input(23) != GPIO.HIGH:
            print('Error')
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
