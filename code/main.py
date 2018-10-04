## SCRIPT TO DETECT PEOPLE IN IMAGE FRAMES, on RPI
# 1. start camera, snapshot at interval
# 2. score image
# 3. post-process
### a. if object detected: store image (blob), send message
### b. if none detected: store every Xth image (blob)

import cv2
import io
import numpy as np
import time
import imutils

from detect_person import detect

## INIT ##
# Load model
fp_deploy = '../model/MobileNetSSD_deploy.prototxt'
fp_model = '../model/MobileNetSSD_deploy.caffemodel'
# FP for local images
fp_img_local = '/home/pi/Desktop/image.jpg'

def init(fp_deploy, fp_model):
    """Load model and dependencies"""
    global CLASSES, COLORS, net
    try:
        # initialize the list of class labels MobileNet SSD was trained to
        # detect, then generate a set of bounding box colors for each class
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(fp_deploy, fp_model)
    except Exception as e:
        print('Error loading model', str(e))

def capture(rpi):
    """Capture images using Rasperry Pi Camera"""
    try:
        if rpi:
            from picamera import PiCamera
            # IO Stream
            stream = io.BytesIO()
            with picamera.PiCamera() as camera:
                # Start Camera Stream
                camera.start_preview()
                ## Allow camera to warm up
                time.sleep(2)
                # Image to stream
                camera.capture(stream, format='jpeg', resize=(300,300))
                # Store image
                # camera.capture(fp_img_local)

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
            vs = VideoStream(src=0).start()
            # # vs = VideoStream(usePiCamera=True).start() ##NOTE: if using RPi
            time.sleep(2.0)
            # Read image
            frame = vs.read()
            # Resize frame
            frame = imutils.resize(frame, width=400)
            # Stop Recording
            vs.stop()

    except Exception as e:
        frame = None
        print('ERROR: image capture ' ,str(e))

    return frame

def alert(frame, pred, score):
    """Evaluate frame for need to send alert"""
    try:
        # Step 1 - check for person (or change?)
        ## a. check for person
        if 'person' in pred:
            print('person detected')
        ## b. lookup of found items - if change (object count, (location))
            # Step 2 - store results (image, pred, score)
            ##TODO: blob storage?
            # Step 3 - send alter email/other
            ##TODO: sendgrid?
    except Exception as e:
        print('Error while evaluating alert', str(e))

def score():
    # Initialize run
    init(fp_deploy, fp_model)

    while True: ##TODO: error with video stream
        # Capture image
        frame = capture(rpi=False)

        # Detect Objects
        f, r, s = detect(frame, net, CLASSES, COLORS, conf = 0.2)
        print('DONE', r ,s)

        # Process results
        alert(f,r,s)
        ##Timer buffer
        time.sleep(10)

if __name__ == "__main__":
    score()