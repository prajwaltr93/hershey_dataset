#!/home/starkm42/opencvprjcts/bin/python3

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

import re
from os import walk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pickle as pic

#globals
WIDTH = 60
HEIGHT = 95
COLOR = 1
THICKNESS = 1
LINE_TYPE = cv.LINE_AA
path_re = re.compile(r'\t(.*)\n')
points_re = re.compile(r'(\d+),\s(\d+)')
traverse_path = "./font_svgs/"
global_dataset_path = "./global_dataset/"

#dataset structure
dataset = {
    "sG_data" : [],
    "sG_labels" : []
}
#debug functions
def showImage(img):
    cv.imshow("show window",img)
    cv.imwrite("debug_image_out.png",img)
    cv.waitKey(0)

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
    fd = open(global_dataset_path+"data_batch_"+str(ind),"wb")
    #convert list to numpy array ie : compatiable with tensorflow adapter
    dataset['sG_data'] = np.array(dataset['sG_data'])
    dataset['sG_labels'] = np.array(dataset['sG_labels'])
    pic.dump(dataset,fd)
    #clear contents of dataset structure
    dataset['sG_data'] = []
    dataset['sG_labels'] = []

def parsePointString(point_string):
    #get x and y cordinate out of point_string
    result_points = points_re.search(point_string)
    return (int(result_points.group(1)), int(result_points.group(2)))

def drawPoint(point = None):
    '''
        point : list of x,y
        if point == Nan:
            generate empty image
        else:
            mark point in white color ex : for argmax
            background in black
        returns numpy representation of images
    '''
    img = np.zeros((HEIGHT,WIDTH))
    if point.x == 0 and point.y == 0:
        #generate black background image
        return img
    else:
        #mark white dot
        img[point.y][point.x] = COLOR
    return img

def drawStroke(strokes):
    '''
        stroke
            ex :
                M 34,45
                L 32,32
                L 14,14
        parse stroke and generate corresponding image

        if stroke == Nan
            generate empty image
        returns numpy representation of images
    '''
    img = np.zeros((HEIGHT,WIDTH))
    if len(strokes) == 0:
        #generate empty image
        return img
    #X_last X_env X_diff
    m_indices = []
    for search_ind, path in zip(range(len(strokes)), strokes.__iter__()):
        if path[0] == 'M':
            m_indices.append(search_ind)
    for ind in range(len(m_indices) - 1):
        slice = strokes[m_indices[ind] : m_indices[ind + 1]]
        for ind in range(len(slice) - 1):
            cv.line(img,parsePointString(slice[ind]),parsePointString(slice[ind+1]),COLOR,THICKNESS,LINE_TYPE)
    #for length of m_indices = 1 and drawing end strokes
    slice = strokes[m_indices[-1] : ]
    for ind in range(len(slice) - 1):
        cv.line(img,parsePointString(slice[ind]),parsePointString(slice[ind+1]),COLOR,THICKNESS,LINE_TYPE)
    return img

def getStrokesIndices(svg_string):
    #get path string
    X_target = path_re.findall(svg_string)
    m_indices = []
    for search_ind, path in zip(range(len(X_target)),X_target.__iter__()):
        if path[0] == 'M':
            m_indices.append(search_ind)
    return X_target, m_indices

#point class
class Point:
    '''
    class to represent simple point
    '''
    def __init__(self, x = None, y = None):
        if x == None and y ==  None:
            self.x = 0
            self.y = 0
        else:
            self.x = x
            self.y = y

    def updatePoint(self, point_string):
        #update X_loc
        points = parsePointString(point_string)
        self.x = points[0]
        self.y = points[1]
    def __str__(self):
        return "X : {} Y : {}\n".format(self.x, self.y)
    def __to_ndarray__():
        return np.array([self.x, self.y])

if __name__ == "__main__":
    #main loop
    thresh = 0
    breaks = [0, 300, 600, 900, 1200, 1569]
    for break_ind in range(len(breaks) - 1):
        for _, _, filelist in walk(traverse_path):
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
                    dataset['sG_labels'].append(np.reshape(X_label_img,(1,(HEIGHT * WIDTH))))
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
        break
