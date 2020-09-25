#filename : char_to_svg_tool.py
#author : PRAJWAL T R
#date last modified : Thu Sep 24 11:51:27 2020
#comments :

'''
    simple tkinter application to create character in svg format to further get dataset out of it
    this is created due to short supply of characters (hershey has only 2000, other 10000 required).
    created characters will be uploaded to font_svgs.zip.
'''

output_path =  "./test_dir/test_out_svg/"

import tkinter as tk

# global variables
svg_start_line = "<svg xmlns='http://www.w3.org/2000/svg' \nxmlns:xlink='http://www.w3.org/1999/xlink' \n"
m_line = "\tM %s, %s\n"
l_line = "\tL %s, %s\n"
counter = 0
items_list = []
line_list = []
final_points_list = []
points_list = []
grid_size = 40
button_size = 10
relief = tk.GROOVE
WIDTH = 40
HEIGHT = 40
O_X = 20
O_Y = 32

# helper functions
def save_action():
    global points_list, final_points_list, counter
    # open an svg file
    write_fd = open(output_path+str(counter)+".svg","w")
    write_fd.write(svg_start_line)
    write_fd.write(f"viewBox = \'{0} {0} {WIDTH} {HEIGHT}\' >\n")
    write_fd.write("<path d = '\n")
    if len(points_list) != 0: # some points not added to final_points_list
        final_points_list.append(points_list)
    for points in final_points_list:
        # M - move command
        write_fd.write(m_line % (points[0][0], points[0][1]))
        for point in points[0:]:
            write_fd.write(l_line % (point[0], point[1]))

    write_fd.write("' fill='none' stroke='black' />\n")
    write_fd.write("</svg>")
    write_fd.close()
    counter += 1
    clear_preview()

def undo_action():
    # TODO : Implement undo if nessesary
    pass
    # global points_list
    # if len(points_list) != 0:
    #     points_list.pop()
    #     grid_canvas.itemconfig(items_list[-1], fill='white')
    #     items_list.pop()
    # elif len(final_points_list) != 0:
    #     final_points_list.pop()
    #     # erase last line
    #     preview_canvas.delete(line_list[-1])
    #     line_list.pop()

def clear_preview():
    # clear preview and grid canvas
    global points_list
    global items_list
    for item in items_list:
        grid_canvas.itemconfig(item, fill='white')
    points_list = []
    items_list = []
    preview_canvas.delete('all')


def update_preview():
    # update preview for selected lines
    global line_list
    if len(points_list) == 1 or len(points_list) == 0:
        return
    else:
        for ind in range(len(points_list) - 1):
            cur_point = points_list[ind]
            next_point = points_list[ind + 1]
            line = preview_canvas.create_line(cur_point[0] * button_size, cur_point[1] * button_size, next_point[0] * button_size , next_point[1] * button_size, fill="black", width=3)
            line_list.append(line)

# callbacks
def mouse_clicked(event):
    item_tag = event.widget.gettags('current')
    item = event.widget.find_withtag(item_tag[0])
    event.widget.itemconfig(item, fill='blue')
    items_list.append(item)
    #get points
    points = [int(point) for point in item_tag[0].split('*')]
    points_list.append(points)
    update_preview()

def mouse_rclicked(event):
    global points_list
    # save stroke
    if len(points_list) == 1 or len(points_list) == 0: # ensure atleast two points exists
        return
    final_points_list.append(points_list)
    points_list = []

window = tk.Tk()
window.title("character creating tool")

# preview frame
preview_frame = tk.Frame(master = window, width = 400, height = 400, relief=relief, borderwidth=5)
preview_canvas = tk.Canvas(master = preview_frame, width = 400, height = 400, bg="white")
preview_canvas.pack()

# grid frame
grid_frame = tk.Frame(master = window, width = 400, height = 400, relief=relief, borderwidth=5)
grid_canvas = tk.Canvas(master = grid_frame, width = 400, height = 400)

for i in range(grid_size):
    for j in range(grid_size):
        rect = grid_canvas.create_rectangle(i*button_size,j*button_size,(i + 1) * button_size, (j + 1) * button_size, fill='white', activefill='black', tags='{}*{}'.format(i,j))
        grid_canvas.tag_bind(rect, '<ButtonPress-1>', mouse_clicked)
        grid_canvas.tag_bind(rect, '<ButtonPress-3>', mouse_rclicked)

grid_canvas.pack()
# button frame
button_frame = tk.Frame(master = window, width = 200, height = 400,relief=relief, borderwidth=5)
undo_button = tk.Button(master = button_frame, text = 'undo',command = undo_action)
undo_button.pack()
# redo_button = tk.Button(master = button_frame, text = 'redo')
# redo_button.pack()
clear_button = tk.Button(master = button_frame, text = 'clear', command = clear_preview)
clear_button.pack()
save_button = tk.Button(master = button_frame, text = 'save', command = save_action)
save_button.pack()
preview_frame.pack(side=tk.LEFT)
grid_frame.pack(side=tk.LEFT)
button_frame.pack(side=tk.LEFT)

window.mainloop()
