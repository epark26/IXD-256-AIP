from machine import Pin, PWM
import time
import os, sys, io
import M5
from M5 import *
from hardware import *
import time

# configure servo on pin G7 using PWM:
servo = PWM(Pin(7))
# configure PWM frequency:
servo.freq(100)

# Set initial position to 50 degrees
initial_position = 70
servo.duty(initial_position)

def setup():
    global pin1
    # initialize M5 board:
    M5.begin()
    # initialize pin1 as an output pin:

def loop():
    global pin1
    # update M5 board:
    M5.update()
    if BtnA.isPressed():
        # move servo counterclockwise by changing PWM duty:
        servo.duty(160)
        time.sleep(0.3)
    else:
        # return servo to the initial position (50 degrees)
        servo.duty(initial_position)
        time.sleep_ms(100)

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to the latest firmware")
