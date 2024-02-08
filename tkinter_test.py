# Import Library
from tkinter import Tk, ttk, Button, LabelFrame, HORIZONTAL, VERTICAL
 
# Create Object
root = Tk()
 
# Set title
root.title("Controls")
 
# Set Geometry
root.geometry("400x500")
 
# Make Button
launch_button = Button(root,
                       text = "launch Window")
launch_button.pack(pady = 10)
 
# Add Label Frames
width_frame = LabelFrame(root,
                         text = "Change width")
 
width_frame.pack(pady = 10)
 
height_frame = LabelFrame(root,
                          text = "change height")
height_frame.pack(pady = 10)
 
both_frame = LabelFrame(root,
                        text = "change both")
 
both_frame.pack(pady = 10)
 
# Add Scale bar
width_slider = ttk.Scale(width_frame,
                         from_ = 100,
                         to = 500,
                         orient = HORIZONTAL,
                         length = 200, value = 100)
 
width_slider.pack(pady = 10, padx = 20)
 
height_slider = ttk.Scale(height_frame,
                          from_ = 100, to = 500,
                          orient = VERTICAL, 
                          length = 200, value = 100)
height_slider.pack(pady = 10, padx = 20)
 
both_slider = ttk.Scale(both_frame, from_ = 100,
                        to = 500, orient = HORIZONTAL,
                        length = 200, value = 100)
 
both_slider.pack(pady = 10,padx = 20)
 
# Execute Tkinter
root.mainloop()

