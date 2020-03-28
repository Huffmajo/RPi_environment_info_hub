#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
from time import strftime, sleep
import time, socket, Adafruit_DHT, requests, json, subprocess
import RPi.GPIO as GPIO

# set gpio pins for i/o
left_button_gpio = 18
right_button_gpio = 15
power_button_gpio = 22
solenoid_gpio = 25

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) # left button
GPIO.setup(right_button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) # right button
GPIO.setup(power_button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) # power button
GPIO.setup(solenoid_gpio, GPIO.OUT) # water valve solenoid
GPIO.output(solenoid_gpio, GPIO.LOW) # start valve closed

# initialize DHT11 sensor for local temperature and humidity
temp_sensor = Adafruit_DHT.DHT11
temp_gpio = 10

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=27, en=17, d4=14, d5=4, d6=3, d7=2, cols=16, lines=2)

# initialize data for weather API
api_key = '0d77ec45d15bebe907b5c11b6194067e'
root_url = 'http://api.openweathermap.org/data/2.5/weather?appid='
city_id = '5713376'
full_url = root_url + api_key + '&id=' + city_id

# returns current ip address
def get_ip_address():
	return[
		(s.connect(('8.8.8.8', 53)),
		s.getsockname()[0],
		s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
	][0][1]

# returns date, day and time
def get_current_time():
	return datetime.now().strftime('%A\n%b %d %I:%M:%S')

# returns humidity and temperature from DHT11
def get_local_temp():
	# let user know temps are being measured
	lcd.clear()
	lcd.message('Measuring local\ntemp/humidity...')

	humidity, temp = Adafruit_DHT.read_retry(temp_sensor, temp_gpio)

	# convert celsius to fahrenheit
	temp = temp * (9/5) + 32

	# clear screen before posting the data
	lcd.clear()

	# return list of temperature and humidity
	return [temp, humidity]

# returns outside local weather from OpenWeatherMap API
def get_api_weather():
	# request API for weather data
	response = requests.get(full_url)

	# store response of weather data
	respo = response.json()
	weather = respo['main']

	return respo

# process for shutting down system
def shutdown():
	# display shutdown message
	lcd.clear()
	lcd.message("Shutting down.\nOne moment")

	# wait a moment
	sleep(5)
	lcd.clear()
	lcd.message("Safe for \npower down")

	# shutdown system
	subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)

# test print all weather info
def test_print_all():
	print ("CURRENT TEMPS @ {}".format(get_current_time()))
	print ("Outside temp: {}F".format(outside_temp))
	print ("Outside humidity: {}%".format(outside_humidity))
	print ("Outside recent rain: {}mm\n".format(rain_3h))

def record_weather():
	# create or open file
	weatherRecord = open("weather.txt", "a")

	# get date and time
	time = get_current_time()

	# get inside weather
	temp_in, humid_in = get_local_temp()

	# get outside weather
	weather_out = get_api_weather()
	main = weather_out['main']
	temp_out = (main['temp'] - 273) * 1.8 + 32
	humid_out = main['humidity']

	# get weather description
	weather_out =  weather_out['weather']
	weather_desc = weather_out[0]['main']

	# get rainfall


	# write formatted data to file

	# close file
	weatherRecord.close()

# main control flow
display = -1 # start with welcome screen
prev_ms = 0
prev_temps = 0
timer_switch_screen = 250
timer_IP_refresh = 1000
timer_temps_refresh = 120000
inside_temp = 0
inside_humidity = 0
outside_temp = 0
outside_humidity = 0
rain_1h = 0
description = 'None'

