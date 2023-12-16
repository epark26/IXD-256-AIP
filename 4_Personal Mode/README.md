## Introduction   

https://epark26.github.io/IXD-256-AIP/4_Personal_Mode/

#### My Personal Mode

The concept revolves around a personalized interactive system. The system is designed to enhance different aspects of daily life, such as exercise, sleep, and work, by integrating technology and automation. Each acrylic board corresponds to a particular activity or mode, and when inserted into the wood box, it initiates a set of actions, including music playback, messaging, and notifications. 

When I insert the acrylic board into the wood box, it triggers predefined actions based on the set colors. First, when I want to exercise, inserting the workout acrylic board plays music on Spotify, and the color changes to a rainbow. Second, when I want to sleep, inserting the sleep acrylic board sends a message to my friends through Telegram, stating that I'll reply the next day, and the color changes to a yellowish hue. Third, when I want to focus on work, inserting the work acrylic board sends a notification to my phone saying 'Do not use your phone,' and the colors shift to green and blue.

### Formatting Tips  
   
![Formatting 1](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Formatting.jpg) 
![Formatting gif](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Formatting.gif) 
![Formatting gif](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Inside.JPG) 

## Implementation   

### Hardware
 
* AtomS3 Lite ESP32S3 Dev Kit 
* ATOMIC PortABC Extension Base 
* Tactile Button switch (6mm) x 20 pack
* Mini Angle Unit Rotary Switch with Potentiometer
* Half-Size Breadboard with Mounting Holes
* Jumper Wire
* USB C

### Firmware   

#### Full Code

``` import os
import sys
import io
from M5 import *
from machine import Pin, ADC
from umqtt import MQTTClient
from hardware import *
import time
from time import sleep_ms
from driver.neopixel import NeoPixel

mqtt_client = None
user_name = 'eunju_pp'
mqtt_timer = 0
adc = None
adc_val = None
rgb = None

np = None


OFF = [(0, 0, 0),(0, 0, 0),(0, 0, 0),
      (0, 0, 0),(0, 0, 0),(0, 0, 0),
       (0, 0, 0),(0, 0, 0),(0, 0, 0),
       (0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]

sleep = [
    (255,140,0),(255,140,0),(255,140,00),
    (255,140,0),(255,140,0),(255,140,0),(255,140,0)]

music = [
    (255, 0, 0),(255, 165, 0),(255, 255, 0),
    (0, 128, 0),(0, 0, 255),(75, 0, 130),(48, 0, 211)]

work = [
    (30,144,25),(95,158,160),(30,144,25),
    (95,158,160),(30,144,25),(95,158,160),(30,144,25)]

btn_sleep = Pin(38, Pin.IN, Pin.PULL_UP)
btn_music = Pin(8, Pin.IN, Pin.PULL_UP)
btn_work = Pin(7, Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(6), atten=ADC.ATTN_11DB)  

mqtt_timer = 0
program_state = 'OFF'
states = ['sleep', 'music', 'work']

def setup():
    M5.begin()
    global np
    global mqtt_client
    global adc, adc_val
    np = NeoPixel(pin=Pin(2), n=7)
    mqtt_client = MQTTClient(
        'testclient',
        'io.adafruit.com',
        port=1883, 
        user=user_name,
        password='aio_twuw742hgZ7d5KflVmgzvlesdhgv',
    )
    mqtt_client.connect(clean_session=True)

def set_colors(color, adc_val):
    global np
    if np is not None and isinstance(np, NeoPixel):
        for i in range(min(len(np), len(color))):
            r, g, b = color[i]
            brightness = map_value(adc_val, 0, 4025, 0, 255)
            r = int(r * brightness / 255)
            g = int(g * brightness / 255)
            b = int(b * brightness / 255)
            np[i] = (r, g, b)
        np.write()
    else:
        print("Error: NeoPixel object not properly initialized.")


def publish_mqtt(topic, message):
    global mqtt_client
    if mqtt_client is not None:
        print("Publishing MQTT:", topic, "Message:", message)
        mqtt_client.connect(clean_session=True)
        mqtt_client.publish(topic, message, qos=0)

music_published = False
work_published = False
sleep_published = False


def loop():
    global np, mqtt_client, mqtt_timer
    global sleep, music, work
    global adc_val, program_state, music_published, work_published, sleep_published
    M5.update()

    # Read ADC value
    adc_val = adc.read()  

    if program_state == 'OFF':

        if not btn_music.value() and not music_published:
            print('music_trigger')
            mqtt_client.publish(user_name+'/feeds/Music', 'ON', qos=0)
            program_state = 'music'
            music_published = True
            work_published = False
            sleep_published = False

        elif not btn_work.value() and not work_published:
            print('work_trigger')
            mqtt_client.publish(user_name+'/feeds/study', 'ON', qos=0)
            program_state = 'work'
            music_published = False
            work_published = True
            sleep_published = False

        elif not btn_sleep.value() and not sleep_published:
            print('sleep_trigger')
            mqtt_client.publish(user_name+'/feeds/sleep', 'ON', qos=0)
            program_state = 'sleep'
            music_published = False
            work_published = False
            sleep_published = True


    else:
        music_published = False
        work_published = False
        sleep_published = False

        # Check for button release to transition back to 'OFF' state
        if btn_music.value() and btn_work.value() and btn_sleep.value():
            program_state = 'OFF'

    # condition for changing the LED color every 2.5 seconds
    if time.ticks_ms() > mqtt_timer + 1000: 
        if program_state == 'music':
            print('music')
            set_colors(music, adc_val)

        elif program_state == 'work':
            print('work')
            set_colors(work, adc_val)

        elif program_state == 'sleep':
            print('sleep')
            set_colors(sleep, adc_val)

        # reset the timer
        mqtt_timer = time.ticks_ms()


# map an input value (v_in) between min/max ranges:
def map_value(in_val, in_min, in_max, out_min, out_max):
  v = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if (v < out_min): 
    v = out_min 
  elif (v > out_max): 
    v = out_max
  return int(v)

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
```


