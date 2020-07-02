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
points_re = re.compile(r'(\d+),\s(\d+)')
traverse_path = "./font_svgs/"

def parsePointString(point_string):
    #get x and y cordinate out of point_string
    result_points = path_re.search(point_string)
    return int(result_points.group[1]), int(result_points.grop[2])

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

def getStrokesIndices(svg_string):
    #get path string
    paths = path_re.findall(svg_string)
    m_indices = []
    print(paths)
    for search_ind, path in zip(range(len(paths)),paths.__iter__()):
        if path[0] == 'M':
            m_indices.append(search_ind)
    return m_indices

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
        self.x, self.y =  parsePointString(point_string)

if __name__ == "__main__":
    thresh = 0
    #main loop
    for _, _, filelist in walk(traverse_path):
        for file in filelist:
            if thresh == 2:
                break
            svg_string = open(traverse_path+file,"r").read()
            m_indices = getStrokesIndices(svg_string)
            print(file)
            print(m_indices)
            thresh += 1
