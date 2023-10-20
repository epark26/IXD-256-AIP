import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
state = 'START'
state_timer = 0

def setup():
  global rgb, input_pin
  M5.begin()
  
  rgb = RGB(io=35, n=1, type="SK6812")
  
  input_pin = Pin(41)
  
  
  # turn on RGB green and wait 2 seconds:
  if state == 'START':
    print('Start with RGB blue..')
    rgb.fill_color(get_color(0, 0, i)) 

    while input_pin.value() == 1:
        pass  # Wait until the input condition is met

    check_input()  # Call the check_input() function after the condition is met


def loop():
  global state, state_timer
  M5.update()
      
  if (state == 'OPEN'):
    print('pulsate blue..')
    # fade in RGB blue:
    for i in range(100):
      rgb.fill_color(get_color(0, 0, i))
      time.sleep_ms(20)
    # fade out RGB blue:
    for i in range(100):
      rgb.fill_color(get_color(0, 0, 100-i))
      time.sleep_ms(20)
    check_input()
    
  elif state == 'CLOSED':
    fade_duration = 10  # seconds
    steps = 100  # Total steps from 0 to 100
    step_duration = fade_duration / steps

    if time.ticks_ms() < state_timer + 10000:  # 10 seconds
        print('Fade in white..')
        for i in range(steps + 1):  # Include 100 (steps go up to 100)
            rgb.fill_color(get_color(i, i, i))
            time.sleep(step_duration)
    elif time.ticks_ms() > state_timer + 5000:
        state = 'FINISH'
        print('Change to', state)
        state_timer = time.ticks_ms()
        
  elif (state == 'FINISH'):
    print('fade from white to red..')
    for i in range(100):
      rgb.fill_color(get_color(100, 100-i, 0))
      time.sleep_ms(50)
      


def check_input():
  global state, state_timer
  if (input_pin.value() == 0):
    if(state != 'CLOSED'):
      print('change to CLOSED')
    state = 'CLOSED'
    # save current time in milliseconds:
    state_timer = time.ticks_ms()
  else:
    if(state != 'OPEN'):
      print('change to OPEN')
    state = 'OPEN'
    

def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

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