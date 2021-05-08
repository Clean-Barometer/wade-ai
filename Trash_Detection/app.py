import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import base64
import os
import detect
import cv2
app = Flask(__name__, static_folder='static')


@app.route('/')
def upload_f():
    return render_template('upload.html')

# TODO ADD ROUTE FOR MAP


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
