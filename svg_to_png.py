#!/usr/bin/python3
#filename : svg_to_png.py
#author : Prajwal T R
#date last modified : Mon Jun 29 08:16:17 2020
#comments :

'''
    convert svg in font_svgs/ to png's and check co-ordinate system by plotting using opencv
'''

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("./font_svgs/1.svg")
renderPM.drawToFile(drawing, "./font_pngs/1.png", fmt="PNG")
