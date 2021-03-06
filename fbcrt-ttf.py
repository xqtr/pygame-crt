#!/usr/bin/python

import os
import sys
import tty,termios
import time
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

'''
im = Image.open('tweeter.png')
layer = Image.new('RGB', im.size, 'red') # "hue" selection is done by choosing a color...
output = Image.blend(im, layer, 0.5)
output.save('output.png', 'PNG')


img = Image.open(r"C:\Users\System-Pc\Desktop\pinktree.jpg").convert("L")
# image colorize function
img1 = ImageOps.colorize(img, black ="blue", white ="white")
'''

fb = None

SCREEN = None
FONTNAME = 'dos.ttf'
FONTSIZE = 5
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
SCRDRAW = None

# common
LF = '\x0d'
CR = '\x0a'
ENTER = '\x0d'
BACKSPACE = '\x7f'
SUPR = ''
SPACE = '\x20'
ESC = '\x1b'

# CTRL
CTRL_A = '\x01'
CTRL_B = '\x02'
CTRL_C = '\x03'
CTRL_D = '\x04'
CTRL_E = '\x05'
CTRL_F = '\x06'
CTRL_G = '\x07'
CTRL_H = '\x08'
CTRL_I = '\x09'
CTRL_J = '\x0a'
CTRL_K = '\x0b'
CTRL_L = '\x0c'

CTRL_N = '\x0e'
CTRL_O = '\x0f'
CTRL_P = '\x10'
"""
q
r
s
t
u
v
w
x
y
"""
CTRL_Y = '\x19'
CTRL_Z = '\x1a'
CTRL_W = ''

# ALT
ALT_A = '\x1b\x61'

# CTRL + ALT
CTRL_ALT_A = '\x1b\x01'

# cursors
UP = '\x1b\x5b\x41'
DOWN = '\x1b\x5b\x42'
LEFT = '\x1b\x5b\x44'
RIGHT = '\x1b\x5b\x43'

CTRL_ALT_SUPR = '\x1b\x5b\x33\x5e'

# other
F1 = '\x1b\x4f\x50'
F2 = '\x1b\x4f\x51'
F3 = '\x1b\x4f\x52'
F4 = '\x1b\x4f\x53'
F5 = '\x1b\x4f\x31\x35\x7e'
F6 = '\x1b\x4f\x31\x37\x7e'
F7 = '\x1b\x4f\x31\x38\x7e'
F8 = '\x1b\x4f\x31\x39\x7e'
F9 = '\x1b\x4f\x32\x30\x7e'
F10 = '\x1b\x4f\x32\x31\x7e'
F11 = '\x1b\x4f\x32\x33\x7e'
F12 = '\x1b\x4f\x32\x34\x7e'

PAGE_UP = '\x1b\x5b\x35\x7e'
PAGE_DOWN = '\x1b\x5b\x36\x7e'
HOME = '\x1b\x5b\x48'
END = '\x1b\x5b\x46'

INSERT = '\x1b\x5b\x32\x7e'
SUPR = '\x1b\x5b\x33\x7e'


KEY_HOME = chr(71)
KEY_UP   = chr(72)
KEY_PGUP = chr(73)
KEY_LEFT = chr(75)
KEY_RIGHT= chr(77)
KEY_END  = chr(79)
KEY_DOWN = chr(80)
KEY_PGDN = chr(81)
KEY_INS  = chr(82)
KEY_DEL  = chr(83)
KEY_BACK = chr(8)
KEY_TAB  = chr(9)
KEY_ENTER= chr(13)
KEY_ESCAPE = chr(27)
KEY_SPACE = chr(32)

KEY_F1 = chr(59)
KEY_F2 = chr(60)
KEY_F3 = chr(61)
KEY_F4 = chr(62)
KEY_F5 = chr(63)
KEY_F6 = chr(64)
KEY_F7 = chr(65)
KEY_F8 = chr(66)
KEY_F9 = chr(67)
KEY_F10 = chr(68)
KEY_F11 = chr(69)
KEY_F12 = chr(70)

