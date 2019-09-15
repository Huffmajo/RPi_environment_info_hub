#!/usr/bin/python
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
import socket
import RPi.GPIO as GPIO

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

# function to get IP info
def get_ip_address():
	return[
		(s.connect(('8.8.8.8', 53)),
		s.getsockname()[0],
		s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
	][0][1]

# function to get time
def get_current_time():
	return datetime.now().strftime('%b %d %H:%M:%S')

# main control flow
display = 0

try:
	while True:
		# allow button presses to modify display
		button_press = not GPIO.input(18)
		if button_press:
			display += 1
			if display > 1:
				display = 0

		lcd.clear()
		if display == 0:
			ip = get_ip_address()
			lcd.message('IP ADDRESS\n')
			lcd.message('{}'.format(ip))
			sleep(1)
		elif display == 1:
			current_time = get_current_time()
			lcd.message('TIME\n')
			lcd.message(current_time)
			sleep(1)

except KeyboardInterrupt:
	print('\nCTRL-C pressed. Program exiting...')

finally:
	lcd.clear()
