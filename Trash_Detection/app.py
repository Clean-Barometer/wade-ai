import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import base64
import os
import detect
import load_model
import cv2
from flask_pymongo import PyMongo
import json
from GPSPhoto import gpsphoto
from binascii import a2b_base64


app = Flask(__name__, static_folder='static')

mongodb_client = PyMongo(
    app, uri="mongodb+srv://user:1234@cluster0.vfc9s.mongodb.net/predictions?retryWrites=true&w=majority")
db = mongodb_client.db
collection = db.predictions


@app.route('/')
def upload_f():
    return render_template('upload.html')


@app.route('/map')
def showMap():
    data = collection.find({}, {'_id': False, 'time': False})
    return render_template('map.html', data=list(data))


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # get image
        f = request.files['file']
        geo_location = request.form
        print(geo_location)
        if not geo_location['lat'] and not geo_location['lon']:
            return render_template('redirect.html', resultMessege="Sorry! the image isn't geo tagged")

        # TODO CHECK IF IMAGE IS GEO TAGGED IF NOT DO NOT DETECT

        image = base64.b64encode(f.read())
        jpg_original = base64.b64decode(image)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)

        # TODO SEND THE LOCATION TO DETECT FUNCTION
        # get detection
        resultMessege = detect.detect_garbage(img, geo_location)

        # TODO RETURN TO INDEX.HTML

        # return 'file uploaded successfully'
        return render_template('redirect.html', resultMessege=resultMessege)


if __name__ == '__main__':
    # model, classes = load_model.load_model()

    app.run(debug=True, port=8909)
