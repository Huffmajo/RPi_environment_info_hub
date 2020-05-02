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

# get and write weather info to text log
def record_weather():
	# create or open file
	weatherRecord = open("weather.txt", "a")

	# get date and time
	time = datetime.now().strftime('%A %b %d %I:%M:%S')

	# get inside weather
	temp_in, humid_in = get_local_temp()

	# get outside weather
	weather_out = get_api_weather()
	temp_out = (weather_out['main']['temp'] - 273) * 1.8 + 32
	humid_out = weather_out['main']['humidity']

	# get weather class
	weather_main = weather_out['weather'][0]['main']

	# get weather description
	weather_desc = weather_out['weather'][0]['description']

	# write all info to file
	weatherRecord.write("{},{},{},{},{},{},{}\n".format(time, weather_main, weather_desc, temp_in, temp_out, humid_in, humid_out));
	print("{},{},{},{},{},{},{}\n".format(time, weather_main, weather_desc, temp_in, temp_out, humid_in, humid_out));

	# close file
	weatherRecord.close()

# main
record_weather()
