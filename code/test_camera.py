from picamera import PiCamera
from time import sleep

# Load camera
camera = PiCamera()

# Rotate image, if needed
# camera.rotation = 180

# Start Camera Stream
camera.start_preview()

# Start recording video
# camera.start_recording('/home/pi/video.h264')
sleep(10) # sleep timer

# Stop recording video
# camera.stop_recording()

# Store image
# camera.capture('/home/pi/Desktop/image.jpg')

# End Camera Stream
camera.stop_preview()