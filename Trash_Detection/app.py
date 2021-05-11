import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import base64
import os
import detect
import cv2
from flask_pymongo import PyMongo
import json 
app = Flask(__name__, static_folder='static')

mongodb_client = PyMongo(app, uri="mongodb+srv://user:1234@cluster0.vfc9s.mongodb.net/predictions?retryWrites=true&w=majority")
db = mongodb_client.db
collection = db.predictions


@app.route('/')
def upload_f():
    return render_template('upload.html')

# TODO ADD ROUTE FOR MAP

@app.route('/map')
def showMap():
    data = collection.find()

    return render_template('map.html', data = list(data))


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # get image
        f = request.files['file']

        # TODO EXTRACT GEO LOCATION

        # TODO CHECK IF IMAGE IS GEO TAGGED IF NOT DO NOT DETECT

        image = base64.b64encode(f.read())
        jpg_original = base64.b64decode(image)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)

        # TODO SEND THE LOCATION TO DETECT FUNCTION
        # get detection
        resultMessege = detect.detect_garbage(img)

        # TODO RETURN TO INDEX.HTML
        return resultMessege


# if __name__ == '__main__':
app.run(debug=True, port=8989)
