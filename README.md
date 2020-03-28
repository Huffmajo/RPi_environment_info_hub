# ENVIRO-HUB
A weather monitor that compares inside and outside weather conditions to determine when to best utilize climate control features. The hub has recently been upgraded to automatically water my garden at regular intervals based on recent rain conditions.

## Hardware
Everything is operating on a Raspberry Pi Zero W running raspbian lite. All data is viewed through the 16x2 LCD screen and controlled through the 2 push buttons. A DHT11 is pulling local humidity and temperature for inside weather information. A 12V solenoid valve is used to open and close the flow of water to the garden. A relay connects the Raspberry Pi and solenoid valve to allow the Pi to open and close the valve.
The current wiring diagram can be seen below.
![Wiring Diagram](/images/RPi_weather_station_ver3_labels.jpg)

## Software
All of the fun stuff is being run from lcd.py. Outside weather information is pulled from the OpenWeatherMap at regular intervals while local weather results are pulled from the DHT11 on demand. The lcd.py script is run on OS start-up automatically by launcher.sh with cron.

## The Process
### Protoype
I prototyped the project to ensure all the parts were operational.
![Prototype wiring diagram](/images/Prototype_wiring_diagram.png)
![Prototype testboard](/images/First_prototype.jpg)

### Main Enclosure
Main componenets installed in an ABS project box. Two push buttons control the current information displayed on the LCD screen. Knob and button on the side control screen brightness and power.
![Enclosure](/images/Enviro-Hub.jpg)
