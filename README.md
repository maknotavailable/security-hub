# Security Hub
Raspberry Pi based security hub.

Security feature to detect people in surveillance frame and notify user. Images are stored in Azure Blob Storage. 

# REQUIREMENTS
## Hardware Requirements
- Raspberry Pi 3 B+
- Raspberry Pi Camera Module

## Software Requirements
- Raspbian Stretch
- Python 3.5
- OpenCV 3

# INSTRUCTIONS
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

# VERSIONS
## TODO
- Improve email sending security
- Date based switch to turn camera on/off (google calendar integration)
- Change detection, to not score every image
- Web logging
- Product Setup (via App/Web)
- Email notification via API service
- Frontend Image Viewer
- Migrate storage to AWS S3 Bucket

## DONE
- [2020-08-17] Updated Logging
### v0.1
- [2020-01-07] Implement run on startup
- [2020-01-06] Convert to class: keep camera loaded
- [2019-01-17] Interval for email alerts, after first alert was sent
- [2019-01-14] Threshold for person detection
- [2018-11-30] Remove images from local storage