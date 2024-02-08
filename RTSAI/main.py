

import tkinter, sys, time
from datetime import datetime
from PIL import Image, ImageTk

from RTSAI.config import PACKAGE_NAME, EXECUTABLE_PATH, PACKAGE_PATH, COMMAND_NAME

ID_counter = 0
def new_ID(): 
    global ID_counter; ID_counter += 1
    return ID_counter

debug = 1

window_width = 800
window_height = 600
window_left_width = 200

left_panel_color = (38, 38, 38)
right_panel_color = (30, 30, 30)

boundary_color_original = (0, 0, 0)
boundary_color_hover = (52, 120, 198)
boundary_appear_delay = (500, 2000)
boundary_thickness = 4

class RTSAI_Boundary_Direction_Exception: pass

def color_tuple_to_rgb(color_tuple): 
    if (debug == 0): print (f"color_tuple: {color_tuple}")
    return ("#%02x%02x%02x" % color_tuple)

def window_geometry(window): 
    geometry_list = window.geometry().replace('x', ',').replace('+', ',').split(',')
    geometry_list = list(map(int, geometry_list))
    window.width = geometry_list[0]; window.height = geometry_list[1]; 
    window.x = geometry_list[2]; window.y = geometry_list[3]; 
def widget_get_coordinate(widget): 
    if (debug == 0): print(f"{widget.name}'s coordinate: {(widget.x, widget.y)}")
    return ((widget.x, widget.y))
def widget_get_dimension(widget):
    if (debug == 0): print(f"{widget.name}'s dimension: {(widget.width, widget.height)}")
    return ((widget.width, widget.height))
def widget_get_relative_position(root, widget): 
    root_x, root_y = widget_get_coordinate(root)
    widget_x, widget_y = widget_get_coordinate(widget)
    return ((widget_x - root_x, widget_y - root_y))
def widget_configure(self): 
    self.configure(width = self.width, height = self.height)
def widget_place(self): 
    self.place(x = self.x, y = self.y)
def event_get_relative_coordinate(event, master): 
    return ((event.x_root - master.x, event.y_root - master.y))

class RTSAI_Boundary(tkinter.Frame): 

    def __init__(self, master, parent_1, parent_2, name = f"Widget {new_ID()}", direction = 'x', **options): 
        tkinter.Frame.__init__(self, master, **options)
        self.master = master; 
        self.parent_1 = parent_1; self.parent_2 = parent_2; 
        self.name = name; self.direction = direction
        if (self.direction == 'x'): 
            assert (self.parent_1.y == self.parent_2.y and 
                    self.parent_1.height == self.parent_2.height)
            self.x = self.parent_1.x + self.parent_1.width; 
            self.y = self.parent_1.y; 
            self.width = boundary_thickness; 
            self.height = self.parent_1.height
        elif (self.direction == 'y'): 
            assert (self.parent_1.x == self.parent_2.x and 
                    self.parent_1.width == self.parent_2.width)
            self.x = self.parent_1.x; 
            self.y = self.parent_1.y + self.parent_1.height; 
            self.width = self.parent_1.width; 
            self.height = boundary_thickness; 
        else: raise RTSAI_Boundary_Direction_Exception

        widget_configure (self)
        widget_place (self)
        self.event_diff_x = 0; self.event_diff_y = 0; 
        self.bind("<Button-1>", self.boundary_drag_init)
        self.bind("<B1-Motion>", self.boundary_drag_place)
        self.bind("<Enter>", self.boundary_appear)
        self.bind("<Leave>", self.boundary_disappear)

    def boundary_drag_init(self, event): 
        event_x, event_y = event_get_relative_coordinate(event, self.master)
        self.event_diff_x = self.x - event_x
        self.event_diff_y = self.y - event_y

    def boundary_drag_place(self, event): 
        event_x, event_y = event_get_relative_coordinate(event, self.master)
        if (self.direction == 'x'): 
            self.x = event_x + self.event_diff_x; 
            x_max = self.parent_1.x + self.parent_1.width + self.parent_2.width - self.width
            x_min = self.parent_1.x
            if (self.x > x_max): self.x = x_max
            elif (self.x < x_min): self.x = x_min
            horizontal_movement = self.x - self.parent_1.x - self.parent_1.width
            self.parent_1.width += horizontal_movement
            self.parent_2.x += horizontal_movement
            self.parent_2.width -= horizontal_movement
        elif (self.direction == 'y'): 
            self.y = event_y + self.event_diff_y; 
            y_max = self.parent_1.y + self.parent_1.height + self.parent_2.height - self.height
            y_min = self.parent_1.y
            if (self.y > y_max): self.y = y_max
            elif (self.y < y_min): self.y = y_min
            vertical_movement = self.y - self.parent_1.y - self.parent_1.height
            self.parent_1.height += vertical_movement
            self.parent_2.y += vertical_movement
            self.parent_2.height -= vertical_movement
        else: raise Exception
        widget_place (self)
        widget_place (self.parent_1)
        widget_configure (self.parent_1)
        widget_place (self.parent_2)
        widget_configure (self.parent_2)
        
    def boundary_appear(self, event): 
        self.configure(bg = color_tuple_to_rgb(boundary_color_hover))

    def boundary_disappear(self, event): 
        self.configure(bg = color_tuple_to_rgb(boundary_color_original))

class RTSAI_Panel(tkinter.Frame): 

    def __init__(self, master, name = f"Widget {new_ID()}", x = 0, y = 0, width = 200, height = 200, **options): 
        tkinter.Frame.__init__(self, master, **options)
        self.master = master; 
        self.name = name; 

        self.width = width; self.height = height; 
        self.x = x; self.y = y; 
        widget_configure (self)
        widget_place (self)

class RTSAI_Window(tkinter.Tk): 

    def __init__(self, name = f"Window {new_ID()}", title = "Tkinter Window", width = 200, height = 200, x = 5, y = 30, **options): 
        
        tkinter.Tk.__init__(self, **options)
        self.name = name; self.title (title)
        self.width = width; self.height = height; 
        widget_configure(self)
        window_geometry(self) # will set self.x and self.y

def RTSAI_chat_window(): 

    RTSAI_window = RTSAI_Window(name = "RTSAI Window", title = "RTSAI", width = window_width, height = window_height)

    # Render the left and the right panels, and the boundary
    left_panel = RTSAI_Panel(RTSAI_window, name = "Left Panel", background=color_tuple_to_rgb(left_panel_color), width=window_left_width, height=window_height, x = 0, y = 0)
    right_panel = RTSAI_Panel(RTSAI_window, name = "Right Panel", background=color_tuple_to_rgb(right_panel_color), width=window_width-window_left_width, height=window_height, x = window_left_width, y = 0)
    left_right_boundary = RTSAI_Boundary(RTSAI_window, left_panel, right_panel, name = "Left Right Boundary", background = color_tuple_to_rgb(boundary_color_original))

    if (debug == 0): print (f"sys.platform: {sys.platform}")
    if (sys.platform.startswith("darwin")): RTSAI_window.iconphoto(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png")))
    else: RTSAI_window.iconbitmap(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png"))) # to be tested

    RTSAI_window.mainloop()

def main(): 
    if (len(sys.argv) == 1 and sys.argv[0] == f'{EXECUTABLE_PATH}/{COMMAND_NAME}'): 
        print (f"{PACKAGE_NAME}: Hello World! ")
        RTSAI_chat_window()

if __name__ == '__main__': 
    main()

