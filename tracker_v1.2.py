# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
import time
from flask import Flask, render_template, Response

app = Flask(__name__) #Ponto Critico. Talvez deva ser a primeira linha.

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
lastActive = {}
lastActiveCheck = datetime.now()

# stores the estimated number of Pis, active checking period, and
# calculates the duration seconds to wait before making a check to
# see if a device was active
ESTIMATED_NUM_PIS = 4
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

# assign montage width and height so we can view all incoming frames
# in a single "dashboard"
mW = 1
mH = 1

#inicialize fps
fps = 0

@app.route("/")
def homepage():
    return render_template("index.html")

def generateVideo():
# start looping over all the frames
    while True:
        start = time.time()

        # receive RPi name and frame from the RPi and acknowledge
        # the receipt
        (rpiName, frame) = imageHub.recv_image()
        imageHub.send_reply(b'OK')

        #For Flask
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

        end = time.time()
        fps = round((1.0/(end-start)), 2)
        fps_media = round((fps+(1.0/(end-start)))/2, 2)

        fps_label = f"FPS {fps}" 
        cv2.putText(frame, fps_label, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 4)
        cv2.putText(frame, fps_label, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        hostName = "Client: "+rpiName

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route("/video_feed")
def video_feed():
    return Response(generateVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

#put on air
if __name__ == "__main__": #true if main.py got executed direct, and not from other package or shit
    app.run(debug=True)