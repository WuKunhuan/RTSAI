
import tkinter
import RTSAI.config as config
from RTSAI.tool_funcs import color_tuple_to_rgb

class Left_Sidebar_Icon(tkinter.Canvas):
    '''
    The left sidebar icon objects
    '''
    def __init__(self, hover_color = config.VSCode_highlight_color):
        super().__init__(master = config.left_panel_sidebar, width=config.left_panel_sidebar_width, height=config.left_panel_sidebar_width, 
                            bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0)
        self.hovered = False
        self.hover_color = hover_color
        self.items_in_panel = []
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.pack(side = "top")

    def on_enter(self, event): 
        self.hovered = True
        for item in self.items_in_panel: 
            self.itemconfigure(item, fill=color_tuple_to_rgb(self.hover_color))

    def on_leave(self, event):
        self.hovered = False
        for item in self.items_in_panel: 
            self.itemconfigure(item, fill=color_tuple_to_rgb(config.VSCode_font_grey_color))
