#sorry this code is not working. Because I write down in class activity in same file :(
import os, sys, io
import M5
from M5 import *
import time
from unit import *


angle_0 = None


angle_value = None


def setup():
  global angle_0, angle_value

  angle_0 = Angle((1,2))
  M5.begin()


def loop():
  global angle_0, angle_value
  print(angle_value)
  M5.update()
  angle_value = angle_0.get_value()
  time.sleep_ms(500)


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
      print("please update to latest firmware")
