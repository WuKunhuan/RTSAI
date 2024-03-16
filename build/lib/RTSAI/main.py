

import tkinter, sys, time
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk

from RTSAI.config import PACKAGE_NAME, EXECUTABLE_PATH, PACKAGE_PATH
from RTSAI.config import COMMAND_NAME, WINDOW_NAME
from RTSAI.config import DESKTOP_SIZE

debug = 1
ID_counter = 0
def new_ID(): 
    global ID_counter; ID_counter += 1
    return ID_counter

window = None
window_width = 800; window_height = 600; 
window_width_max = DESKTOP_SIZE[0]; window_height_max = DESKTOP_SIZE[1]; 
window_width_min = 600; window_height_min = 450; 

left_panel = None
left_panel_relwidth = 0.3; 
left_panel_relwidth_max = 0.4; left_panel_relwidth_min = 0.2; 
left_panel_color = (38, 38, 38)

left_panel_change_arrow = None
left_panel_change_arrow_width = 25; left_panel_change_arrow_height = 25; 

right_panel = None
right_panel_color = (30, 30, 30)

default_grey_color = (64, 64, 64)
VSCode_highlight_color = (47, 108, 187)

def color_tuple_to_rgb(color_tuple): 
    return ("#%02x%02x%02x" % color_tuple)

def resize_window(): 
    global window_width, window_height, left_panel_relwidth
    global left_panel, left_panel_change_arrow
    window_geometry = list(map(int, window.geometry().replace('x', ' ').replace('+', ' ').split(' ')))
    window_width = window_geometry[0]
    window_height = window_geometry[1]
    left_panel_width = int(left_panel_relwidth * window_width)
    left_panel.configure (width = left_panel_width, height = window_height)
    right_panel.configure (height = window_height)
    left_panel_change_arrow.place(x = left_panel_width, y = window_height, anchor = tkinter.SE)

def create_left_panel():
    global window, left_panel, left_panel_change_arrow
    left_panel = tkinter.Frame(window, bg = color_tuple_to_rgb(left_panel_color))
    left_panel.pack(side='left', fill='y')

    left_panel_change_arrow = tk.Canvas(left_panel, width=25, height=25, bg = color_tuple_to_rgb(left_panel_color), highlightthickness=0, relief='ridge')
    left_panel_width = int(left_panel_relwidth * window_width)
    left_panel_change_arrow.place(x = left_panel_width, y = window_height, anchor = tkinter.SE)

    def configure_canvas(event):
        canvas_width = left_panel_change_arrow.winfo_width()
        canvas_height = left_panel_change_arrow.winfo_height()
        left_panel_change_arrow.delete("arrow")
        left_panel_change_arrow.config(width=canvas_width, height=canvas_height)

        arrow_coords = [
            canvas_width * 0.9, canvas_height * 0.5,
            canvas_width * 0.5, canvas_height * 0.25,
            canvas_width * 0.5, canvas_height * 0.375,
            canvas_width * 0.1, canvas_height * 0.375,
            canvas_width * 0.1, canvas_height * 0.625,
            canvas_width * 0.5, canvas_height * 0.625,
            canvas_width * 0.5, canvas_height * 0.75
        ]
        left_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(default_grey_color), tags="arrow")
        window_height = window.winfo_height()
        left_panel_change_arrow.place(x=left_panel_width, y=window_height, anchor=tkinter.SE)
    
    def resize_canvas(event): 
        global left_panel_relwidth
        left_panel_relwidth += 0.05
        if (left_panel_relwidth > left_panel_relwidth_max): 
            left_panel_relwidth = left_panel_relwidth_max
        left_panel_width = int(left_panel_relwidth * window_width)
        left_panel.configure(width = left_panel_width)

    def change_arrow_color(event):
        left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(VSCode_highlight_color))

    def reset_arrow_color(event):
        left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(default_grey_color))

    left_panel_change_arrow.bind("<Enter>", change_arrow_color)
    left_panel_change_arrow.bind("<Leave>", reset_arrow_color)
    left_panel_change_arrow.bind("<Configure>", configure_canvas)
    left_panel_change_arrow.bind("<Button-1>", resize_canvas)

    return left_panel

