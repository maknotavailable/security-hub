# SecurityHub
Raspberry Pi based security hub.

Security feature to detect people in surveillance frame and notify user. Images are stored in Azure Storage Blobs. 

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
