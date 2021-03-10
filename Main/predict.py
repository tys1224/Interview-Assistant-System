# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:23:19 2020

@author: swift
"""

import  tensorflow as tf
import numpy as np 
import os
import cv2
import pickle
from PIL import Image
from dan import DAN

os.environ["CUDA_VISIBLE_DEVICES"] = '1'

init_op = tf.initialize_all_variables()
with tf.Session() as sess:
  labels = ["ValueExtraversion","ValueNeuroticism","ValueAgreeableness","ValueConscientiousness","ValueOpenness"]
  sess.run(init_op)
  
  def load_model():
	     # Load graph and parameters, etc.
		 global imgs, output
		 modelpath = 'D:\\Aubrey_file\\Main\\model1'
		 saver = tf.train.import_meta_graph(modelpath + '\\model_full.meta')
		 saver.restore(sess, tf.train.latest_checkpoint(modelpath))
		 graph = tf.get_default_graph()
		 # Get tensor names
		 imgs = graph.get_tensor_by_name("image_placeholder:0")
		 output = graph.get_tensor_by_name("output:0")
		 #print(output)
  
        
  def load_image(addr):
	  img = np.array(Image.open(addr).resize((224,224), Image.ANTIALIAS))
	  img = img.astype(np.uint8)
	  return img
  
  def predict(img):
	  global imgs, prediction
	  feed_dict ={imgs: [img]}
	  prediction = sess.run(output,feed_dict=feed_dict)
	  return prediction
  
  def read_directory(directory_name):
	  global array_of_addr
	  # this loop is for read each image in this foder,directory_name is the foder name with images.
	  array_of_addr = []
	  array_of_img = [] # this if for store all of the image data
	  # this function is for read image,the input is directory name
	  for filename in os.listdir(directory_name):
          #print(filename) #just for test
		  #img is used to store the image data 
		  array_of_addr.append(directory_name + "\\" + filename)
		  #print(img)
		  
  load_model()
  print("finish loading model1!")