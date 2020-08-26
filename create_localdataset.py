#filename : create_localdataset.py
#author : PRAJWAL T R
#date last modified : Mon Jul 13 14:25:12 2020
#comments :

'''
    python script to create dataset for local model in paper "Teaching Robots to Draw"

    dataset structure :
        dataset : {
            lG_data : [
                [[X_env],[X_con],[X_diff]] ,
                ... ,
                ... ,
            ] ,
            lG_labels : [
                [dx, dy],
                ... ,
                ... ,
            ]
            lG_extract : [
                [begin, size],
                ... ,
                ... ,
            ]
            lG_touch : [
                [touch],
                ... ,
                ... ,
            ]
        }

    //end of structure

    keywords :
        X_env : visited region
        X_con: continoulsy connected stroke
        X_diff: remaining strokes to draw
    lG : state of local model
'''

from drawing_utils import *
from os import walk

traverse_path = "./font_svgs/"
global_dataset_path = "./local_dataset/"
sample_rate = 300
_, _, filelist = next(walk(traverse_path))

breaks = [i for i in range(0, len(filelist), sample_rate)]

for break_ind in range(len(breaks) - 1):
    for file in filelist[breaks[break_ind] : breaks[break_ind + 1]]:
        svg_string = open(traverse_path+file).read()
        X_target, m_indices = getStrokesIndices(svg_string)
        #loop through all strokes
        for index in range(len(m_indices) - 1):
            #get current stroke
            stroke = X_target[m_indices[index] : m_indices[index + 1]]

            #all points for given stroke ML,MLL,MLLLL
            points = getAllPoints(stroke)
            env_l = []
            diff_l = points
            touch = 1
            con_img = drawStroke(stroke)
            print(stroke)
            print(points)
            for ind in range(len(points) - 1):
                env_img = drawFromPoints(env_l)
                diff_img = drawFromPoints(diff_l)
                target = pointDiff(points[ind], points[ind + 1]) #return dx, dy
                current_xy = points[ind]
                # TODO : update data structure
                #con_img
                print("env_l : ", env_l)
                print("diff_l : ", diff_l)
                print("target : ", target)
                print("current_xy : ", current_xy)
                print("touch : ", touch)
                #update env,diff
                env_l = points[0 : ind + 2] # add two points for one complete stroke
                diff_l = points[ind + 1 :]

            #update last instance
            #con_img
            touch = 0
            env_l = points
            diff_l = []
            target = pointDiff(points[-2], points[-1])
            current_xy = points[-1]
            # TODO : update data structure
            print("env_l  : ", env_l)
            print("diff_l : ", diff_l)
            print("target : ", target)
            print("current_xy : ", current_xy)
            print("touch : ", touch)
            exit(0)
