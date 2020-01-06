from picamera import PiCamera
from time import sleep

# Load camera
camera = PiCamera()

# Start Camera Stream
camera.start_preview()
sleep(5) # sleep timer
print('[INFO] Camera Started')

# Rotate image, if needed
camera.rotation = 180

### PICTURE
# Store image
camera.capture('/home/pi/Desktop/image.jpg')

### VIDEO
# Start recording video
# camera.start_recording('/home/pi/video.h264')

# Stop recording video
# camera.stop_recording()

# End Camera Stream
camera.stop_preview()
print('[INFO] Camera Stopped')