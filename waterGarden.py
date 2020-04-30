#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
from time import sleep
import Adafruit_DHT
import RPi.GPIO as GPIO

# set gpio pins for i/o
solenoid_gpio = 25

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_gpio, GPIO.OUT) # water valve solenoid
GPIO.output(solenoid_gpio, GPIO.LOW) # start valve closed

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=27, en=17, d4=14, d5=4, d6=3, d7=2, cols=16, lines=2)

# write message to LCD1602
def lcd_message(message):
	lcd.clear()
	lcd.message(message)

# open solenoid valve
def open_valve():
	lcd_message("***VALVE OPEN***\nTIME LEFT: {}".format(duration))
	print("Valve opened at {} for {} minutes". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.HIGH)

# close solenoid valve
def close_valve():
	lcd_message("**VALVE CLOSED**")
	print("Valve closed at {}". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.LOW)

# main
duration = 30

open_valve()
for i in range(duration):
	lcd_message("***VALVE OPEN***\nTime left: {}".format(duration - i))
	sleep(60) # wait one minute
close_valve()
