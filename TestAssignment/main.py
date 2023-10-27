import js as p5
from js import document

data_string = None
data_list = None
sensor_val = None
button_val = None

# load font data and assign it to variable:
NeueHaasUnica_font = p5.loadFont('NeueHaasUnica-ExtraBold.ttf')

def setup():
  p5.createCanvas(400, 400)
  p5.background(167, 167, 211)
  p5.rectMode(p5.CENTER)
  p5.noStroke()
  p5.fill(234, 234,234)
  p5.rect(200, 200, 250, 150, 10)
  p5.fill(167, 167, 211)

    # Draw a grid of rectangles
  for x in range(4):
      for y in range(2):
          p5.fill(167, 167, 211)
          p5.rect(125 + x * 50, 200 + y * 45, 40, 40, 10)

def draw():
  global data_string, data_list
  global sensor_val, button_val, num_circles

  colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        
  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  # assign 1st item of data_list to sensor_val:
  sensor_val = int(data_list[0])
  # assign 2nd item of data_list to sensor_val:
  button_val = int(data_list[1])

  p5.fill(240, 78, 35)  # Set the text fill color to orange
  p5.textFont(NeueHaasUnica_font)  # Use the "Neue Haas Unica" font
  p5.textSize(24)
  p5.textStyle(p5.BOLD)
  p5.text("happy card", 135, 160)

  p5.noStroke()  # disable stroke

  p5.fill(233, 230, 31)
  p5.ellipse(125, 200, 40, 40)
  if button_val == 1:
      # Cycle through colors when the button is pressed
      current_color_index = frameCount % len(colors)
      p5.fill(*colors[current_color_index])
  else:
      # Use the default color when the button is not pressed
      p5.fill(233, 230, 31)

  
  color_index = p5.floor(p5.map(sensor_val, 0, 255, 0, len(colors)))
  triangle_color = colors[color_index]
  # draw square changing color with sensor data:
  # fill function can take (red, green, blue)
  p5.fill(240, 78, 35) 
  # rectangle function takes (x, y, width, height)
  x1 = 160
  y1 = 215
  x2 = x1 + 34
  y2 = y1
  x3 = x1 + 17
  y3 = y1 - 34

  p5.fill(*triangle_color)
  p5.triangle(x1, y1, x2, y2, x3, y3)

