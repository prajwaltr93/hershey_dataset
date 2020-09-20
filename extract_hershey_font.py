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
#constants and magic numbers
R = ord('R')
min_x = -40
min_y = -50
WIDTH = 40
HEIGHT = 40
O_X = 20
O_Y = 32
svg_start_line = "<svg xmlns='http://www.w3.org/2000/svg' \nxmlns:xlink='http://www.w3.org/1999/xlink' \n"
m_line = "\tM %s, %s\n"
l_line = "\tL %s, %s\n"

#helper functions
def ord_string(parse_res):
    # print(parse_res)
    return (ord(parse_res[0]) - R - min_x), (ord(parse_res[1]) - R - min_y)

def parse_command(fd, flag, command):
    parse_pointer = 0
    if command[-1] == '\n':
        command = command[:len(command)]
    if flag:
        parse_pointer += 1

    #process R or start drawing ex M x,y
    parse_res = command[parse_pointer:parse_pointer+2]
    fd.write(m_line % ord_string(parse_res))
    # print(m_line % ord_string(parse_res))
    parse_pointer += 2

    #recursively extract command
    for i in range(int(len(command[parse_pointer:])/2)):
        if parse_pointer+2 == len(command):
            #reached end of command
            parse_res = command[parse_pointer:]
        else:
            parse_res = command[parse_pointer:parse_pointer+2]

        fd.write(l_line % ord_string(parse_res))
        # print(l_line % ord_string(parse_res))
        parse_pointer += 2

def get_fonts(fd):
    for raw_line in fd:

        ## print(f"ascii {raw_line[:6]} vertices {raw_line[6:8]} rest {raw_line[8:]}")
        line_number = int(raw_line[:6].strip())
        vertices = int(raw_line[6:8].strip())
        command_string = raw_line[8:]
        commands = command_string.split(" ")
        # print(line_number,vertices,command_string,commands)

        #prepare file
        write_fd = open("./font_svgs/"+str(line_number)+".svg","w")
        write_fd.write(svg_start_line) #write first line

        #get metrics
        left_line = ord(commands[0][0])
        right_line = ord(commands[0][1])
        width = right_line - left_line
        # print(left_line,right_line,width)
        write_fd.write(f"viewBox = \'{O_X} {O_Y} {WIDTH} {HEIGHT}\' >\n")
        write_fd.write("<path d = '\n")
        # print(width,left_line,right_line)
        #remove characters containing metrics
        commands[0] = commands[0][2:]

        if len(commands[0]) != 1:
            #get vertices
            for command in commands:
                if command[0] == 'R' and commands.index(command) != 0:
                    parse_command(write_fd, True, command)
                else:
                    parse_command(write_fd, False, command)
                write_fd.write("\n")
        write_fd.write("' fill='none' stroke='black' />\n")
        write_fd.write("</svg>")
        write_fd.close()

if __name__ == "__main__":
    from sys import argv
    # just simple validations to check if users wants minimal fonts coverage ex : english alphabets or japanese characters too
    if len(argv) == 2:
        files = ['hershey.jhf']
    else:
        files = ['japanese_hershey.jhf', 'hershey.jhf']
    for file in files:
        get_fonts(open(file,'r'))
