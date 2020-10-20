"""
SCRIPT TO DETECT PEOPLE IN IMAGE FRAMES, on RPI
1. start camera, snapshot at interval
2. score image
3. post-process
 a. if object detected: store image (blob), send message
 b. if none detected: store every Xth image (blob)
"""
import os
import cv2
import io
import numpy as np
import time
import datetime
import configparser
import imutils
import smtplib
import argparse
import logging

# Format logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s')

# Custom functions
from detect_person import detect
import camera as pica
import notification
# import storage

## INIT ##
# Load model
fp_deploy = '../model/MobileNetSSD_deploy.prototxt'
fp_model = '../model/MobileNetSSD_deploy.caffemodel'
# FP for local images
fp_img_local = '/home/pi/Desktop/Security/'
# Timer Last
timer_last = None
email_last = time.time()
# Email server
email = notification.Email()
# Storage server
# store = storage.Cloud()

def init(fp_deploy, fp_model):
    """Load model and dependencies"""
    global CLASSES, COLORS, net, config
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
        log.info("loading model...")
        net = cv2.dnn.readNetFromCaffe(fp_deploy, fp_model)

    except Exception as e:
        log.error('loading model failed: %s' % e)

def alert_email(path_local, pred, score):
    """Send an alert message via email about potential intruders.
    
    Set the interval in which emails after the first are ignored, in seconds.
    """
    # Prepare email
    # fn = path_local.split('/')[-1]
    # img_url = config['blob']['link-person'] + fn
    subject = 'ALARM - Human spotted in the residence !'
    body = 'The following objects were detected: %s with the following likelihood: %s. See the image here: %s' % (str(pred), str(score), str(img_url))
    
    # Send email
    email.send(subject, body)

def alert(frame, pred, score, interval=1800):
    """Evaluate frame for need to send alert"""
    global timer_last, email_last
    try:
        # Format date in human readable format
        now = ":".join(str(datetime.now()).split(":")[:2])

        # Step 1 - check for person
        ## a. check for person
        if 'person' in pred:
            log.info('person detected')
            fr = camera.capture(resize=False)

            fn_img_person = fp_img_local + now + '_person.jpg'
            cv2.imwrite(fn_img_person, frame)
            # Step 2 - upload image to blob
            # upload(fn_img_person, 'container-person')

            ## Take better resolution image:
            fn_img_person = fp_img_local + now + '_person_full.jpg'
            cv2.imwrite(fn_img_person, fr)
            # upload(fn_img_person, 'container-person', remove=False)

            # Step 3 - send alert email
            email_interval = time.time() - email_last
            if email_interval > interval:
                alert_email(fn_img_person, pred, score)
                email_last = time.time()
            else:
                log.info('email alert skipped. Last email was %s seconds ago.' % email_interval)
        ## b. upload based on timer
        fn_img_time = fp_img_local + now + '_time.jpg'
        if timer_last is None:
            cv2.imwrite(fn_img_time, frame)
            timer_last = datetime.datetime.now()
            # upload(fn_img_time, 'container-time')
        elif abs((timer_last - timer_start).total_seconds()) > 3600:
            cv2.imwrite(fn_img_time, frame)
            timer_last = datetime.datetime.now()
            # upload(fn_img_time, 'container-time')

    except Exception as e:
        log.error('While evaluating alert: %s' % e)

def score():
    global timer_start, camera
    ## Run arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--not_rpi',
                    action='store_false',
                    help="If non RPI device is used (for testing only)")
    parser.add_argument("--interval", 
                    default=5,
                    type=int,
                    help="Seconds between inferred frames.")      
    parser.add_argument("--confidence", 
                    default=0.4,
                    type=float,
                    help="Seconds between inferred frames.")        
    args = parser.parse_args()

    # Initialize run
    init(fp_deploy, fp_model)

    # Load camera
    camera = pica.Image(rpi=args.not_rpi)

    while True:
        # Start timer
        timer_start = datetime.datetime.now() 

        # Capture image
        frame = camera.capture(resize=True)

        # Detect Objects
        f, r, s = detect(frame, net, CLASSES, COLORS, conf = args.confidence)

        # Process results
        alert(f,r,s)
        log.info('loop complete: %s - %s - %s ' % (r, s, time.time()))
        
        ##Timer buffer
        time.sleep(args.interval)

if __name__ == "__main__":
    score()