KEY_CTRLA  = chr(1) 
KEY_CTRLB  = chr(2) 
KEY_CTRLC  = chr(3) 
KEY_CTRLD  = chr(4) 
KEY_CTRLE  = chr(5) 
KEY_CTRLF  = chr(6) 
KEY_CTRLG  = chr(7) 
KEY_CTRLH  = chr(8) 
KEY_CTRLI  = chr(9) 
KEY_CTRLJ  = chr(10)
KEY_CTRLK  = chr(11)
KEY_CTRLL  = chr(12)
KEY_CTRLM  = chr(13)
KEY_CTRLN  = chr(14)
KEY_CTRLO  = chr(15)
KEY_CTRLP  = chr(16)
KEY_CTRLQ  = chr(17)
KEY_CTRLR  = chr(18)
KEY_CTRLS  = chr(19)
KEY_CTRLT  = chr(20)
KEY_CTRLU  = chr(21)
KEY_CTRLV  = chr(22)
KEY_CTRLW  = chr(23)
KEY_CTRLX  = chr(24)
KEY_CTRLY  = chr(25)
KEY_CTRLZ  = chr(26)

KEY_ALTA  = chr(158)
KEY_ALTB  = chr(176)
KEY_ALTC  = chr(174)
KEY_ALTD  = chr(160)
KEY_ALTE  = chr(146)
KEY_ALTF  = chr(161)
KEY_ALTG  = chr(162)
KEY_ALTH  = chr(163)
KEY_ALTI  = chr(151)
KEY_ALTJ  = chr(164)
KEY_ALTK  = chr(165)
KEY_ALTL  = chr(166)
KEY_ALTM  = chr(178)
KEY_ALTN  = chr(177)
KEY_ALTO  = chr(152)
KEY_ALTP  = chr(153)
KEY_ALTQ  = chr(144)
KEY_ALTR  = chr(147)
KEY_ALTS  = chr(159)
KEY_ALTT  = chr(148)
KEY_ALTU  = chr(150)
KEY_ALTV  = chr(175)
KEY_ALTW  = chr(145)
KEY_ALTX  = chr(173)
KEY_ALTY  = chr(149)
KEY_ALTZ  = chr(172)

def rgb2bgr(cl):
  return (cl[2],cl[1],cl[0],cl[3])

#colors     R    G    B
black   = (  0,   0,   0,255)
blue    = (  0,   0, 128,255)
green   = (  0, 128,   0,255)
cyan    = (  0, 128, 128,255)
red     = (170,   0,   0,255)
magenta = (128,   0, 128,255)
brown   = (128, 128,   0,255)
gray    = (192, 192, 192,255)
darkgray= (128,128,128,255)
lblue   = (0,0,255,255)
lgreen  = (0,255,0,255)
lcyan   = (0,255,255,255)
lred    = (255,0,0,255)
lmagenta= (255,0,255,255)
yellow  = (255,255,0,255)
white   = (255, 255, 255,255)

ATTR = 7
COLOR = {
0:rgb2bgr(black),
1:rgb2bgr(blue),
2:rgb2bgr(green),
3:rgb2bgr(cyan),
4:rgb2bgr(red),
5:rgb2bgr(magenta),
6:rgb2bgr(brown),
7:rgb2bgr(gray),
8:rgb2bgr(darkgray),
9:rgb2bgr(lblue),
10:rgb2bgr(lgreen),
11:rgb2bgr(lcyan),
12:rgb2bgr(lred),
13:rgb2bgr(lmagenta),
14:rgb2bgr(yellow),
15:rgb2bgr(white)
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

fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)    

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
    self.screen = np.memmap(self.path, dtype='uint8',mode='w+', shape=(self.height,self.width,self.channels)) 
  
  def _read_and_convert_to_ints(self,filename):
    with open(filename, "r") as fp:
      content = fp.read()
      tokens = content.strip().split(",")
      return [int(t) for t in tokens if t]
      
  def savetofile(filename):
    '''save the frame buffer screen to a file'''
    SCREEN.save(filename)
      
  def showPILImage(self,image):
    self.screen[:] = np.array(image)
      
  def plot(self,x,y,color): # blue = [255,0,0,255]
    self.screen[y,x]=color
    #self.screen[y:x]=color

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
    
def refresh():
  global SCREEN,fb
  #fb.screen[:]=pygame.surfarray.array2d(SCREEN)
  fb.showPILImage(SCREEN)
    
def printSDLVariables():
  print("Checking current env variables...")
  print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
  print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))
  print("DISPLAY = {0}".format(os.getenv("DISPLAY")))

