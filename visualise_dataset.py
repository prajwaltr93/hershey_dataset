#!/usr/bin/python3
#filename : visualise_dataset.py
#author : PRAJWAL T R
#date last modified : Sun Jul  5 09:22:30 2020
#comments :

import pickle as pic
import matplotlib.pyplot as plt
import numpy as np

data = pic.load(open("./global_dataset/data_batch_1","rb"), encoding="bytes")

imgs = data['sG_data'][1:4]

labels = data['sG_labels'][1:4]

img_height = 95
img_width = 65

print("image shape : ",np.shape(imgs[0]))
print("label shape : ",np.shape(labels[0]))
for img, label in zip(imgs,labels):
    #get label image
    label = np.reshape(label,(img_height,img_width))
    img = np.transpose(img,(2,0,1))
    _, axs = plt.subplots(1,5)
    axs[0].imshow(img[0],cmap="Greys_r")
    axs[1].imshow(img[1],cmap="Greys_r")
    axs[2].imshow(img[2],cmap="Greys_r")
    axs[3].imshow(img[3],cmap="Greys_r")
    axs[4].imshow(label,cmap="Greys_r")
    axs[0].set_title("X_loc")
    axs[1].set_title("X_env")
    axs[2].set_title("X_last")
    axs[3].set_title("X_diff")
    axs[4].set_title("label")
    plt.show()