### Software   

#### IFTTT mqtt
```     
      if program_state == 'OFF':

        if not btn_music.value() and not music_published:
            print('music_trigger')
            mqtt_client.publish(user_name+'/feeds/Music', 'ON', qos=0)
            program_state = 'music'
            music_published = True
            work_published = False
            sleep_published = False

        elif not btn_work.value() and not work_published:
            print('work_trigger')
            mqtt_client.publish(user_name+'/feeds/study', 'ON', qos=0)
            program_state = 'work'
            music_published = False
            work_published = True
            sleep_published = False

        elif not btn_sleep.value() and not sleep_published:
            print('sleep_trigger')
            mqtt_client.publish(user_name+'/feeds/sleep', 'ON', qos=0)
            program_state = 'sleep'
            music_published = False
            work_published = False
            sleep_published = True


    else:
        music_published = False
        work_published = False
        sleep_published = False

        # Check for button release to transition back to 'OFF' state
        if btn_music.value() and btn_work.value() and btn_sleep.value():
            program_state = 'OFF'
``` 

#### Led Color
```     
        if time.ticks_ms() > mqtt_timer + 1000: 
        if program_state == 'music':
            print('music')
            set_colors(music, adc_val)

        elif program_state == 'work':
            print('work')
            set_colors(work, adc_val)

        elif program_state == 'sleep':
            print('sleep')
            set_colors(sleep, adc_val)

        # reset the timer
        mqtt_timer = time.ticks_ms()
```  
### Integrations   

#### Adafruit feed
![Adafruit data](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Adafruit_Data.png) 

#### IFTTT Trigger
![IFTTT](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/IFTTT.png) 


### Enclosure / Mechanical Design   

#### woodboard
![laser cut1](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Raser-cut-1.jpg) 
![laser cut1](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/wood%2BLight.JPG) 

#### Mode
![laser cut2](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Raser-cut-2.jpg) 
![laser cut2](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/3%20DifferentMode.JPG) 

## Project outcome  

#### Sleep Mode
![Sleep](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/sleepmode_final.jpg) 

#### Exercise Mode
![exercise](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/exercise_final.jpg) 

#### Work Mode
![work](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/workmode_final.jpg) 

#### Prototyping Video
![Final](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Full%20Prototyping.gif) 
![Final](https://github.com/epark26/IXD-256-AIP/blob/main/4_Personal%20Mode/Photo/Level%20of%20Brightness.gif) 

## Conclusion  

#### First Challenge: Continuous Notification During LED Activation

The first challenge involved dealing with continuous notifications while the LED remained on. I wanted the LED to stay on continuously, but the notifications to come only once. As a solution, I separated the code into sections for the LED and the IFTTT (If This Then That) part. This process took quite some time.

#### Second Challenge: Potentiometer for LED Brightness Control

The second challenge was to use a potentiometer to adjust the brightness of the LED. There were issues with the pin configuration, and despite multiple attempts, the problem could not be resolved. Fortunately, during the presentation, it started working smoothly.

#### Take away
If I have more time, I'd like to add various modes instead of making it smaller. Additionally, I want to place an acrylic board just above the LED to enhance the display of colors more effectively.


## Project references  

I only use nikita's github code and make design myself
