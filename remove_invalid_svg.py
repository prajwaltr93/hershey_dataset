#!/usr/bin/python3
#filename : svg_to_png.py
#author : Prajwal T R
#date last modified : Mon Jun 29 08:16:17 2020
#comments :

'''
    remove invalid(empty) svg files in font_svgs/
'''

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from os import walk,remove

#paths
traverse_path = "./font_svgs/"
invalid_files = []
original_file_count = 0
#traverse and save files as PNG
for _,_,filelist in walk(traverse_path):
    original_file_count = len(filelist)
    for file in filelist:
        try:
            drawing = svg2rlg(traverse_path+file)
        except:
            print("invalid file : "+file)
            invalid_files.append(file)
            continue

#remove invalid svg files

for file in invalid_files:
    try:
        remove(traverse_path+file)
    except:
        print(traverse_path+file," not found !")

#print summary

print("original_file_count : ",original_file_count," files lost : ",len(invalid_files)," remaining files : ",original_file_count - len(invalid_files))