def create_right_panel():
    global window, right_panel, right_panel_change_arrow
    right_panel = tk.Frame(window, bg=color_tuple_to_rgb(right_panel_color))
    right_panel.pack(side='left', fill='both', expand=True)

    right_panel_change_arrow = tk.Canvas(right_panel, width=25, height=25, bg=color_tuple_to_rgb(right_panel_color), highlightthickness=0, relief='ridge')
    right_panel_change_arrow.place(x=0, y=window_height, anchor=tk.SW)

    def configure_canvas(event):
        canvas_width = right_panel_change_arrow.winfo_width()
        canvas_height = right_panel_change_arrow.winfo_height()

        right_panel_change_arrow.delete("arrow")
        right_panel_change_arrow.config(width=canvas_width, height=canvas_height)

        arrow_coords = [
            canvas_width * 0.1, canvas_height * 0.5,
            canvas_width * 0.5, canvas_height * 0.25,
            canvas_width * 0.5, canvas_height * 0.375,
            canvas_width * 0.9, canvas_height * 0.375,
            canvas_width * 0.9, canvas_height * 0.625,
            canvas_width * 0.5, canvas_height * 0.625,
            canvas_width * 0.5, canvas_height * 0.75
        ]
        right_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(default_grey_color), tags="arrow")
        window_height = window.winfo_height()
        right_panel_change_arrow.place(x=0, y=window_height, anchor=tkinter.SW)

    def resize_canvas(event): 
        global left_panel_relwidth
        left_panel_relwidth -= 0.05
        if (left_panel_relwidth < left_panel_relwidth_min): 
            left_panel_relwidth = left_panel_relwidth_min
        left_panel_width = int(left_panel_relwidth * window_width)
        left_panel.configure(width = left_panel_width)

    def change_arrow_color(event):
        right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(VSCode_highlight_color))

    def reset_arrow_color(event):
        right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(default_grey_color))

    right_panel_change_arrow.bind("<Enter>", change_arrow_color)
    right_panel_change_arrow.bind("<Leave>", reset_arrow_color)
    right_panel_change_arrow.bind("<Configure>", configure_canvas)
    right_panel_change_arrow.bind("<Button-1>", resize_canvas)

    return right_panel

def create_window_component(): 
    '''
    Create the left and right panels
    '''
    global left_panel, right_panel, left_panel_change_arrow
    global window_width, window_height, left_panel_relwidth
    global left_panel_change_arrow_width, left_panel_change_arrow_height
    left_panel = create_left_panel()
    left_panel_width = int(left_panel_relwidth * window_width)
    left_panel.configure(width = left_panel_width)
    right_panel = create_right_panel()

def main(): 

    if (len(sys.argv) == 1 and sys.argv[0] == f'{EXECUTABLE_PATH}/{COMMAND_NAME}'): 

        print (f"{PACKAGE_NAME}: Hello World! ")

        '''
        Create the RTSAI Window
        '''
        global window; 
        window = tkinter.Tk()
        window.title("RTSAI")

        if (debug == 0): print (f"sys.platform: {sys.platform}")
        if (sys.platform.startswith("darwin")): window.iconphoto(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png")))
        else: window.iconbitmap(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png"))) # to be tested

        global window_width, window_height
        window.geometry(f"{window_width}x{window_height}")
        window.bind("<Configure>", lambda event: resize_window())
        window.maxsize(window_width_max, window_height_max)
        window.minsize(window_width_min, window_height_min)

        '''
        Create the window components
        '''
        create_window_component()

        '''
        Load user data
        '''

        window.mainloop()

if __name__ == '__main__': 
    main()

