#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
from time import strftime, sleep
import time, socket, Adafruit_DHT, requests, json
import RPi.GPIO as GPIO

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize DHT11 sensor for local temperature and humidity
temp_sensor = Adafruit_DHT.DHT11
temp_gpio = 17

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

# initialize data for weather API
api_key = '0d77ec45d15bebe907b5c11b6194067e'
root_url = 'http://api.openweathermap.org/data/2.5/weather?appid='
city_id = '5713376'
full_url = root_url + api_key + '&id=' + city_id

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

		# convert celsius to fahrenheit
		temp = temp * (9/5) + 32

		result = 'Inside: {0:0.1f}F'.format(temp)
	else:
		result = 'Inside: ERROR'

	# clear screen before posting the data
	lcd.clear()

	# return tuple of weather data strings
	return result

# function to get local weather from OpenWeather API
def get_api_weather():
	# request API for weather data
	response = requests.get(full_url)

	# store response of weather data
	respo = response.json()
	weather = respo['main']

	# pull the weather data we need
	api_temp = weather['temp']
	api_humid = weather['humidity']

	# convert temp from kelvin to fahrenheit
	api_temp = (api_temp - 273) * 1.8 + 32

	api_result = 'Outside: {0:0.1f}F'.format(api_temp)

	return api_result

# main control flow
display = 0
prev_ms = 0
prev_temps = 0
timer_switch_screen = 250
timer_IP_refresh = 1000
timer_temps_refresh = 120000

try:
	while True:
		ms = int(round(time.time() * 1000))

		# allow button presses to modify display
		button_1_press = not GPIO.input(18)

		# button1 switches screens
		if ((button_1_press) and (ms - prev_ms > timer_switch_screen)):
			display += 1
			if display > 1:
				display = 0
			prev_ms = int(round(time.time() * 1000))

		# display IP and datetime
		if display == 0:
			if (ms - prev_ms > timer_IP_refresh):
				ip = get_ip_address()
				current_time = get_current_time()
				lcd.clear()
				lcd.message('{}'.format(ip))
				lcd.message('\n')
				lcd.message(current_time)
				prev_ms = ms
		# display inside/outside temps
		elif display == 1:
			if (ms - prev_temps > timer_temps_refresh):
				inside_temp = get_local_temp()
				outside_temp = get_api_weather()
				lcd.clear()
				lcd.message(inside_temp)
				lcd.message('\n')
				lcd.message(outside_temp)
				prev_temps = ms

except KeyboardInterrupt:
	print('\nCTRL-C pressed. Program exiting...')

finally:
	lcd.clear()
