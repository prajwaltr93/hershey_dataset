#filename : create_globaldataset.py
#author : PRAJWAL T R
#date last modified : Wed Jul  1 11:09:55 2020
#comments :

'''
    python script to create dataset for global model in paper "Teaching Robots to Draw"

    dataset structure :
        dataset : {
            sG_data : [
                [[X_loc],[X_env],[X_last],[X_diff]] ,
                ... ,
                ... ,
            ] ,
            sG_labels : [
                [label_img],
                ... ,
                ... ,
            ]
        }

    //end of structure

    keywords :
        X_loc : current locaion of local model
        X_env : visited region
        X_last: last draw stroke
        X_diff: remaing strokes to draw
    sG : state of global model
'''

from os import walk
import numpy as np
import matplotlib.pyplot as plt
import pickle as pic
import sys
from drawing_utils import *

traverse_path = "./font_svgs/"
global_dataset_path = "./global_dataset/"

#dataset structure
dataset = {
    "sG_data" : [],
    "sG_labels" : []
}

#meta-data structure
metadata = {
    "img_dim" : [HEIGHT, WIDTH],
    "label_dim" : (HEIGHT*WIDTH),
    "total_samples" : 0
}
#helper functions
def plotImages(ind, X_loc_img, X_env_img, X_last_img, X_diff_img):
    fig, axs = plt.subplots(1,4)
    axs[0].imshow(X_loc_img)
    axs[0].set_title("X_loc_img")
    axs[1].imshow(X_env_img)
    axs[1].set_title("X_env_img")
    axs[2].imshow(X_last_img)
    axs[2].set_title("X_last_img")
    axs[3].imshow(X_diff_img)
    axs[3].set_title("X_diff_img")
    plt.savefig("mygraph"+ind+".png")

def pickleDataset(dataset,ind):
    out_path = global_dataset_path+"data_batch_"+str(ind)
    fd = open(out_path,"wb")
    #convert list to numpy array ie : compatiable with tensorflow data adapter
    dataset['sG_data'] = np.array(dataset['sG_data'])
    dataset['sG_labels'] = np.array(dataset['sG_labels'])
    pic.dump(dataset,fd)
    print("dataset created at : ",out_path)
    #clear contents of dataset structure
    dataset['sG_data'] = []
    dataset['sG_labels'] = []

if __name__ == "__main__":
    #get sample rate
    len_sample = 0
    sample_rate = sys.argv[1] if (len(sys.argv) == 2) else 300
    #main loop
    _, _, filelist = next(walk(traverse_path))
    breaks = [i for i in range(0, len(filelist), sample_rate)]
    for break_ind in range(len(breaks) - 1):
        for file in filelist[breaks[break_ind] : breaks[break_ind + 1]]:
            svg_string = open(traverse_path+file).read()
            X_target, m_indices = getStrokesIndices(svg_string)
            #last point of local model
            X_loc = Point()
            #strokes completed by local model
            X_env = []
            #last stroke drawn by local model
            X_last = []
            #remaining strokes to complete
            X_diff = X_target
            #target label
            label = Point()
            label.updatePoint(X_target[0])
            #creating images and labels
            for index, m_index in zip(range(len(m_indices)),m_indices.__iter__()):
                #each function call generates corresponding image
                X_loc_img = drawPoint(X_loc)
                X_env_img = drawStroke(X_env)
                X_last_img = drawStroke(X_last)
                X_diff_img = drawStroke(X_diff)
                X_label_img = drawPoint(label)
                #plotImages(str(index), X_loc_img, X_env_img, X_last_img, X_diff_img)
                #update to dataset
                dataset['sG_data'].append(np.dstack((X_loc_img, X_env_img, X_last_img, X_diff_img)))
                dataset['sG_labels'].append(np.reshape(X_label_img, (HEIGHT * WIDTH)))
                len_sample += 1
                #udpate variables
                if (len(m_indices) == 1) or (index + 1 == len(m_indices)):
                    #X_target has only one stroke
                    continue
                X_loc.updatePoint(X_target[m_indices[index + 1] - 1])
                X_env += X_target[m_indices[index] : m_indices[index + 1]]
                X_last = X_target[m_indices[index] : m_indices[index + 1]]
                X_diff = X_target[m_indices[index + 1]:]
                label.updatePoint(X_target[m_indices[index + 1]])
        pickleDataset(dataset,break_ind)
    metadata["total_samples"] = len_sample
    meta_fd = open(global_dataset_path+"metadata",'wb')
    pic.dump(metadata,meta_fd) #create metadata file
