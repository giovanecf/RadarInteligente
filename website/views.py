from flask import Blueprint, render_template, Response
import time
import cv2
import imagezmq
from datetime import datetime

views = Blueprint('views', __name__)

imageHub = imagezmq.ImageHub()

lastActive = {}
lastActiveCheck = datetime.now()

ESTIMATED_NUM_PIS = 4
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

mW = 1
mH = 1


@views.route('/')
def home():
    return render_template("home.html")

def generateVideo():

    while True:

        # receive RPi name and frame from the RPi and acknowledge
        # the receipt
        (rpiName, frame) = imageHub.recv_image()
        imageHub.send_reply(b'OK')
        #print("Receving from: "+str(rpiName))
            
        #For Flask
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        
        hostName = "Client: "+rpiName

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@views.route("/video_feed")
def video_feed():
    return Response(generateVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')
