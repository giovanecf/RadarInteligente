from flask import Blueprint, render_template, request, flash, jsonify, Response, template_rendered
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import cv2

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/cam_profile/<id>')
def cam_profile(id):
    return render_template("cam_profile.html", id=id, user=current_user)

def generateVideo():

    cap = cv2.VideoCapture("http://187.19.166.182/mjpg/video.mjpg")
    #cap = cv2.VideoCapture("./static/video.mp4") 
    #no_image_hero = cv2.imread("/")

    while True:
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            yield "no-video"
        

@views.route("/video_feed")
def video_feed():
    return Response(generateVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route("/data_feed")
def data_feed():
    return {"fps":"0","counter":"1","mediumVelocity":"10","mediumDensity":"12","rpiName":"1231"}