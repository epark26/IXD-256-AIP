import os
import sys
import io
from M5 import *
from machine import Pin
from umqtt import *
from hardware import *
import time
from time import sleep_ms
from driver.neopixel import NeoPixel

mqtt_client = None
user_name = 'eunju_pp'
mqtt_timer = 0

np = None

OFF = [(0, 0, 0),(0, 0, 0),(0, 0, 0),
      (0, 0, 0),(0, 0, 0),(0, 0, 0),
       (0, 0, 0),(0, 0, 0),(0, 0, 0),
       (0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]

sleep = [
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (102, 0, 204),(102, 0, 204),(102, 0, 204),(102, 0, 204),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0)]

music = [
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (0 , 0, 255),(0 , 0, 255),(0 , 0, 255),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0)]

work = [
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (0 , 0, 0),(0 , 0, 0),(0 , 0, 0),
    (255, 255, 255),(255, 255, 255),(255, 255, 255)]

btn_sleep = Pin(41, Pin.IN, Pin.PULL_UP)
btn_music = Pin(7, Pin.IN, Pin.PULL_UP)
btn_work= Pin(8, Pin.IN, Pin.PULL_UP)

mqtt_timer = 0
program_state = 'OFF'
states = ['sleep', 'music', 'cheerup']

def setup():
    M5.begin()
    global np
    global mqtt_client
    np = NeoPixel(pin=Pin(2), n=13)
    mqtt_client = MQTTClient(
        'testclient',
        'io.adafruit.com',
        port=1883, 
        user=user_name,
        password='aio_ycCx41X0NQ6t5ytBmV98xDr0Mn7p',
    )
    mqtt_client.connect(clean_session=True)
    

def set_colors(color):
    global np
    if np is not None and isinstance(np, NeoPixel):
        for i in range(min(len(np), len(color))):
            np[i] = color[i]
        np.write()
    else:
        print("Error: NeoPixel object not properly initialized.")
        
def button_pressed(button):
    sleep_ms(50)  # Debounce time
    return not button.value()

def publish_mqtt(topic, message):
    global mqtt_client
    if mqtt_client is not None:
        mqtt_client.connect(clean_session=True)
        mqtt_client.publish(topic, message, qos=0)

def loop():
    global np, mqtt_client, mqtt_timer
    global np, sleep, music, work
    global mqtt_timer, program_state
    M5.update()
    
    if program_state == 'OFF':
        #print('OFF')
        set_colors(OFF)
        #sleep_ms(2000)
        if not btn_music.value():
            program_state = 'music'
        elif not btn_work.value():
            program_state = 'work'
        elif not btn_sleep.value():
            program_state = 'sleep'
            
    # condition for every 2.5 seconds
                
    if time.ticks_ms() > mqtt_timer + 1000:
        if program_state == 'music':
            print('music')
            mqtt_client.publish(user_name+'/feeds/Music', 'ON', qos=0)
            set_colors(music)

        elif program_state == 'work':
            print('work')
            mqtt_client.publish(user_name+'/feeds/study', 'ON', qos=0)
            set_colors(work)

        elif program_state == 'sleep':
            print('sleep')
            mqtt_client.publish(user_name+'/feeds/sleep', 'ON', qos=0)
            set_colors(sleep)
            
        mqtt_timer = time.ticks_ms()


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
            pass
