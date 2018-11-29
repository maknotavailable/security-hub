# import the necessary packages
import numpy as np
import imutils
import time
import cv2


def detect(frame, net, CLASSES, COLORS, conf=0.2):

    # grab the frame dimensions and convert it to a blob
    #(h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    pred = []
    score = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > conf:
            # Extract label
            idx = int(detections[0, 0, i, 1])
            # Store results
            pred.append(CLASSES[idx])
            score.append(confidence)

            ##TODO: for display only
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            # 
            # box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            # label = "{}: {:.2f}%".format(CLASSES[idx],
            #     confidence * 100)
            # (startX, startY, endX, endY) = box.astype("int")
            # cv2.rectangle(frame, (startX, startY), (endX, endY),
            #     COLORS[idx], 2)
            # y = startY - 15 if startY - 15 > 15 else startY + 15
            # cv2.putText(frame, label, (startX, y),
            #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # ##TODO: display frame
    # # show the output frame
    # cv2.imshow("Frame", frame)
    # time.sleep(5)
    # # # do a bit of cleanup
    # cv2.destroyAllWindows()

    return frame, pred, score

