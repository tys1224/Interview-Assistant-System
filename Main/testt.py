# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:52:22 2020

@author: swift
"""

import tensorflow as tf
import keras
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import pandas as pd
import numpy as np
import os.path
import cv2
from keras_vggface import utils
from keras.engine import  Model
from keras_vggface.vggface import VGGFace
import os
import os.path
os.environ["CUDA_VISIBLE_DEVICES"] = '1'

def extract_metadata(input_lie_path):
    '''
        Extract and write metadata from images dataset to dataframe

        parameters:
            input_path: directory path to Images directory
            output_path: directory path to output directory
        
    '''
    
    df = pd.DataFrame(columns=['path'])
    
    for  file in os.listdir(input_lie_path):
        df = df.append(pd.Series([file],index=['path']), ignore_index=True)
    return df
    
    
def features_extractor(X, feature_model):
    """
     Part 1 of the face recognition pipeline extract 1st F layer from VGGFace 
    

    input : X 4D tensors (m,150,150,3)
    output: features matrix (m,4096)
    """
    # preprocess 
    X = X.astype(np.float64)/255.
    
    # Layer Features
    vgg_model_new = feature_model
    X_features = vgg_model_new.predict(X)
    
    X_features = X_features /np.linalg.norm(X_features,axis =1, keepdims=True)
    return X_features
    
    
def to_tensors(df):

    """
        convert images in path columns to numpy 4D tensors
    """
    X = df.path.apply(lambda path: cv2.imread(path))
    X = np.stack(X, axis = 0)
    return X

model = keras.models.load_model('my_model1.h5')
print("finish loading model2!")