# RPi_environment_info_hub
A  weather monitor that compares inside and outside weather conditions

## Hardware
Everything is operating on a Raspberry Pi Zero W running raspbian lite. All data is viewed through the 16x2 LCD screen and controlled through the 2 push buttons. A DHT22 is pulling local humidity and temperature for inside weather information.

## Software
All of the fun stuff is being run from lcd.py. Outside weather information is pulled from the OpenWeatherMap at regular intervals while local weather results are pulled from the DHT22 on demand.

## The Process
### Protoype
I prototyped the project to ensure all the parts were operational.
![Prototype wiring diagram](/Prototype_wiring_diagram.png)
![Prototype testboard](/First_prototype.jpg)
