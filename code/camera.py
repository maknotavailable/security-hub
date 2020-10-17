import os
import cv2
import io
import numpy as np
import time
import datetime
import imutils
import logging

# Format logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s')

class Image():
    def __init__(self, rpi=True):
        self.rpi = rpi

        if rpi:
            from picamera import PiCamera

            # Load camera
            self.camera = PiCamera()

            # Start preview
            self.camera.start_preview()
            ## Allow camera to warm up
            time.sleep(7)
            
            # Adjust camera settings
            self.camera.rotation = 180

        else:
            # TODO:
            pass

    def capture(self, resize=True):
        """Capture Image"""
        try:
            # IO Stream
            stream = io.BytesIO()
            
            # Capture
            if resize:
                self.camera.capture(stream, format='jpeg', resize=(400,400))
            else:
                self.camera.capture(stream, format='jpeg')
        
            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            
            # "Decode" the image from the array, preserving colour
            frame = cv2.imdecode(data, 1)

        except Exception as e:
            frame = None
            log.error('image capture failed: %s' % e)

        return frame

    def load_and_capture(self, resize=True):
        """Load camera and capture image using Rasperry Pi Camera. """
        try:

            if self.rpi:
                # Stop preview from init()
                self.camera.stop_preview()

                # IO Stream
                stream = io.BytesIO()
                with PiCamera() as camera:
                    # Start Camera Stream
                    camera.start_preview()
                    ## Allow camera to warm up
                    time.sleep(4)
                    # Image to stream
                    camera.rotation = 180
                    if resize:
                        camera.capture(stream, format='jpeg', resize=(400,400))
                    else:
                        camera.capture(stream, format='jpeg')
                    
                    # ## NOTE: for testing only ##
                    # # Store image
                    # fn_img_local = fp_img_local + str(time.time()) + '.jpg'
                    # camera.capture(fn_img_local)
                    # # upload image to blbo
                    # upload(fn_img_local, 'container-time')
                    # # send alert email
                    # alert_email(fn_img_local, 'test', 'nada')

                # Construct a numpy array from the stream
                data = np.fromstring(stream.getvalue(), dtype=np.uint8)
                # "Decode" the image from the array, preserving colour
                frame = cv2.imdecode(data, 1)
            else:
                ##NOTE: FOR LOCAL DEBUGGING
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                from imutils.video import VideoStream
                from imutils.video import FPS
                # Load video stream
                #vs = VideoStream(src=0).start()
                vs = VideoStream(usePiCamera=True).start() ##NOTE: if using RPi
                time.sleep(2.0)
                # Read image
                frame = vs.read()
                # Resize frame
                frame = imutils.resize(frame, width=400)
                # Stop Recording
                vs.stop()

        except Exception as e:
            frame = None
            log.error('image capture failed: %s' % e)

        return frame