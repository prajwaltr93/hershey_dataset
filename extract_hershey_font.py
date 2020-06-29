#!/usr/bin/python3

#filename : extract_hershey_font.py
#author : Prajwal T R
#date last modified : Thu Jun 11 09:29:03 2020
#comments :

'''
    extract_hershey_font.py uses hershey.jhf file to create svg dataset of english characters
    this dataset is used to train nueral network to make machines learn to draw and write
    , based on reasearch paper by Brown University. In Paper they use data set of japanese characters
    which is then generalised to english and other languages. this dataset is created to be used for training purposes.
    feel free to use and report any issues
'''
#constants
R = ord('R')
padding = 1
left_line = 0
svg_start_line = "<svg xmlns='http://www.w3.org/2000/svg' \nxmlns:xlink='http://www.w3.org/1999/xlink' \n"
m_line = "\tM %s, %s\n"
l_line = "\tL %s, %s\n"

#helper functions
def ord_string(parse_res):
    #print(parse_res)
    return ord(parse_res[0]) - left_line, ord(parse_res[1]) - left_line + padding

def parse_command(flag,command):
    parse_pointer = 0
    if command[-1] == '\n':
        command = command[:len(command)]
    if flag:
        parse_pointer += 1

    #process R or start drawing ex M x,y
    parse_res = command[parse_pointer:parse_pointer+2]
    fd.write(m_line % ord_string(parse_res))
    print(m_line % ord_string(parse_res))
    parse_pointer += 2

    #recursively extract command
    for i in range(int(len(command[parse_pointer:])/2)):
        if parse_pointer+2 == len(command):
            #reached end of command
            parse_res = command[parse_pointer:]
        else:
            parse_res = command[parse_pointer:parse_pointer+2]

        fd.write(l_line % ord_string(parse_res))
        print(l_line % ord_string(parse_res))
        parse_pointer += 2

thresh = 0
fd = open("hershey.jhf","r")

for raw_line in fd:

    if thresh == 1:
        break

    #print(f"ascii {raw_line[:6]} vertices {raw_line[6:8]} rest {raw_line[8:]}")
    line_number = int(raw_line[:6].strip())
    vertices = int(raw_line[6:8].strip())
    command_string = raw_line[8:]
    commands = command_string.split(" ")
    #print(line_number,vertices,command_string,commands)

    #prepare file
    fd = open("./font_svgs/"+str(line_number)+".svg","w")
    fd.write(svg_start_line) #write first line

    #get metrics
    left_line = ord(commands[0][0])
    right_line = ord(commands[0][1])
    width = right_line - left_line
    print(left_line,right_line,width)
    fd.write(f"viewBox = \'{0} {0} {width} {width + padding}\' >\n")
    fd.write("<path d = '\n")
    #print(width,left_line,right_line)
    #remove characters containing metrics
    commands[0] = commands[0][2:]

    if len(commands[0]) != 1:
        #get vertices
        for command in commands:
            if command[0] == 'R' and commands.index(command) != 0:
                parse_command(True,command)
            else:
                parse_command(False,command)
            fd.write("\n")
    fd.write("' fill='none' stroke='black' />\n")
    fd.write("</svg>")
    fd.close()
    thresh += 1
