#!/usr/bin/python

import os
import pygame
from pygame.locals import *
import time
import random

SCREEN = None
FONTNAME = '80x25.bmp'
#FONTNAME = "courier new"
FONTSIZE = 50
HEIGHT = 0
WIDTH = 0
SCR_OFFSET_X = 0
SCR_OFFSET_Y = 0
WHEREX = 1
WHEREY = 1
BUFFER = []
SAVEX = None
SAVEY = None
MODE = {'x':80,'y':25}
SCREENHEIGHT = MODE['y']
SCREENWIDTH = MODE['x']
CHARWIDTH = 0
CHARHEIGHT = 0

#colors     R    G    B
black   = (  0,   0,   0)
blue    = (  0,   0, 128)
green   = (  0, 128,   0)
cyan    = (  0, 128, 128)
red     = (170,   0,   0)
magenta = (128,   0, 128)
brown   = (128, 128,   0)
gray    = (192, 192, 192)
darkgray= (128,128,128)
lblue   = (0,0,255)
lgreen  = (0,255,0)
lcyan   = (0,255,255)
lred    = (255,0,0)
lmagenta= (255,0,255)
yellow  = (255,255,0)
white   = (255, 255, 255)

ATTR = 7
COLOR = {
0:black,
1:blue,
2:green,
3:cyan,
4:red,
5:magenta,
6:brown,
7:gray,
8:darkgray,
9:lblue,
10:lgreen,
11:lcyan,
12:lred,
13:lmagenta,
14:yellow,
15:white
}

cfg_pausestr = '|08[|15Pause|08]'
cfg_popup_box_at = 8
cfg_popup_title_at = 15
cfg_popup_text_at = 7
cfg_popup_pause_at = 8
cfg_popup_pause_str = 'Press any key to continue...|PN'

pathchar = os.sep
pathsep  = os.sep

box_ascii=('.','-','.','|','|','`','-',"'",' ')
box1=(chr(218),chr(196),chr(191),chr(179),chr(179),chr(192),chr(196),chr(217),' ')

font = None
imgfont = None

class buttonclass():
  
  def __init__(self):
    self.items=list()
    self.total = 0
    
  def addbutton(self,x,y,width,height,func):
    item = {'x':x,'y':y,'w':width,'h':height,'func':func}
    self.items.append(item)
    self.total+=1
  
  def clear(self):
    self.items.clear()
    self.total = 0
    
  def check(self,x,y):
    global CHARWIDTH, CHARHEIGHT
    res = None
    for index,itm in enumerate(self.items):
      if (itm['x']-1)*CHARWIDTH<x and (itm['x']+itm['w'])*CHARWIDTH>x and \
        (itm['y']-1)*CHARHEIGHT<y and (itm['y']+itm['h'])*CHARHEIGHT>y:
        res = index
        break
    return res
    
def refresh(fb='/dev/fb0'):
  # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
  f = open(fb,"wb")
  # According to the TFT screen specs, it supports only 16bits pixels depth
  # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
  # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
  f.write(SCREEN.convert(16,0).get_buffer())
  # We can then close our access to the framebuffer
  f.close()
  time.sleep(0.1)
    
def printSDLVariables():
  print("Checking current env variables...")
  print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
  print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))
  print("DISPLAY = {0}".format(os.getenv("DISPLAY")))

