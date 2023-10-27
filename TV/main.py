import js as p5
from js import document

data_string = None
data_list = None
sensor_val = None
button_val = None
button_state = 0

# load image data and assign it to variable:
TV_img = p5.loadImage('tv.jpg')
NEWTV_img = p5.loadImage('new_tv.jpg')

def setup():
  p5.createCanvas(400, 400)
  # change mode to draw rectangles from center:
  p5.rectMode(p5.CENTER)
  # change mode to draw images from center:
  p5.imageMode(p5.CENTER)
  # change stroke cap to square:
  p5.strokeCap(p5.SQUARE)

def draw():

  global data_string, data_list
  global sensor_val, button_val
  global button_state

  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  # assign 1st item of data_list to sensor_val:
  sensor_val = int(data_list[0])
  # assign 2nd item of data_list to sensor_val:
  button_val = int(data_list[1])

  p5.noStroke()  # disable stroke
  p5.image(TV_img, 200, 200, 400, 400)

  if button_val == 1:
    # Display the new image when the button is pressed (assuming button_val indicates the button is pressed)
    p5.image(NEWTV_img, 200, 200, 400, 400)
  elif(button_val == 0):
    p5.image(TV_img, 200, 200, 400, 400)