try:
	while True:
		ms = int(round(time.time() * 1000))

		# refresh weather information every 5 minutes
		if ((ms - prev_temps > timer_temps_refresh) or prev_temps == 0):
				# get inside temperature and humidity
				inside_temp, inside_humidity = get_local_temp()

				# get outside weather info
				outside_weather = get_api_weather()
				main = outside_weather['main']

				# pull the weather data we need
				outside_temp = main['temp']
				outside_humidity = main['humidity']

				# convert temp from kelvin to fahrenheit
				outside_temp = (outside_temp - 273) * 1.8 + 32

				# get weather description
				weather_main = outside_weather['weather']
				description = weather_main[0]['main']

				# get recent rain levels
				if outsidew_weather['rain'] != null:
					rain = outside_weather['rain']
					rain_1h = rain['1h']
				else:
					rain_1h = 0

				prev_temps = ms

		# allow button presses to modify display
		left_button_press = not GPIO.input(left_button_gpio)
		right_button_press = not GPIO.input(right_button_gpio)
		power_button_press = not GPIO.input(power_button_gpio)

		# test for solenoid triggering
		if (right_button_press):
			GPIO.output(solenoid_gpio, GPIO.HIGH)
		else:
			GPIO.output(solenoid_gpio, GPIO.LOW)

		# check for shutdown button press
		if (power_button_press):
			shutdown()

		# button1 switches screens
		if ((left_button_press) and (ms - prev_ms > timer_switch_screen)):
			display += 1
			if display > 2:
				display = 0
			prev_ms = int(round(time.time() * 1000))
			print('Left_button_press_success. Display: {}'.format(display))

		# welcome screen
		if display == -1:
			if (ms - prev_ms > timer_switch_screen):
				lcd.clear()
				lcd.message("***ENVIRO-HUB***\nPress any button")

				# right button also exits welcome screen
				if (right_button_press):
					display += 1
					print('Right_button_press_success. Display: {}'.format(display))
				prev_ms = ms

		# display datetime or IP
		elif display == 0:
			function = 1
			if (ms - prev_ms > timer_IP_refresh):
				# display date and time
				if function == 1:
					current_time = get_current_time()
					lcd.clear()
					lcd.message(current_time)
				elif function == -1:
					ip = get_ip_address()
					lcd.clear()
					lcd.message("IP address:\n{}".format(ip))
				prev_ms = ms

			# right button switches function
			if ((right_button_press) and (ms - prev_ms > timer_switch_screen)):
				if function == 1:
					function = -1
				else:
					function = 1
				prev_ms = int(round(time.time() * 1000))
				print('Right_button_press_success. Display: {}'.format(display))
				print('Function: {}'.format(function))

		# display inside/outside temps and humidity
		elif display == 1:
			function = 1

			if (ms - prev_ms > timer_IP_refresh):

				# display temps
				lcd.clear()
				inside_temp_print = 'Inside: {0:0.1f}F'.format(inside_temp)
				lcd.message(inside_temp_print)
				lcd.message('\n')
				outside_temp_print = 'Outside: {0:0.1f}F'.format(outside_temp)
				lcd.message(outside_temp_print)

				prev_ms = ms

			# right button switches function
			if ((Right_button_press) and (ms - prev_ms > timer_switch_screen)):
				if function == 1:
					function = -1
				else:
					function = 1
				prev_ms = int(round(time.time() * 1000))
				print('Right_button_press_success. Display: {}'.format(display))
				print('Function: {}'.format(function))

		# display outside weather info
		elif display == 2:
			function = 1

			if (ms - prev_ms > timer_IP_refresh):

				# display weather description and rainfall
				if function == 1:
					lcd.clear()
					lcd.message(description)
					lcd.message('\n')
					rain_print = 'Rainfall: {0:0.1f}mm'.format(rain_1h)
					lcd.message(rain_print)
				# display humidity
				elif function == -1:
					lcd.clear()
					inside_temp_print = 'Inside: {0:0.1f}%'.format(inside_humidity)
					lcd.message(inside_temp_print)
					lcd.message('\n')
					outside_humidity_print = 'Outside: {0:0.1f}F'.format(outside_humidity)
					lcd.message(outside_humidity_print)
				prev_ms = ms

			# right buttons switches function
			if (right_button_press):
				if function == 1:
					function = -1
				else:
					function = 1
				print('Right_button_press_success. Display: {}'.format(display))
				print('Function: {}'.format(function))

except KeyboardInterrupt:
	print('\nCTRL-C pressed. Program exiting...')

finally:
	lcd.clear()