def init():
  global SCREEN, HEIGHT, WIDTH, BUFFER, SCREENHEIGHT, SCREENWIDTH, FONTNAME
  global WHEREX, WHEREY, FONTSIZE, MODE, CHARWIDTH, CHARHEIGHT
  global imgfont
  "Ininitializes a new pygame screen using the framebuffer"
  # Based on "Python GUI in Linux frame buffer"
  # http://www.karoltomala.com/blog/?p=679
  
  printSDLVariables()
  os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide pygame prompt message
  disp_no = os.getenv("DISPLAY")
  if disp_no:
    print("I'm running under X display = {0}".format(disp_no))
  
  # Check which frame buffer drivers are available
  # Start with fbcon since directfb hangs with composite output
  drivers = ['fbcon','directfb', 'svgalib', 'fbdev']
  #drivers = ['directfb', 'fbcon', 'svgalib', 'x11']
  #drivers = ['directfb', 'fbcon', 'svgalib']
  found = False
  
    
  for driver in drivers:
    print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
    print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))
    # Make sure that SDL_VIDEODRIVER is set
    #if not os.getenv('SDL_VIDEODRIVER'):
      #os.putenv('SDL_VIDEODRIVER', driver)
    os.environ['SDL_VIDEODRIVER']=driver
    os.environ["SDL_FBDEV"] = "/dev/fb0"
    os.environ['FRAMEBUFFER']="/dev/fb0"
    try:
      pygame.display.init()
    except pygame.error:
      print('Driver: {0} failed.'.format(driver))
      continue
    found = True
    break
  
  if not found:
    raise Exception('No suitable video driver found!')

  pygame.init()
  
  size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
  WIDTH,HEIGHT = size
  print("Framebuffer size: %d x %d" % (size[0], size[1]))
  SCREEN = pygame.display.set_mode(size, pygame.FULLSCREEN)
  # Clear the screen to start
  SCREEN.fill((0, 0, 0))        
  
  BUFFER.clear()
  WHEREX = 1
  WHEREY = 1
  for y in range(SCREENHEIGHT):
    for x in range(SCREENWIDTH):
      BUFFER.append([' ',7])
  
  CHARWIDTH = WIDTH // MODE['x']
  
  if WIDTH>CHARWIDTH*MODE['x']:
    SCR_OFFSET_X = WIDTH-CHARWIDTH*MODE['x']
  
  imgfont = bmpfont(FONTNAME)
  CHARHEIGHT = CHARWIDTH * (imgfont.fontimg.get_height() // imgfont.fontimg.get_width())
  if HEIGHT>CHARHEIGHT*MODE['y']:
    SCR_OFFSET_Y = HEIGHT-CHARHEIGHT*MODE['y']
  print(f'Char. Width: {CHARWIDTH}, Height: {CHARHEIGHT}, Total: {80*CHARWIDTH}x{25*CHARHEIGHT}')
  pygame.display.update()
  

def checkxy():
  global WHEREX,WHEREY
  global SCREENWIDTH,SCREENHEIGHT
  if WHEREX > SCREENWIDTH:
    WHEREX = 1
    WHEREY += 1
  if WHEREY > SCREENHEIGHT:
    WHEREY = SCREENHEIGHT
    scrolldown()
    update()
    
def bufwritechar(c):
  global BUFFER,WHEREX,WHEREY,ATTR
  if c!='\r':
    if WHEREY>SCREENHEIGHT: WHEREY = SCREENHEIGHT
    BUFFER[(WHEREY-1)*SCREENWIDTH+(WHEREX-1)][0]=c
    BUFFER[(WHEREY-1)*SCREENWIDTH+(WHEREX-1)][1]=ATTR
    WHEREX += 1 
    
  checkxy()
  
def bufflush():
  global BUFFER,SCREENHEIGHT,SCREENWIDTH
  global WHEREX,WHEREY
  gotoxy(1,1)
  for yy in range(SCREENHEIGHT):
    for xx in range(SCREENWIDTH):
      c,a = BUFFER[xx+(yy*SCREENWIDTH)]
      if ord(c)!=0:
        textcolor(a)
        writechar(c)
  WHEREX = 1
  WHEREY = 1
  update()

def getcharat(x,y):
  global BUFFER,SCREENHEIGHT,SCREENWIDTH
  return BUFFER[(y-1)*SCREENWIDTH+(x-1)][0]
    
def getattrat(x,y):
  global BUFFER,SCREENHEIGHT,SCREENWIDTH
  return BUFFER[(y-1)*SCREENWIDTH+(x-1)][1]

def setattrat(x,y,a):
  global BUFFER,SCREENHEIGHT,SCREENWIDTH
  BUFFER[(y-1)*SCREENWIDTH+(x-1)][1] = a

def textcolor(c):
  global ATTR
  bg = ATTR // 16
  ATTR = c+(bg*16)

def textbackground(c):
  global ATTR
  fg = ATTR % 16
  ATTR = fg+(c*16)
  
def textattr(at):
  global ATTR
  ATTR=at
  
def gotoxy(x,y):
  global SCREENHEIGHT,SCREENWIDTH,WHEREX,WHEREY
  if x < 1:
    x = 1
  if x > SCREENWIDTH:
    x = SCREEWIDTH
  if y<1:
    y = 1
  if y>SCREENHEIGHT:
    y=SCREENHEIGHT
  WHEREX,WHEREY = x,y
  
def bufwritestr(s):
  for x in range(len(s)):
    bufwritechar(s[x:x+1])
    
def writechar(c):
  global SCREEN, imgfont, CHARWIDTH, CHARHEIGHT, WHEREX, WHEREY
  if c!='\n':
    pygame.draw.rect(SCREEN,bg2color(),(SCR_OFFSET_X+(CHARWIDTH*(WHEREX-1)),SCR_OFFSET_Y+(CHARHEIGHT*(WHEREY-1)),CHARWIDTH,CHARHEIGHT))
    imgfont.writexy(SCREEN,SCR_OFFSET_X+(CHARWIDTH*(WHEREX-1)),SCR_OFFSET_Y+(CHARHEIGHT*(WHEREY-1)),c)
  else:
    WHEREX = 1
    WHEREY+= 1
    if WHEREY>SCREENHEIGHT:
      WHEREY=SCREENHEIGHT
      scrolldown()
  bufwritechar(c)
  
def write(s):
  for c in s:
    writechar(c)
  
def writeln(st):
  write(st+'\n')
  
def writexy(x,y,a,s):
  textattr(a)
  gotoxy(x,y)
  writepipe(s)
  
def writexyw(x,y,a,w,s,char=' ',align='left'):
  gotoxy(x,y)
  textattr(a)
  if align.upper() == 'LEFT':
    write(s.ljust(char,w))
  elif align.upper() == 'RIGHT':
    write(s.rjust(char,w))
  else:
    write(s.center(char,w))
  
def writepipe(txt):
    OldAttr = ATTR
    
    width=len(txt)
    Count = 0

    while Count <= len(txt)-1:
        #swrite(str(Count)+' '+str(len(txt))+' '+str(width)
        if txt[Count] == '|':
            Code = txt[Count+1:Count+3]
            CodeNum = int(Code)

            if (Code == '00') or (CodeNum > 0):
                Count = Count +2
                if 0 <= int(CodeNum) < 16:
                    textattr(int(CodeNum) + ((ATTR // 16) * 16))
                else:
                    textattr((ATTR % 16) + (int(CodeNum) - 16) * 16)
            elif Code == 'PN': pause()
            else:
                write(txt[Count:Count+1])
                width = width - 1
      
        else:
            write(txt[Count:Count+1])
            width = width - 1
    

        if width == 0:
            break

        Count +=1
    
    if width > 1:
        write(' '*width)
    
def writexypipe(x,y,attr,width,txt):
    OldAttr = ATTR
    OldX    = WHEREX
    OldY    = WHEREY

    gotoxy(x,y)
    textattr(attr)

    Count = 0

    while Count <= len(txt)-1:
        #swrite(str(Count)+' '+str(len(txt))+' '+str(width)
        if txt[Count] == '|':
            Code = txt[Count+1:Count+3]
            CodeNum = int(Code)

            if (Code == '00') or (CodeNum > 0):
                Count = Count +2
                if 0 <= int(CodeNum) < 16:
                    textattr(int(CodeNum) + ((ATTR // 16) * 16))
                else:
                    textattr((ATTR % 16) + (int(CodeNum) - 16) * 16)
            else:
                write(txt[Count:Count+1])
                width = width - 1
      
        else:
            write(txt[Count:Count+1])
            width = width - 1
    

        if width == 0:
            break

        Count +=1
    
    if width > 1:
        write(' '*width)

    textattr(OldAttr)
    gotoxy(OldX, OldY)
    
def fg2color():
  global ATTR
  return COLOR[ATTR % 16]
  
def bg2color():
  global ATTR
  return COLOR[ATTR // 16]
  
def update():
  pygame.display.update()
  #refresh()

def clrscr():
  global SCREEN
  SCREEN.fill(bg2color())
  #update()
  
def scrolldown():
  SCREEN.scroll(dy=-CHARHEIGHT)
  
def delay(t):
  time.sleep(t/ 1000.0)
  
def savecursor():
  global SAVEX,SAVEY,WHEREX,WHEREY
  SAVEX = WHEREX
  SAVEY = WHEREY

def restorecursor():
  global SAVEX,SAVEY,WHEREX,WHEREY
  WHEREX = SAVEX
  WHEREY = SAVEY
  gotoxy(WHEREX,WHEREY)
  SAVEX,SAVEY = None,None
  
def cleararea(x1,y1,x2,y2,bg):
  for i in range(y2-y1):
    gotoxy(x1,y1+i)
    writechar(bg*(x2-x1))
  
def byte2str(v):
  s=''.join(str(v))
  return s[2:-1]

def ansibox(x1,y1,x2,y2,box=box_ascii):
  gotoxy(x1,y1)
  write(box[0]+box[1]*(x2-x1-1)+box[2])
  gotoxy(x1,y2)
  write(box[5]+box[6]*(x2-x1-1)+box[7])
  for i in range(y2-y1-1):
    gotoxy(x1,y1+1+i)
    write(box[3]+box[8]*(x2-x1-1)+box[4])
    
def popupbox(title,text,y):
  global cfg_popup_title_at, cfg_popup_text_at, cfg_popup_pause_at
  global cfg_popup_pause_str, cfg_popup_box_at
  d = len(text)
  d2 = d // 2
  textattr(cfg_popup_box_at)
  if d < 25:
    cleararea(26,y,54,y+3," ")
    ansibox(26,y,54,y+3)
  else:
    cleararea(38-d2,y,42+d2,y+3," ")
    ansibox(38-d2,y,42+d2,y+3)
  writexy(38-d2,y,cfg_popup_title_at,title)  
  writexy(40-d2,y+1,cfg_popup_text_at,text)
  writexy(28,y+2,cfg_popup_pause_at,cfg_popup_pause_str)

def charxy(x,y):
  return (getcharat(x,y),getattrat(x,y))

def shadow(x1,y1,x2,y2,attr):
  for i in range(y2-y1):
    writexy(x2+1,y1+1+i,attr,charxy(x2+1,y1+1+i)[0])
  for i in range(x2-x1):
    writexy(x1+2+i,y2+1,attr,charxy(x1+2+i,y2+1)[0])
    
def readkey():
  global buttons
  ext = None
  key = ''
  Done = False
  while not Done:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONUP:
        if buttons.total!=0:
          mpos = pygame.mouse.get_pos()
          a = buttons.check(mpos[0],mpos[1])
          print(f'asdadada: {a}')  
          if a!=None: 
            Done = True
      if event.type == pygame.KEYUP:
        key = event.key
        if event.mod == pygame.KMOD_NONE:
          ext = None
          Done = True
        elif event.mod & pygame.KMOD_CTRL:
          ext = 'ctrl'
        elif event.mod & pygame.KMOD_ALT:
          ext = 'alt'
        elif event.mod & pygame.KMOD_SHIFT:
          ext = 'shift'
        Done = True
  return (key,ext)

class bmpfont():
  
  def __init__(self,imagefile,transrgb = (0, 0, 0)):
    #self.fontimg = pygame.image.load(imagefile).convert()
    self.fontimg = pygame.image.load(imagefile)
    self.fontimg.set_colorkey(transrgb, RLEACCEL)
    self.charwidth = self.fontimg.get_width() // 16
    self.charheight = self.fontimg.get_height() // 16
    self.chartable = list()
    for y in range(16):
      for x in range(16):
        tmp = self.clip(self.fontimg,x*self.charwidth,y*self.charheight,self.charwidth,self.charheight)
        self.chartable.append(pygame.transform.scale(tmp,(CHARWIDTH,CHARHEIGHT)))
  
  def clip(self,surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()
    
  def changeColor(self,image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage
    
  def writexy(self,surf,x,y,s):
    xpos,ypos = 0,0
    for c in s:
      surf.blit(self.changeColor(self.chartable[ord(c)],COLOR[ATTR % 16]), (x+xpos,y+ypos))
      xpos += CHARWIDTH

#init program
buttons = buttonclass()    
init()
key = None
clrscr()
imgfont = bmpfont(FONTNAME)

#main code
buttons.addbutton(8,8,22,6,None)
textattr(14+32)
ansibox(8,8,30,14,box1)
writexy(10,10,3,'hello')
update()
key,ext = readkey()
buttons.clear()
while key!=pygame.K_ESCAPE:
  clrscr()
  for y in range(1,SCREENHEIGHT+1):
    for x in range(1,SCREENWIDTH+1):
      writexy(x,y,7,chr(177))
  writexy(1,1,14,f'width: {imgfont.charwidth} height: {imgfont.charheight}')
  update()
  key,ext = readkey()
  
  writexy(5,5,11+32,'You pressed: '+str(key)+' '+str(ext))
  
  update()
  key,ext = readkey()
  for i in range(30):
    writeln('hello')
    update()
  key,ext = readkey()