def init(size):
  global SCREEN, HEIGHT, WIDTH, BUFFER, SCREENHEIGHT, SCREENWIDTH, FONTNAME
  global WHEREX, WHEREY, FONTSIZE, MODE, CHARWIDTH, CHARHEIGHT
  global imgfont, SCRDRAW, SCR_OFFSET_X, SCR_OFFSET_Y
  
  WIDTH,HEIGHT = size
  SCREEN = Image.new(mode="RGBA", size=fb.size)
  SCRDRAW = ImageDraw.Draw(SCREEN)
  print("Framebuffer size: %d x %d" % (size[0], size[1]))
  
  #SCREEN.fill((0, 0, 0))        
  BUFFER.clear()
  WHEREX = 1
  WHEREY = 1
  for y in range(SCREENHEIGHT):
    for x in range(SCREENWIDTH):
      BUFFER.append([' ',7])
  
  
  
  font = ImageFont.truetype(FONTNAME, getfontsize())
  #CHARWIDTH = WIDTH // MODE['x']
  CHARWIDTH, CHARHEIGHT = font.getsize('#')
  CHARHEIGHT = getbigestcharheight()
  
  if WIDTH>CHARWIDTH*MODE['x']:
    SCR_OFFSET_X = (WIDTH-CHARWIDTH*MODE['x']) // 2
    if SCR_OFFSET_X < 0: SCR_OFFSET_X = 0

  #CHARHEIGHT = CHARWIDTH * (imgfont.fontimg.get_height() // imgfont.fontimg.get_width())
  if HEIGHT>CHARHEIGHT*MODE['y']:
    SCR_OFFSET_Y = (HEIGHT-CHARHEIGHT*MODE['y']) // 2
    if SCR_OFFSET_Y < 0: SCR_OFFSET_Y = 0
  print(f'Char. Width: {CHARWIDTH}, Height: {CHARHEIGHT}, Total: {80*CHARWIDTH}x{25*CHARHEIGHT}')
  print(f'Screen width: {WIDTH}, height: {HEIGHT}')
  print(f'Offset X: {SCR_OFFSET_X}, Y: {SCR_OFFSET_Y}')

def getbigestcharheight():
  global FONTSIZE,FONTNAME,font
  hh = 0
  for a in range(256):
    w,h = font.getsize(chr(a))
    if h>hh: hh = h
    
  return hh
    
  
  
def getfontsize():
  global FONTSIZE,FONTNAME,font
  a = FONTSIZE
  while True:
    a += 1
    font = ImageFont.truetype(FONTNAME, a)
    CHARWIDTH, CHARHEIGHT = font.getsize('#')
    print(CHARWIDTH,CHARWIDTH*80,WIDTH)
    if CHARWIDTH*MODE['x']>WIDTH:
      a -= 2
      return a
      break
  

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
  if c!='13':
    if WHEREY>SCREENHEIGHT: WHEREY = SCREENHEIGHT
    BUFFER[(WHEREY-1)*SCREENWIDTH+(WHEREX-1)][0]=chr(c)
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
        writechar(ord(c))
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
    
def writechar(c:int()):
  global SCREEN, CHARWIDTH, CHARHEIGHT, WHEREX, WHEREY, font, ATTR, SCRDRAW, SCR_OFFSET_X, SCR_OFFSET_Y
  global SCREENHEIGHT
  if c!=13:
    #pygame.draw.rect(SCREEN,bg2color(),(SCR_OFFSET_X+(CHARWIDTH*(WHEREX-1)),SCR_OFFSET_Y+(CHARHEIGHT*(WHEREY-1)),CHARWIDTH,CHARHEIGHT))
    #imgfont.writexy(SCREEN,SCR_OFFSET_X+(CHARWIDTH*(WHEREX-1)),SCR_OFFSET_Y+(CHARHEIGHT*(WHEREY-1)),c)
    x = SCR_OFFSET_X+(CHARWIDTH*(WHEREX-1))
    y = SCR_OFFSET_Y+(CHARHEIGHT*(WHEREY-1))
    SCRDRAW.rectangle(((x,y,x+CHARWIDTH,y+CHARHEIGHT)), fill=bg2color())
    #char = chr(c).encode('utf-8').decode('latin-1')
    #char = chr(c).encode('utf8').decode('latin-1')
    char = chr(c)
    #print(f'{char}, len:{len(char)}')
    SCRDRAW.text((x,y),char, font=font,fill=fg2color())
  else:
    WHEREX = 1
    WHEREY+= 1
    if WHEREY>SCREENHEIGHT:
      WHEREY=SCREENHEIGHT
      scrolldown()
  bufwritechar(c)
  
def write(s):
  for c in s:
    writechar(ord(c))
  
def writeln(st):
  write(st+'\n')
  
def writexy(x,y,a,s):
  textattr(a)
  gotoxy(x,y)
  write(s)
  
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
  #pygame.display.update()
  refresh()

def clrscr():
  global SCREEN
  SCREEN.paste( bg2color(), [0,0,SCREEN.size[0],SCREEN.size[1]])
  gotoxy(1,1)
  #update()
  
