#!/usr/bin/python3

#filename : create_globaldataset.py
#author : PRAJWAL T R
#date last modified : Wed Jul  1 11:09:55 2020
#comments :

'''
    python script to create dataset for global model in paper "Teaching Robots to Draw"

    dataset structure :
        dataset : {
            sG_data : {
                [[X_loc],[X_env],[X_last],[X_diff]] ,
                ... ,
                ... ,
            } ,
            sG_labels : {
                [x, y],
                ... ,
                ... ,
            }

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

#globals
path_re = re.compile(r'\t(.*)\n')

traverse_path = "./font_svgs/"

#point class

class point:
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

def drawPoint(point):
    '''
        point : list of x,y
        if point == Nan:
            generate empty image
        else:
            mark point in white color ex : for argmax
            background in black
    '''
    pass

def drawStroke(stroke):
    '''
        stroke
            ex :
                M 34,45
                L 32,32
                L 14,14
        parse stroke and generate corresponding image

        if stroke == Nan
            generate empty image
    '''
    pass

def updateStroke(flag, path_remaining):
    '''
        flags :
        1 - update stroke complete
        2 - udpate prev_stroke
        3 - update remaining stroke

    '''
    pass

def getStrokes(stroke_string):
    #get path string
    paths = path_re.findall(stroke_string)
    processed_paths = []
    for path in paths:


if __name__ == "__main__":

    #main loop
    for _, _, filelist in walk(traver_path):
        for file in filelist:
            svg_string = open(traverse_path+file,"r").read()
            paths = getStrokes(svg_string)
            print(svg_string)
            print(file)
            print(paths)
            break
