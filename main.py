from flask import Flask, render_template, Response
import time
import cv2

app = Flask(__name__)

#build  first page
# every page has ROUTE(www.site.com/"myroute") and
# FUNCTION(what u want in page)

#... and a template, if u will

#@ is a decorator. This gives a function to nex line
#@app.route("/aulas")
#@app.route("/home")
@app.route("/")
def homepage():
    return render_template("index.html")

def generateVideo():
    #cap = cv2.VideoCapture("http://187.19.166.182/mjpg/video.mjpg")
    cap = cv2.VideoCapture("http://187.19.166.182/mjpg/video.mjpg")

    while True:
        ret, img = cap.read()

        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break

@app.route("/video_feed")
def video_feed():
    return Response(generateVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/users/<user_name>")
def user(user_name):
    return render_template("users.html", user_name=user_name)

#put on air
if __name__ == "__main__": #true if main.py got executed direct, and not from other package or shit
    app.run(debug=True)