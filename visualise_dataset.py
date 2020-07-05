#!/usr/bin/python3
#filename : visualise_dataset.py
#author : PRAJWAL T R
#date last modified : Sun Jul  5 09:22:30 2020
#comments :

import pickle as pic
import matplotlib.pyplot as plt

data = pic.load(open("./global_dataset/data_batch_0","rb"), encoding="bytes")

imgs = data['sG_data'][200:204]

labels = data['sG_labels'][200:204]

for img, label in zip(imgs,labels):

    _, axs = plt.subplots(1,5)
    axs[0].imshow(img[0])
    axs[1].imshow(img[1])
    axs[2].imshow(img[2])
    axs[3].imshow(img[3])
    axs[4].imshow(label)
    axs[0].set_title("X_loc")
    axs[1].set_title("X_env")
    axs[2].set_title("X_last")
    axs[3].set_title("X_diff")
    axs[4].set_title("label")
    plt.show()
