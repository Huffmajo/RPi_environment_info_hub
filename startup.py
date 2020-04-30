#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import Adafruit_DHT

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=27, en=17, d4=14, d5=4, d6=3, d7=2, cols=16, lines=2)

# write message to LCD1602
def lcd_message(message):
	lcd.clear()
	lcd.message(message)

# welcome loading screen
lcd.clear()
lcd.message("LOADING...\n")
for i in range(16):
	lcd.message("*")
	sleep(0.5)

lcd.clear
lcd.message("***ENVIRO-HUB***\nSTATE: IDLE")

