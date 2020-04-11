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
	lcd_message("Shutting down\nOne moment")

	# wait a moment
	sleep(5)

	# update message
	lcd_message("Safe for \npower down")

	# shutdown system
	subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)

# write message to LCD1602
def lcd_message(message):
	lcd.clear()
	lcd.message(message)

# open solenoid valve
def open_valve():
	lcd_message("***VALVE OPEN***")
	print("Valve opened at {} for {} minutes". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.HIGH)

# close solenoid valve
def close_valve():
	lcd_message("**VALVE CLOSED**")
	print("Valve closed at {}". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.LOW)

# get and write weather info to text log
def record_weather(watered):
	# create or open file
	weatherRecord = open("weather.txt", "a")

	# get date and time
	time = get_current_time()

	# get inside weather
	temp_in, humid_in = get_local_temp()

	# get outside weather
	weather_out = get_api_weather()
	temp_out = (weather_out['main']['temp'] - 273) * 1.8 + 32
	humid_out = ['main']['humidity']

	# get weather description
	weather_desc = weather_out['weather'][0]['description']

	# get rainfall
	if "rain" in weather_out:
		rain = outside_weather['rain']
		rain_1h = outside_weather['rain']['1h']
	else:
		rain_1h = 0

	# write all info to file
	weatherRecord.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(time, watered, weather_desc, temp_in, temp_out, humid_in, humid_out, rain_1h));

	# close file
	weatherRecord.close()

# main control flow
display = -1 # start with welcome screen
prev_ms = 0
quarter_sec = 250
one_sec = 1000
one_min = 60000
two_min = 120000
description = 'None'
wateredToday = False

# set scheduled times
amHour = 6
amMinute = 0
pmHour = 18
pmMinute = 0
duration = 15
now = datetime.now()

try:
	while True:
		# allow button presses to modify display
		left_button_press = not GPIO.input(left_button_gpio)
		right_button_press = not GPIO.input(right_button_gpio)
		power_button_press = not GPIO.input(power_button_gpio)


		# check for shutdown button press
		if (power_button_press):
			shutdown()

		# increment counter
		ms = int(round(time.time() * 1000))

		# update once a minute
		if (ms - prev_ms > one_min):
			# show current time
			lcd_message(get_current_time())
			now = datetime.now()
			print(now) # USED FOR DEBUG

			# check for scheduled water time
			if (now.hour == amHour and now.minute == amMinute) or (now.hour == pmHour and now.minute == pmMinute):
				open_valve()
				sleep(60 * duration)
				close_valve()

				wateredToday = True
				record_weather(wateredToday)
				wateredToday = False

			prev_ms = ms

		# override watering
		if (right_button_press):
			open_valve()
			sleep(60 * duration)
			close_valve()

except KeyboardInterrupt:
	print('\nCTRL-C pressed. Program exiting...')

finally:
	close_valve()
