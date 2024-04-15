import tkinter
import textwrap

root = tkinter.Tk()
question = "This is a very long sentence that needs wrapping else it will run out of space. To dynamically wrap the text when resizing the window and place it under the label on the left side, you can use the textvariable option of the Label widget and the LEFT value for the anchor parameter. Here's an updated example:"
line_width_constant = 6
label = tkinter.Label(root, text=textwrap.fill(question, 20), anchor=tkinter.W, justify=tkinter.LEFT)
label.pack(side = 'left', anchor = 'n')

def wrap_text(widget): 
    original_text = widget.cget("text")
    window_width = int(int(root.geometry().split('x')[0])/line_width_constant) - 2
    new_text = textwrap.fill(original_text, window_width)
    print (f"New window width: {window_width}")
    print (f"New text: {new_text}\n")
    widget.configure(text = new_text, anchor=tkinter.W, justify=tkinter.LEFT)

root.bind("<Configure>", lambda event: wrap_text(label))

root.mainloop()