from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
app = Flask(__name__)
MODEL_PATH = 'models/my_model.h5'
model = load_model(MODEL_PATH)
model._make_predict_function()
print('Model loaded. Start serving...')
def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(50,50)) #target_size must agree with what the trained model expects!!

    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    pred = np.argmax(preds,axis = 1)
    return pred
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        #file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        file_path = join(dirname(realpath(__file__)), 'static/uploads/..')
        f.save(file_path)
        pred = model_predict(file_path, model)
        str1 = 'Malaria Parasitized'
        str2 = 'Normal'
        if pred[0] == 0:
            return str1
        else:
            return str2
    return('working')
if __name__ == '__main__':
    app.run()
