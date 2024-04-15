
import tkinter
from RTSAI import config
from RTSAI.tool_funcs import color_tuple_to_rgb

window = tkinter.Tk()

frame = tkinter.Frame(window, bg=color_tuple_to_rgb(UI_config.VSCode_new_color))

text = "Sure! Here's an example of how you can use the pack geometry manager to place multiple Label widgets in a single row: "
tokens = text.strip().split(' ')

for token in tokens: 
    token_label = tkinter.Label(frame, text = token, 
                                bg=color_tuple_to_rgb(UI_config.VSCode_highlight_color), 
                                fg=color_tuple_to_rgb(UI_config.VSCode_font_grey_color))
    token_label.pack(side=tkinter.TOP, anchor=tkinter.NW, fill=tkinter.X)

frame.pack(side = 'top', fill = 'both', expand = True)

window.mainloop()
