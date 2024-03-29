from flask import Blueprint, render_template, request
import pickle
import numpy as np
import os
from skimage.io import imread
from skimage.transform import resize

views = Blueprint('views',__name__)

model_path = os.path.join(os.path.dirname(__file__), '..', 'model.p')
model = pickle.load(open(model_path, 'rb'))

# model = pickle.load(open('model.p','rb'))
categories = ['flea', 'mosquito', 'tick']

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/identifybite', methods=['GET', 'POST'])
def identify():
    if request.method =='POST':
        try:
            url=request.form['image_url']
            img=imread(url)
            img=resize(img, (30,30,3))
            flat_data=[img.flatten()]
            flat_data=np.array(flat_data)
            y_out=model.predict(flat_data)
            category=categories[y_out[0]]
            return render_template("identify.html", prediction=category, image_url=url)
        except Exception as e:
            return render_template('identify.html', error=str(e))
    else:
        return render_template('identify.html')

@views.route('/infobug')
def photo_gallery():
    return render_template("photo_gallery.html") 

@views.route('/personality_quiz')
def personality_quiz():
    return render_template("personality_quiz.html")