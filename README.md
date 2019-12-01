# MPR121-Touch-Controller
Python3 driver for the MPR121 chip (for example Adafruit  breakout board 1982 or compatible)

I created this driver to possibly use the MPR121 capacitive touch controller as a keyboard input for a Raspberry Pi with an Pimoroni Enviro+ board plugged in. The Enviro+ covers all GPIO pins but still allows access to the I2C bus. The MPR121 has an I2C interface and has 12 pins that can be electrodes or GPIO or LED drivers. This driver currently only supports the capacitive electrodes. It does not support GPIO or LED mode, but that may come in the future... 

The mpr121_lcd.py is a little test program that uses the MPR121 driver. It assumes an Enviro+ board is plugged in and uses the LCD screen to display a two squares and a circle. The squares indicate the status of electrodes 2 and 3 and the circle colour is determined by the ratio of capacitance of electrodes 0 and 1. 
