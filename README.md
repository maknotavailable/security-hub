# SecurityHub
Raspberry Pi based security hub.

Security feature to detect people in surveillance frame and notify user. Images are stored in Azure Blob Storage. 

## Hardware Requirements
- Raspberry Pi 3 B+
- Raspberry Pi Camera Module

## Software Requirements
- Raspbian Stretch
- Python 3
- OpenCV 3

## Install Instructions
- Install Raspbian Stretch via NOOBS  
https://www.raspberrypi.org/downloads/noobs/  
- Install OpenCV   
https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/  
- Install some additional dependencies  
sudo apt-get install libatlas-base-dev  
sudo apt-get install libjasper-dev  
sudo apt-get install libqtgui4  
sudo apt-get install python3-pyqt5  

## Run on Startup
Add the following to your /etc/rc.local file:
/usr/bin/tvservice -o (-p to re-enable)
sudo python3 /home/pi/Desktop/SecurityHub/code/main.py &

# TODO
- Implement run on startup
- Date based switch to turn camera on/off (google calendar integration)
- Change detection, to not score every image
- Connection with CCTV
# DONE
- Interval for email alerts, after first alert was sent
- Threshold for person detection