import cv2
from ImageProcess import FaceProcess
import requests
import threading as th
import time
import numpy as np
from flask import Flask
from firebase import MyDataBase
from flask import request
from flask_cors import *
import json
from PIL import Image

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
face_rgn = FaceProcess(resize_frame=1, recognize_threshold=0.6,
                       detect_interval=1, person_store_number=10, filename=filename)
face_rgn.load_database()

# Configure the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280.0)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720.0)

# Configure the database
my_database = MyDataBase()

# Check the flags
# th.Thread(target=check_status).start()

# Configure the window
# cv2.namedWindow('Detection', cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


@app.route('/')
def root():
    return "Hello"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the data from request
        ans = dict(request.form)

        # Format the data
        tmp = ans['img'][1:-2].split(',')
        img_list = list(map(float, tmp))
        img_list = list(map(int, img_list))
        width = int(ans['width'])
        height = int(ans['height'])

        # Transfer data to img
        img = np.reshape(np.array(img_list, dtype=np.uint8), (height, width))
        # img = np.array([img, img, img])
        # cv2.imwrite('test.png', img)

        # print(img)

        # Detect people and recognize them
        face_rgn.detect_people(img)
        face_names, face_positions = face_rgn.get_faces_info(img)

        # Return the results
        new_data = {"face_names": face_names, "face_pos": face_positions}
        return json.dumps(new_data)
    else:
        return "MY GET!"




# # When everything is done, release the capture
# camera.release()
# # cv2.destroyAllWindows()
# face_rgn.stop_recognize_thread()
# check_flag = False


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8081, debug=True)
    pass
