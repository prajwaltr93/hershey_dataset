#filename : char_to_svg_tool.py
#author : PRAJWAL T R
#date last modified : Thu Sep 24 11:51:27 2020
#comments :


import tkinter as tk

# global variables
items_list = []
final_points_list = []
points_list = []
grid_size = 40
button_size = 10
relief = tk.GROOVE


# helper functions
def undo_action():
    pass

def clear_preview():
    global points_list
    for item in items_list:
        grid_canvas.itemconfig(item, fill='white')
    points_list = []
    preview_canvas.delete('all')


def update_preview():
    global preview_canvas
    if len(points_list) == 1 or len(points_list) == 0:
        return
    else:
        for ind in range(len(points_list) - 1):
            cur_point = points_list[ind]
            next_point = points_list[ind + 1]
            preview_canvas.create_line(cur_point[0] * button_size, cur_point[1] * button_size, next_point[0] * button_size , next_point[1] * button_size, fill="black", width=3)

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
    if len(points_list) == 1:
        return
    final_points_list.append(points_list)
    points_list = []

window = tk.Tk()

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
save_button = tk.Button(master = button_frame, text = 'save')
save_button.pack()
preview_frame.pack(side=tk.LEFT)
grid_frame.pack(side=tk.LEFT)
button_frame.pack(side=tk.LEFT)

window.mainloop()
