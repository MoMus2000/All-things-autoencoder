# -*- coding: utf-8 -*-
"""ConvAutoEncoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cIv7lSkU0N65l6aD87E9SbCGp73Oyhbh
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,Reshape,Dense,MaxPooling2D,Conv2DTranspose,UpSampling2D
from tensorflow.keras.optimizers import SGD

(X_train,y_train),(X_test,y_test) = mnist.load_data()
X_train = X_train/255.0
X_test = X_test/255.0

X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1)
print(X_train.shape)

# encoder = Sequential()
# encoder.add(Conv2D(64,(3,3),input_shape=(28,28,1),padding='same'))
# encoder.add(MaxPooling2D((2,2)))
# encoder.add(Conv2D(32,(3,3),padding='same'))
# encoder.add(MaxPooling2D((2,2)))
# encoder.add(Conv2D(16,(3,3),padding='same'))
# encoder.add(MaxPooling2D((2,2)))
# encoder.summary()

# decoder = Sequential()
# # decoder.add()

enc = Sequential()
enc.add( Conv2D(16, (3, 3), activation='relu', padding='same',input_shape=(28,28,1)))
enc.add(MaxPooling2D((2, 2), padding='same'))
enc.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
enc.add(MaxPooling2D((2, 2), padding='same'))
enc.add(Conv2D(8, (3, 3), activation='relu', padding='same',name='MUSAFA'))
enc.add(MaxPooling2D((2, 2), padding='same'))
enc.add(Reshape([128],name='MUSTAFA'))
enc.summary()

dec = Sequential()
dec.add(Reshape((4,4,8),input_shape = [128]))
dec.add(Conv2D(8, (3, 3), activation='relu', padding='same',input_shape = (4,4,8)))
dec.add(UpSampling2D((2, 2)))
dec.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
dec.add(UpSampling2D((2, 2)))
dec.add(Conv2D(16, (3, 3), activation='relu'))
dec.add(UpSampling2D((2, 2)))
dec.add(Conv2D(1, (3, 3), activation='sigmoid', padding='same'))
dec.summary()

encoder = Sequential([enc,dec])
encoder.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=0.001))

encoder.fit(X_train,X_train,epochs=20,validation_data=(X_test,X_test))

!pip install bokeh

from tensorflow.keras import Model
layer_name = 'MUSTAFA'
intermediate_layer_model = Model(inputs=enc.input,outputs=enc.get_layer(layer_name).output)

intermediate_output = intermediate_layer_model.predict(X_test)
print(intermediate_output.shape)

import bokeh.plotting as bp
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_notebook

from sklearn.manifold import TSNE
tsne_model = TSNE(n_components=2, verbose=1, random_state=0)
tsne_img_label = tsne_model.fit_transform(intermediate_output)

import pandas as pd
import numpy as np
tsne_df = pd.DataFrame(tsne_img_label, columns=['x', 'y'])
tsne_df['image_label'] = y_test

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
cmap = plt.cm.get_cmap('jet')
plt.scatter(tsne_df['x'], tsne_df['y'], 
            alpha=0.5, c=y_test, cmap=cmap, s=5)
plt.colorbar()