def scrolldown():
  global CHARHEIGHT, SCREEN, SCREENHEIGHT, SCREENWIDTH
  region = SCREEN.crop((0,CHARHEIGHT,SCREEN.size[0],SCREEN.size[1]))
  SCREEN.paste(region,(0,0,region.size[0],region.size[1]))
  SCRDRAW.rectangle(((0,SCREENHEIGHT-CHARHEIGHT,SCREENWIDTH,SCREENHEIGHT)), fill=bg2color())
  update()
  
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
  for i in range(y2-y1+1):
    gotoxy(x1,y1+i)
    #writechar(bg*(x2-x1))
    for a in range(x2-x1+1):
      writechar(ord(bg))
  
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

def readkey(echo=True):
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)
    extended=False
    if len(ch) == 1:
        if ch == ENTER:
            ch = KEY_ENTER
        elif ch == BACKSPACE:
            ch = KEY_BACK
        elif ch == SPACE:
            ch = KEY_SPACE
        elif ch == ESC:
            ch = KEY_ESCAPE
        elif ch == CTRL_A:
            ch = KEY_CTRLA
        elif ch == CTRL_B:
            ch = KEY_CTRLB
        elif ch == CTRL_C:
            ch = KEY_CTRLC
        elif ch == CTRL_D:
            ch = KEY_CTRLD
        elif ch == CTRL_E:
            ch = KEY_CTRLE
        elif ch == CTRL_F:
            ch = KEY_CTRLF
        elif ch == CTRL_G:
            ch = KEY_CTRLG
        elif ch == CTRL_H:
            ch = KEY_CTRLH
        elif ch == CTRL_I:
            ch = KEY_CTRLI
        elif ch == CTRL_J:
            ch = KEY_CTRLJ
        elif ch == CTRL_K:
            ch = KEY_CTRLK
        elif ch == CTRL_L:
            ch = KEY_CTRLL
        elif ch == CTRL_N:
            ch = KEY_CTRLN
        elif ch == CTRL_O:
            ch = KEY_CTRLO
        elif ch == CTRL_P:
            ch = KEY_CTRLP
        elif ch == CTRL_Z:
            ch = KEY_CTRLZ
        elif ch == CTRL_Y:
            ch = KEY_CTRLY
        elif ch == CTRL_W:
            ch = KEY_CTRLW
        elif ord(ch) < 32 or ord(ch) > 126:
            ch = ch
            if echo:
                write(ch)
    else:
        extended = True
        if ch == INSERT:
            ch = KEY_INS
        elif ch == PAGE_DOWN:
            ch = KEY_PGDN
        elif ch == PAGE_UP:
            ch = KEY_PGUP
        elif ch == HOME:
            ch = KEY_HOME
        elif ch == END:
            ch = KEY_END
        elif ch == F1:
            ch = KEY_F1
        elif ch == F2:
            ch = KEY_F2
        elif ch == F3:
            ch = KEY_F3
        elif ch == F4:
            ch = KEY_F4
        elif ch == F5:
            ch = KEY_F5
        elif ch == F6:
            ch = KEY_F6
        elif ch == F7:
            ch = KEY_F7
        elif ch == F8:
            ch = KEY_F8
        elif ch == F9:
            ch = KEY_F9
        elif ch == F10:
            ch = KEY_F10
        elif ch == F11:
            ch = KEY_F11
        elif ch == F12:
            ch = KEY_F12
        elif ord(ch[0]) == 27:
            if ch[1] == "[":
                if ch[2] == "A":
                    ch = KEY_UP
                elif ch[2] == "B":
                    ch = KEY_DOWN
                elif ch[2] == "C":
                    ch = KEY_RIGHT
                elif ch[2] == "D":
                    ch = KEY_LEFT
                elif ch[2] == "K" or ch[2]=="F":
                    ch = KEY_END
                elif ch[2] == "V":
                    ch = KEY_PGUP
                elif ch[2] == "U":
                    ch = KEY_PGDN
    
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return (ch, extended)
    
def getkey():
    return readkey()  

# INITIALIZE FRAMEBUFFER
fb = framebuffer(0)
init(fb.size)
key = None

# MAIN CODE
clrscr()
ansibox(1,1,79,25,box1)
cleararea(2,2,78,24,chr(176))
update()
ch,ext = readkey()
writexy(10,10,14,'hello')
update()
ch,ext = readkey()
for a in range(16):
  for b in range(16):
    writexy(10+a,2+b,14,chr(b*16+a))
update()
