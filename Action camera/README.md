# Action camera
A very compact DIY camera that has similar functionality and specs with a GoPro.

## Features:
* Built-in screen for displaying several usefull info: memory left, time, quality of photo and video
* 3 Modes: Photos, Videos and Timelapse
* 5h battery life
* Friendly design

## Parts needed for this project:
* Raspberry Pi Camera
* Raspberry Pi Zero W
* The official Raspberry pi Zero case (comes with cable for connecting the camera to the board)
* a micro SD card (with Raspian)
* An [Adafruit PowerBoost](https://www.adafruit.com/product/1944) in combination with a LiPoly battery such as [this](https://www.adafruit.com/product/258) one.
* 4 Tactile buttons
* An OLED display 128x64

## Software:
In order to run the script you need to have installed th following libraries:
* RPi.GPOI
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo pip install RPi.GPIO

* imaging labrary
sudo apt-get install python-imaging python-smbus

* the SSD1306 library made by Adafruit
sudo apt-get install git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python3 setup.py install

After doing all this there are 2 more steps you need to do:
1) you copy the script from this repository onto your desktop's pi 
2) make it run at startup. You do this by:
* Opening a terminal
* typing sudo nano /etc/rc.local
* adding at the end of the script but not after the exit 0 line the following line: sudo python3 /home/pi/Desktop/script.py &.

## Hooking everything up together 
To be continued....
