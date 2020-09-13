# ENVIRO-HUB
The Enviro-hub is a weather monitoring and automated watering system for my veggie garden. At scheduled times (using cron), python scripts are run to collect climate information and water the plants (if it's not already raining). This climate information is then recorded to the weather log for later monitoring.

## Hardware
Everything is operating on a Raspberry Pi Zero W running raspbian lite. Updates to what the Enviro-Hub is doing is printed to the 16x2 LCD screen for clarity. A DHT11 is pulling local humidity and temperature for inside weather information. A 12V solenoid valve is used to open and close the flow of water to the garden. A TIP120 transistor lets the Raspberry Pi GPIO open and close the solenoid valve at will.

## Software
Scheduled tasks through cron run the python scripts at regular times. The script recordWeather.py gets climate information (outside from the OpenWeatherMap API and inside from the DHT11) and writes it to the weather log at 12AM and 12PM everyday. At 6AM and 6PM, waterGarden.py is run and waters the garden for 30 minutes if it's not already raining outside.

### Main Enclosure
Main componenets installed in an ABS project box. Knob and button on the side control screen brightness and power.
![Enclosure](/images/Enclosure.jpg)
![Layout](/images/Layout.jpg)
![Solenoid](/images/Solenoid.jpg)

## Next Steps
- Push the logged weather data to a webpage for long term monitoring of weather and watering habits. ChartJS could be used to attractively present the information.
- Photos of the wiring and inside of the enclosure.
- Step-by-step tutorial for others to follow.

####Sources
Air quaility information sourced from World Air Quality Index Project via https://aqicn.org/api/
