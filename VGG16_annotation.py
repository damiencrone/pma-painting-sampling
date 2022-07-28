#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 16:07:32 2021

@author: dcrone

"""

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import os
import json

img_dir = 'img/'
image_list = os.listdir(img_dir)

model = VGG16(weights='imagenet')
fc2_model = Model(inputs=model.input, outputs=model.get_layer('fc2').output)
n = 5

feature_list = []
prediction_list = {}
id_list = []

for fn in image_list:
    
    print('Processing ' + fn)
    img_path = img_dir + fn
    object_id = fn.split('.')[0]
    ext = fn.split('.')[1]
    
    if ext == 'jpg':
        
        id_list.append(object_id)
        img = image.load_img(img_path, target_size=(224, 224))
        
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        full_features = model.predict(x)
        fc2_features = fc2_model.predict(x)
        feature_list.append(fc2_features[0])
        
        top_predictions = decode_predictions(full_features, top=n)
        prediction_list[object_id] = top_predictions[0]


col_names = ['V' + str(i) for i in range(1, 4097)]
df = pd.DataFrame(feature_list, columns=col_names, index=id_list)
df.to_csv('VGG16_annotations.csv')


# Save model predictions after converting tuples to lists
pred_output = prediction_list
for item in pred_output.keys():
    for i in range(n):
        pred_output[item][i] = list(pred_output[item][i])
        pred_output[item][i][2] = str(pred_output[item][i][2])
            
output_filename = 'VGG16_predictions.json'
with open(output_filename, 'w') as f:
    json.dump(pred_output, f)