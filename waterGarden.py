#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
from time import sleep
import Adafruit_DHT, requests
import RPi.GPIO as GPIO

# set gpio pins for i/o
solenoid_gpio = 25

# initialize GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_gpio, GPIO.OUT) # water valve solenoid
GPIO.output(solenoid_gpio, GPIO.LOW) # start valve closed

# initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=27, en=17, d4=14, d5=4, d6=3, d7=2, cols=16, lines=2)

# initialize data for weather API
api_key = '0d77ec45d15bebe907b5c11b6194067e'
root_url = 'http://api.openweathermap.org/data/2.5/weather?appid='
city_id = '5713376'
full_url = root_url + api_key + '&id=' + city_id

# write message to LCD1602
def lcd_message(message):
	lcd.clear()
	lcd.message(message)

# open solenoid valve
def open_valve():
	print("Valve opened at {} for {} minutes". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.HIGH)

# close solenoid valve
def close_valve():
	print("Valve closed at {}". format(datetime.now(), duration))
	GPIO.output(solenoid_gpio, GPIO.LOW)

# returns local weather description from OpenWeatherMap API
def get_weather_description():
	# request API for weather data
	response = requests.get(full_url)

	# store response of weather data
	respo = response.json()
	weather = respo['main']

	return respo['weather'][0]['main']

# main
duration = 30

# if currently raining, no need to water
curr_weather = get_weather_description()

if curr_weather is 'Thunderstorm' or 'Drizzle' or 'Rain' or 'Snow':
	lcd_message("No water needed\n{}".format(curr_weather))
	print("Garden not watered due to current weather conditions, {}".format(curr_weather))
else:
	open_valve()
	for i in range(duration):
		lcd_message("***VALVE OPEN***\nTime left: {}".format(duration - i))
		sleep(60) # wait one minute
	close_valve()
	lcd_message("**VALVE CLOSED**")

