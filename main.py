import cv2
from ImageProcess import FaceProcess
import requests
import threading as th
import time
import numpy as np
from flask import Flask
from flask import request
from flask_cors import *
import json
from PIL import Image
import base64
import io

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# Enable CORS
CORS(app, supports_credentials=True)

# Users can change the following parameters
url_stranger = 'https://maker.ifttt.com/trigger/strangerdetect/with/key/cUXwhgUTcUmlTgd6DhhawX'
url_package = 'https://maker.ifttt.com/trigger/PackageCall/with/key/cUXwhgUTcUmlTgd6DhhawX'
filename = 'dataset/known_face.csv'

# Users shouldn't change the following parameters
stranger = 0
package = 1
check_flag = True
flags = [True, True]


# Send Message with IFTTT APIs
def send_message(url):
    response = requests.post(url)
    print(response.content)


# Check the status of elements
def check_status():
    global flags
    while check_flag:
        if False in flags:
            index = flags.index(False)
            flags[index] = True
        time.sleep(30)


# Configure the face recognition process
filename = 'dataset/known_face.csv'
face_rgn = FaceProcess(resize_frame=1, recognize_threshold=0.4, detect_interval=0)
face_rgn.load_database(filename)

# Configure the camera
# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280.0)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720.0)

# Check the flags
# th.Thread(target=check_status).start()

# Configure the window
# cv2.namedWindow('Detection', cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


@app.route('/')
def root():
    return "Hello"


@app.route('/test', methods=['POST'])
def test():
    print(request.data)
    news = dict(request.form)
    image_bytes = io.BytesIO(base64.b64decode(news['img'].split(',')[1]))
    im = Image.open(image_bytes)
    image = np.array(im)

    print(image)

    return "MY POST"


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        # Get news from POST
        news = json.loads(request.data)
        img_url = news['img'].split(',')[1]

        # Convert url to image
        img = url_to_image(img_url)

        # Detect people and recognize them
        face_positions = face_rgn.detect_people(img)

        # Return the results
        face_pos = {"face_pos": face_positions}
        return json.dumps(face_pos)
    else:
        face_names = face_rgn.recognize_people()
        face_nam = {"face_name": face_names}

        return json.dumps(face_nam)


@app.route('/save', methods=['POST'])
def save_remove():
    # Get news from POST
    news = json.loads(request.data)
    status = False
    if news["mode"] == "remove":
        face_rgn.delete_data(filename, news["name"])
        status = True
    elif news["mode"] == "add":
        img_url = news['img'].split(',')[1]
        img = url_to_image(img_url)
        status = face_rgn.save_database(filename, news["name"], img)

    rtn_message = {"status": status}
    return json.dumps(rtn_message)


def url_to_image(img_url):
    image_bytes = io.BytesIO(base64.b64decode(img_url))
    im = Image.open(image_bytes)
    img = np.array(im)
    return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8081, debug=True)
    pass
