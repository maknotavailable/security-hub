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
import datetime
import configparser
import imutils
from azure.storage.blob import BlockBlobService
import smtplib

# Load custom functions
from detect_person import detect

## INIT ##
# Load model
fp_deploy = '../model/MobileNetSSD_deploy.prototxt'
fp_model = '../model/MobileNetSSD_deploy.caffemodel'
# FP for local images
fp_img_local = '/home/pi/Desktop/Security/'
# Timer Last
timer_last = None

def init(fp_deploy, fp_model):
    """Load model and dependencies"""
    global CLASSES, COLORS, net, block_blob_service, config, server
    try:
        # Load config file
        config = configparser.ConfigParser()
        config.read('../config.ini')

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

        # prepare blob connection
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=config['blob']['account'], account_key=config['blob']['key'])

    except Exception as e:
        print('[ERROR] loading model failed: ', str(e))

def upload(path_local, container_name):
    """Upload image to Azure Blob Storage"""
    try:
        fn = path_local.split('/')[-1]
        block_blob_service.create_blob_from_path(config['blob'][container_name], fn, path_local)
        print('[INFO] Uploaded image to blob storage: ', container_name)
    except Exception as e:
        print('[ERROR] Uploading image failed: ', str(e))

def alert_email(path_local, pred, score):
    """Send an alert message via email about potential intruders."""
    try:
        # Prepare Email
        fn = path_local.split('/')[-1]
        img_url = config['blob']['link-person'] + fn
        sender = config['email']['sender']
        receiver = config['email']['receiver'].split(',')
        subject = 'IBIZA Alert - Human Spotted in the Residence'
        body = 'A Human has been spotted in the residence. \
        The following objects were detected: %s with the \
        following likelihood: %s . \
        See the image here: %s' % (str(pred),str(score),str(img_url))

        email_text = """Subject: %s

        %s
        """ % (subject, body)

        # Send Email
        server = smtplib.SMTP_SSL(config['email']['server'], 465)
        server.ehlo()
        server.login(sender, config['email']['key'])
        server.sendmail(sender, receiver, email_text)
        server.close()
        print('[INFO] sent email alert')
    except Exception as e:
        print('[ERROR] sending alert email failed: ', str(e))

def alert(frame, pred, score):
    """Evaluate frame for need to send alert"""
    global timer_last
    try:
        # Step 1 - check for person (TODO: or change?)
        ## a. check for person
        if 'person' in pred:
            print('person detected')
            fn_img_person = fp_img_local + str(time.time()) + '_person.jpg'
            cv2.imwrite(fn_img_person, frame)
            # Step 2 - upload image to blob
            upload(fn_img_person, 'container-person')

            ## Take better resolution image:
            fr = capture(rpi=True, resize=False)
            fn_img_person = fp_img_local + str(time.time()) + '_person2.jpg'
            cv2.imwrite(fn_img_person, fr)
            upload(fn_img_person, 'container-person')

            # Step 3 - send alert email
            alert_email(fn_img_person, pred, score)
        ## b. upload based on timer
        fn_img_time = fp_img_local + str(time.time()) + '_time.jpg'
        if timer_last is None:
            cv2.imwrite(fn_img_time, frame)
            timer_last = datetime.datetime.now()
            upload(fn_img_time, 'container-time')
        elif abs((timer_last - timer_start).total_seconds()) > 3600:
            cv2.imwrite(fn_img_time, frame)
            timer_last = datetime.datetime.now()
            upload(fn_img_time, 'container-time')

    except Exception as e:
        print('[ERROR] While evaluating alert: ', str(e))

def capture(rpi, resize=True):
    """Capture images using Rasperry Pi Camera"""
    try:
        if rpi:
            from picamera import PiCamera
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
        print('[ERROR] image capture failed: ' ,str(e))

    return frame

def score():
    global timer_start
    # Initialize run
    init(fp_deploy, fp_model)

    while True:
        # Start timer
        timer_start = datetime.datetime.now() 

        # Capture image
        frame = capture(rpi=True)

        # Detect Objects
        f, r, s = detect(frame, net, CLASSES, COLORS, conf = 0.2)

        # Process results
        alert(f,r,s)

        print('[INFO] loop complete: ', r ,s, str(time.time()))
        ##Timer buffer
        time.sleep(11)

if __name__ == "__main__":
    score()