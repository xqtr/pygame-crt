#!/usr/bin/env python3

import numpy as np

class framebuffer():
  
  def __init__(self, device_no: int):
    self.path = "/dev/fb%d" % device_no
    config_dir = "/sys/class/graphics/fb%d/" % device_no
    self.size = tuple(self._read_and_convert_to_ints(
      config_dir + "/virtual_size"))
    self.stride = self._read_and_convert_to_ints(config_dir + "/stride")[0]
    self.bits_per_pixel = self._read_and_convert_to_ints(
      config_dir + "/bits_per_pixel")[0]
    self.width = self.size[0]
    self.height = self.size[1]
    self.channels = 4
    self.screen = np.memmap(self.path, dtype='uint8',mode='w+', shape=(self.height,self.width)) 
    #self.screen = np.memmap(self.path, dtype='uint8',mode='w+', shape=(self.height,self.width,self.channels)) 
  
  def _read_and_convert_to_ints(self,filename):
    with open(filename, "r") as fp:
      content = fp.read()
      tokens = content.strip().split(",")
      return [int(t) for t in tokens if t]
      
  def showPILImage(self,image):
    self.screen[:] = np.array(image)
      
  def plot(self,x,y,color): # blue = [255,0,0,255]
    self.screen[y,x]=color
    #self.screen[y:x]=color

# Map the screen as Numpy array
# N.B. Numpy stores in format HEIGHT then WIDTH, not WIDTH then HEIGHT!
# c is the number of channels, 4 because BGRA

fb = framebuffer(0)
# Fill entire screen with blue - takes 29 ms on Raspi 4
#fb.screen[:] = [255,0,0,255]

# Fill top half with red - takes 15 ms on Raspi 4
#fb.screen[:fb.height//2] = [155,0,255,255]

# Fill bottom right quarter with green - takes 7 ms on Raspi 4
#fb[h//2:, w//2:] = [0,255,0,255] 
fb.plot(100,100,[255,255,255,255])
fb.plot(200,200,[255,255,255,255])


# from PIL import Image

# # Load Lena image
# im = Image.open('/home/pi/lena1280.png') 

# # Convert from PIL Image to Numpy array
# n = np.array(im)

# # Blit to screen - takes 30ms
# fp[:] = n

from PIL import ImageDraw
from PIL import Image
import time

image = Image.new("RGBA", (fb.width,fb.height))
draw = ImageDraw.Draw(image)
draw.rectangle(((0, 0), fb.size), fill="green")
draw.ellipse(((0, 0), fb.size), fill="blue", outline="red")
draw.line(((0, 0), fb.size), fill="green", width=2)
start = time.time()


fb.showPILImage(image)

stop = time.time()
print("fps: %.2f" % (10 / (stop - start)))
