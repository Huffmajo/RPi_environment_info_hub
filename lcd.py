#!/usr/bin/python
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
import socket
import RPi.GPIO as GPIO
import Adafruit_DHT

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize DHT11 sensor for local temperature and humidity
temp_sensor = Adafruit_DHT.DHT11
temp_gpio = 17

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

# function to get humidity and temperature from DHT11
def get_local_temp():
	# let user know temps are being measured
	lcd.message('Measuring local\ntemp/humidity...')

	humidity, temp = Adafruit_DHT.read_retry(temp_sensor, temp_gpio)

	# return error if DHT11 fails to detect humidity
	if humidity is not None and temp is not None:
		result = 'Temp: {0:0.1f}C\nHumidity: {1:0.1f}%'.format(temp, humidity)
	else:
		result = '***ERROR***\nNo temps read'

	# clear screen before posting the data
	lcd.clear()

	# return tuple of weather data strings
	return result

# main control flow
display = 0

try:
	while True:
		# allow button presses to modify display
		button_press = not GPIO.input(18)
		if button_press:
			display += 1
			if display > 2:
				display = 0

		lcd.clear()
		# display IP info
		if display == 0:
			ip = get_ip_address()
			lcd.message('IP ADDRESS\n')
			lcd.message('{}'.format(ip))
			sleep(1)
		# display date and time
		elif display == 1:
			current_time = get_current_time()
			lcd.message('TIME\n')
			lcd.message(current_time)
			sleep(1)
		# display measured weather info
		elif display == 2:
			measured_temp = get_local_temp()
			lcd.message(measured_temp)
			sleep(3)

except KeyboardInterrupt:
	print('\nCTRL-C pressed. Program exiting...')

finally:
	lcd.clear()
