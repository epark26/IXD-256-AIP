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
Car_img = p5.loadImage('car.gif')
Pool_img = p5.loadImage('pool.gif')
Noise_img = p5.loadImage('noise.gif')
Pool_sound = p5.loadSound('Pool.mp3') 
Retro_sound = p5.loadSound('Retro.mp3')
Glitch_sound = p5.loadSound('Glitch.mp3')

added_images = []

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

  if(button_val == 1):
    p5.image(NEWTV_img, 200, 200, 400, 400)
    if sensor_val > 120:
        added_images = [(Car_img, 179, 220, 176, 129)]
        Retro_sound.play()
        Pool_sound.stop()
        Glitch_sound.stop()
    elif sensor_val < 80:
        added_images = [(Pool_img, 179, 220, 176, 129)]
        Pool_sound.play()
        Glitch_sound.stop()
        Retro_sound.stop()
    else:
        added_images = [(Noise_img, 179, 220, 176, 129)]
        Glitch_sound.play()
        Retro_sound.stop()
        Pool_sound.stop()
  else:
    p5.image(TV_img, 200, 200, 400, 400)
    if sensor_val > 120:
        added_images = [(Car_img, 179, 220, 176, 129)]
        Retro_sound.play()
        Pool_sound.stop()
        Glitch_sound.stop()
    elif sensor_val < 80:
        added_images = [(Pool_img, 179, 220, 176, 129)]
        Pool_sound.play()
        Glitch_sound.stop()
        Retro_sound.stop()
    else:
        added_images = [(Noise_img, 179, 220, 176, 129)]
        Glitch_sound.play()
        Retro_sound.stop()
        Pool_sound.stop()

  p5.noStroke()  # disable stroke

  for img, x, y, w, h in added_images:
        # Create a rounded rectangle mask with a corner radius
      rounded_rect_mask = p5.createGraphics(w, h)
      rounded_rect_mask.noStroke()
      rounded_rect_mask.fill(255)
      rounded_rect_mask.rect(0, 0, 176, 129, 3)  # Adjust the corner radius as needed

        # Apply the rounded rectangle mask to the image
      img.mask(rounded_rect_mask)

      p5.image(img, x, y, w, h)




   
