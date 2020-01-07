# SecurityHub
Raspberry Pi based security hub.

Security feature to detect people in surveillance frame and notify user. Images are stored in Azure Blob Storage. 

## Hardware Requirements
- Raspberry Pi 3 B+
- Raspberry Pi Camera Module

## Software Requirements
- Raspbian Stretch
- Python 3.5
- OpenCV 3

## Install Instructions
- Install Raspbian Stretch via NOOBS  
https://www.raspberrypi.org/downloads/noobs/  
- Install OpenCV   
https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/  
- Install some additional dependencies  
> sudo apt-get install libatlas-base-dev  
> sudo apt-get install libjasper-dev  
> sudo apt-get install libqtgui4  
> sudo apt-get install python3-pyqt5  

## TeamViewer Update
Run apt-get update, then:
> sudo apt --fix-broken install
> teamviewer info

# TODO
Sorted by priority.
- Date based switch to turn camera on/off (google calendar integration)
- Change detection, to not score every image
- Product Setup (via App/Web)
- Frontend Image Viewer
- Connection with CCTV

# DONE
- Implement run on startup
- Convert to class: keep camera loaded
- Interval for email alerts, after first alert was sent
- Threshold for person detection
- Remove images from local storage