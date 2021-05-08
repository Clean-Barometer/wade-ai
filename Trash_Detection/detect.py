

# TODO ADD LOCATION PARAMETER
def detect_garbage(image):

    from trash import trash
    from mrcnn.model import log
    import mrcnn.model as modellib
    from mrcnn.visualize import display_images
    from mrcnn import visualize
    from mrcnn import utils
    import os
    import sys
    import random
    import math
    import re
    import time
    import glob
    import skimage
    import numpy as np
    import tensorflow as tf
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import cv2
    from pymongo import MongoClient
    import base64
    from datetime import datetime

    # Root directory of the project.
    # Change in case you want to put the notebook somewhere else.
    ROOT_DIR = os.getcwd()
    print(ROOT_DIR)

    # Import Mask RCNN
    sys.path.append(ROOT_DIR)  # To find local version of the library

    # plt.show()

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Path to Trash trained weights
    TRASH_WEIGHTS_PATH = "weights/mask_rcnn_trash_0200_030519_large.h5"
    # the best

    print('Weights being used: ', TRASH_WEIGHTS_PATH)

    # Configurations

    config = trash.TrashConfig()
    TRASH_DIR = 'trash'

    # Override the training configurations with a few
    # changes for inferencing.

    class InferenceConfig(config.__class__):
        # Run detection on one image at a time
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    config.display()

    # Notebook Preferences

    # Device to load the neural network on.
    # Useful if you're training a model on the same
    # machine, in which case use CPU and leave the
    # GPU for training.
    DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

    # Inspect the model in training or inference modes
    # values: 'inference' or 'training'
    TEST_MODE = "inference"

    def get_ax(rows=1, cols=1, size=16):
        """Return a Matplotlib Axes array to be used in
        all visualizations in the notebook. Provide a
        central point to control graph sizes.

        Adjust the size attribute to control how big to render images
        """
        _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
        return ax

    # Load Validation Dataset

    # Load validation dataset
    dataset = trash.TrashDataset()
    dataset.load_trash(TRASH_DIR, "val")

    # Must call before using the dataset
    dataset.prepare()

    print("Images: {}\nClasses: {}".format(
        len(dataset.image_ids), dataset.class_names))

    # Load Model

    # Create model in inference mode
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(
            mode="inference", model_dir=MODEL_DIR, config=config)

    # Load the weights you trained
    weights_path = os.path.join(ROOT_DIR, TRASH_WEIGHTS_PATH)
    model.load_weights(weights_path, by_name=True)
    print("Loading weights ", TRASH_WEIGHTS_PATH)

    # image = skimage.io.imread('{}'.format("images/trash_55.jpg"))
    # print(type(image))
    # Run object detection
    results = model.detect([image], verbose=1)

    # Display results

    r = results[0]
    result = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                         dataset.class_names, r['scores'],
                                         title="Predictions")

    # CEHCK IF THE IMAGE HAS GARBAGE IF YES DO:
    if True in  r["masks"][:, 0, 0]:

        # CONVERT IMAGES OT URI
        retval, buffer = cv2.imencode('.jpg',  result)
        jpg_as_text = base64.b64encode(buffer)
        predicted = jpg_as_text.decode('ASCII')

        retval, buffer = cv2.imencode('.jpg',  image)
        jpg_as_text = base64.b64encode(buffer)
        original = jpg_as_text.decode('ASCII')

        # PUSH TO DATABASE INCLUDING GEO LOCATION
        client = MongoClient("mongodb+srv://user:1234@cluster0.vfc9s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db=client.predictions
        collection = db.predictions

        record ={
                "loc" : { "type": "Point", "coordinates": [ -73.97, 40.77 ] },
                "predictedImage" : predicted,
                "originalImage" : original,
                "time" : datetime.now(),
            }

        collection.insert(record)

        return 'file was uploaded successfully'
    else:
        return "the uploaded file doesn't seem to have trash in it, if you believe this isn't the case please try again or contact us"
