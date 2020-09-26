import tkinter as tk
from PIL import Image, ImageTk
from os import walk
# constants
relief = tk.GROOVE
traverse_path = './font_pngs/'
_, _, filelist = next(walk(traverse_path))
filelist = sorted(filelist)
counter = 0
grid_size = 40
button_size = 10
items_list = []
points_list = []
final_points_list = []
WIDTH = 40
HEIGHT = 40
O_X = 20
O_Y = 32
svg_start_line = "<svg xmlns='http://www.w3.org/2000/svg' \nxmlns:xlink='http://www.w3.org/1999/xlink' \n"
m_line = "\tM %s, %s\n"
l_line = "\tL %s, %s\n"

# helper functions
def save_action():
    global points_list, final_points_list, counter
    if len(final_points_list) == 0:
        return
    # open an svg file
    write_fd = open(output_path+str(counter)+".svg","w")
    write_fd.write(svg_start_line)
    write_fd.write(f"viewBox = \'{O_X} {O_Y} {WIDTH} {HEIGHT}\' >\n")
    write_fd.write("<path d = '\n")
    if len(points_list) != 0: # some points not added to final_points_list
        final_points_list.append(points_list)
    for points in final_points_list:
        # M - move command
        write_fd.write(m_line % ((points[0][0] + O_X).__str__(),(points[0][1] + O_Y).__str__()))
        for point in points[0:]:
            write_fd.write(l_line % ((point[0] + O_X).__str__(), (point[1] + O_Y).__str__()))

    write_fd.write("' fill='none' stroke='black' />\n")
    write_fd.write("</svg>")
    write_fd.close()
    counter += 1
    clear_preview()

def clear_preview():
    global points_list
    for item in items_list:
        drawing_canvas.itemconfig(item, fill='')
    points_list = []
    preview_canvas.delete('all')

def update_preview():
    if len(points_list) == 1 or len(points_list) == 0:
        return
    else:
        for ind in range(len(points_list) - 1):
            cur_point = points_list[ind]
            next_point = points_list[ind + 1]
            preview_canvas.create_line(cur_point[0] * button_size, cur_point[1] * button_size, next_point[0] * button_size , next_point[1] * button_size, fill="red", width=3)

def mouse_clicked(event):
    item_tag = event.widget.gettags('current')
    item = event.widget.find_withtag(item_tag[0])
    event.widget.itemconfig(item, fill='blue')
    items_list.append(item)
    #get points
    points = [int(point) for point in item_tag[0].split('*')]
    points_list.append(points)
    print(points_list)
    update_preview()

def mouse_rclicked(event):
    global points_list
    # save stroke
    if len(points_list) == 1:
        return
    final_points_list.append(points_list)
    points_list = []


def prev():
    global counter
    counter -= 1
    image = Image.open("./font_pngs/" + filelist[counter])
    photo = ImageTk.PhotoImage(image)
    drawing_canvas.itemconfigure(image_id, image=photo)
    drawing_canvas.photo = photo

def next():
    global counter
    counter += 1
    image = Image.open("./font_pngs/" + filelist[counter])
    photo = ImageTk.PhotoImage(image)
    drawing_canvas.itemconfigure(image_id, image=photo)
    drawing_canvas.photo = photo

window = tk.Tk()
window.title("character trace tool")
preview_frame = tk.Frame(master = window, width = 400, height = 400, relief=relief, borderwidth=5)
preview_canvas = tk.Canvas(master = preview_frame, width = 400, height = 400, bg="white")
preview_canvas.pack()
preview_frame.pack(side = tk.LEFT)

left_frame = tk.Frame(master = window, relief = relief, height = 400, width = 200, borderwidth = 5)
left_frame.pack(side = tk.LEFT)
left_button = tk.Button(master = left_frame, text = 'prev', command = prev)
left_button.pack()

drawing_frame = tk.Frame(master = window,relief = relief, width = 400, height = 400, borderwidth = 5)
drawing_canvas = tk.Canvas(master = drawing_frame, width = 400, height = 400,  bd=0, highlightthickness=0)
# image = Image.open("./font_pngs/1.png")
photo = ImageTk.PhotoImage(file = "./font_pngs/1.png")
image_id = drawing_canvas.create_image(200, 200, image=photo)

for i in range(grid_size):
    for j in range(grid_size):
        rect = drawing_canvas.create_rectangle(i*button_size,j*button_size,(i + 1) * button_size, (j + 1) * button_size, fill='', activefill = 'green', tags='{}*{}'.format(i,j))
        drawing_canvas.tag_bind(rect, '<ButtonPress-1>', mouse_clicked)
        drawing_canvas.tag_bind(rect, '<ButtonPress-3>', mouse_rclicked)

drawing_canvas.pack()
drawing_frame.pack(side = tk.LEFT)

right_frame = tk.Frame(master = window, relief = relief, height = 400, width = 200, borderwidth = 5)
right_frame.pack(side = tk.LEFT)
right_button = tk.Button(master = right_frame, text = 'next', command = next)
right_button.pack()

button_frame = tk.Frame(master = window, relief = relief, width = 200, height = 400, borderwidth = 5)
button_frame.pack(side = tk.LEFT)
clear_button = tk.Button(master = button_frame, text = 'clear', command = clear_preview)
save_button = tk.Button(master = button_frame, text = 'save', command = save_action)
clear_button.pack()
save_button.pack()

window.mainloop()