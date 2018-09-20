import cv2
import time
from flask import Flask, render_template, Response


# import camera driver
from camera_opencv import Camera


app = Flask(__name__)


# get data from DHT sensor
def getDHTdata():
    hum = "33"
    temp = "22"
    return temp, hum


@app.route("/")
def index():
    timeNow = time.asctime(time.localtime(time.time()))
    temp, hum = getDHTdata()

    templateData = {
        'time': timeNow,
        'temp': temp,
        'hum': hum
    }
    return render_template('index.html', **templateData)


@app.route('/camera')
def cam():
    """Video streaming home page."""
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('camera.html', **templateData)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        frame = cv2.Canny(frame, 100, 200)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.178.32', threaded=True)
