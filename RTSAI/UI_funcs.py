
import tkinter
from tkinter.font import Font
import RTSAI.UI_config as UI_config
import RTSAI.UI_components as UI_components
import textwrap

debug = 1

def show_popup_message(message, title = "Message", parent_item = None):
    import tkinter
    if parent_item is None:
        parent_item = UI_components.window
    tkinter.messagebox.showinfo(title, message, parent = parent_item)

def wrap_label_text(parent_label, expected_width = None, label_text = None, text_align = tkinter.CENTER): 
    '''
    Rendering the label_text, by adding necessary newline characters
    '''
    if (not expected_width): 
        expected_width = parent_label.winfo_width()
    if (not label_text): 
        label_text = parent_label.cget("text")
    textwrap_width = int(expected_width / UI_config.label_width_ratio_wrap)
    if (debug == 0): print (f"textwrap width: {textwrap_width}")
    new_text = textwrap.fill(label_text, textwrap_width)
    parent_label.configure(text = new_text, justify=text_align)

def measure_label_width(label): 
    label_text = label.cget("text")
    font = Font(font=label.cget("font"))
    label_width = font.measure(label_text)
    if (debug == 0): print (f"Label width measuring: '{label_text}' [{label_width}]")
    return (label_width)
