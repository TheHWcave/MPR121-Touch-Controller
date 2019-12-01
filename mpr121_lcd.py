#!/usr/bin/env python3
from time import sleep, time, localtime,strftime,perf_counter
import ST7735
from PIL import Image, ImageDraw, ImageFont

from MPR121 import MPR121

mpr121 = MPR121(3.3, 0x5a)
oor = mpr121.ReadOOR()
if oor != 0:
	print('autoconfig error: '+hex(oor))
mpr121.SetProxMode(0) # disable proximity


# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

font_size = 20
font = ImageFont.truetype("ttf/UbuntuMono-Regular.ttf", font_size)
text_colour = (255, 255, 255)
back_colour = (0, 0, 0)

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

try:
	while True:
		ts,ef = mpr121.Filtered()
		isTouched = [False] * 13
		msg = ''
		for el in range(13): 
			Touch = ((ts & (2**el)) != 0)
			isTouched[el] = Touch
			c = ' '
			if Touch:
				if el <= 9:
					c = chr(48+el)
				else:
					c = chr(55+el)
			msg = msg + c
		draw.rectangle([0,0,159,19],back_colour,None,0)
		draw.text((0,0),msg,font=font, fill=text_colour)
		
		# calculate a colour change based on capacitance of electrodes 0 and 1
		ratio = ef[0] / ef[1]
		r = abs(ratio - 0.9) * 5
		if r > 1.0 : r = 1.0
		col = int(255*r)
		
		# draw a circle filled with calculated colour
		if isTouched[0] or isTouched[1]:
			draw.ellipse([60,20,100,60],(255-col,col,255),None,0)
		else:
			draw.ellipse([60,20,100,60],(0,0,0),(255-col,col,255),2)
			
		# draw a filled red rectangle if electrode 2 is touched
		if isTouched[2]:
			draw.rectangle([10,20,50,60],(255,0,0),None,0)
		else:
			draw.rectangle([10,20,50,60],(0,0,0),(255,0,0),2)

		# draw a filled green rectangle if electrode 3 is touched
		if isTouched[3]:
			draw.rectangle([110,20,150,60],(0,255,0),None,0)
		else:
			draw.rectangle([110,20,150,60],(0,0,0),(0,255,0),2)
			
			
		disp.display(img)
		
		sleep(0.25)

except KeyboardInterrupt:
	disp.set_backlight(0)
	
