

def load_model():

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

    return model, dataset.class_names
