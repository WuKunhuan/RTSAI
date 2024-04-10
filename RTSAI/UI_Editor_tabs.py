
import tkinter, math
from tkinter.font import Font
import RTSAI.config as config
from RTSAI.counter import new_ID
from RTSAI.tool_funcs import color_tuple_to_rgb
from RTSAI.UI_Icons import draw_chat_icon, draw_crawl_icon
from RTSAI.UI_Right_Panel import Right_Panel_Main_Window

debug = 1

class Editor_Tab(tkinter.Frame): 
    '''
    The editor tabs inside the tab bar
    '''

    def draw_tab_icon_status(self): 
        '''
        Draw tab icon and status
        '''
        if (debug == 0): print (f"Draw tab icon for {self.tab_type}|{self.tab_value}")
        canvas_width = config.right_panel_tabbar_height - self.active_bar_thickness; 
        canvas_height = config.right_panel_tabbar_height - self.active_bar_thickness; 
        self.tab_status.delete("tab_status_indicator")

        '''
        Draw tab icon
        '''
        if (self.tab_type == "CHAT"): 
            draw_chat_icon(self.tab_icon, config.right_panel_tabbar_height - self.active_bar_thickness, config.right_panel_tabbar_height - self.active_bar_thickness, color_tuple_to_rgb(config.chat_icon_color))
        elif (self.tab_type == "CRAWL"): 
            draw_crawl_icon(self.tab_icon, config.right_panel_tabbar_height - self.active_bar_thickness, config.right_panel_tabbar_height - self.active_bar_thickness, color_tuple_to_rgb(config.crawl_icon_color))
        '''
        Draw tab status
        '''
        if (self.tab_status_display == "HOVER"): 
            cross_points = [
                canvas_width * 0.3, canvas_height * 0.2,  
                canvas_width * 0.5, canvas_height * 0.4,  
                canvas_width * 0.7, canvas_height * 0.2,  
                canvas_width * 0.8, canvas_height * 0.3,  
                canvas_width * 0.6, canvas_height * 0.5, 
                canvas_width * 0.8, canvas_height * 0.7,  
                canvas_width * 0.7, canvas_height * 0.8, 
                canvas_width * 0.5, canvas_height * 0.6,  
                canvas_width * 0.3, canvas_height * 0.8,  
                canvas_width * 0.2, canvas_height * 0.7,  
                canvas_width * 0.4, canvas_height * 0.5, 
                canvas_width * 0.2, canvas_height * 0.3,  
            ]
            self.tab_status.create_polygon(cross_points, tags = "tab_status_indicator", fill = color_tuple_to_rgb(config.VSCode_font_grey_color))
        elif (self.tab_status == "MODIFIED"): 
            self.tab_status.create_oval(canvas_width * 0.25, canvas_height * 0.25, canvas_height * 0.75, canvas_height * 0.75, tags = "tab_status_indicator", fill = color_tuple_to_rgb(config.VSCode_font_grey_color))
        else: pass # == "SAVED"

    def hover_tab(self): 
        if (debug == 0): print (f"Hover the tab {self.tab_type}|{self.tab_value}")
        self.tab_status_display = "HOVER"; self.draw_tab_icon_status()
        if (not config.current_editor_id == self.id): 
            self.tab_label.configure(bg = color_tuple_to_rgb(config.right_panel_color))
            self.tab_status.configure(bg = color_tuple_to_rgb(config.right_panel_color))

    def leave_tab(self): 
        self.tab_status_display = "DEFAULT"; self.draw_tab_icon_status()
        if (not config.current_editor_id == self.id): 
            self.tab_label.configure(bg = color_tuple_to_rgb(config.left_panel_color))
            self.tab_status.configure(bg = color_tuple_to_rgb(config.left_panel_color))
    
    def click_tab(self): 
        if (config.current_editor_id != self.id): 
            config.current_editor_id = self.id
            config.tabbar_shown = False; show_editor_tabbar()
            config.editor_updated = False; configure_editor()

    def close_tab(self): 
        config.editor_states = config.editor_states[0:self.id] + config.editor_states[self.id+1:]
        if (config.current_editor_id == self.id): 
            config.current_editor_id = -1
            if (config.current_editor): 
                config.current_editor.pack_forget()
                config.current_editor = None
        elif (config.current_editor_id > self.id): 
            config.current_editor_id -= 1

        if (config.editor_states): 
            config.tabbar_shown = False; show_editor_tabbar(tabbar_width = config.right_panel_width)
        else: hide_editor_tabbar()

    def measure_tab_label_width(self, label): 
        label_text = label.cget("text")
        font = Font(font=label.cget("font"))
        label_width = font.measure(label_text)
        if (debug == 0): print (f"Label width measuring: '{label_text}' [{label_width}]")
        return (label_width)

    def __init__(self, id, master, tab_type, tab_value, tab_display_name, tab_status): 
        super().__init__(master, bg = color_tuple_to_rgb(config.left_panel_color), 
                            highlightbackground=color_tuple_to_rgb(config.grey_color_43), 
                            highlightthickness=config.boundary_width)
        
        self.id = id; self.tab_type = tab_type; self.tab_value = tab_value
        self.tab_display_name = tab_display_name; 
        self.tab_status = tab_status; 
        self.tab_status_display = "DEFAULT"
        self.active_bar_thickness = 4

        self.font = (config.standard_font_family, config.standard_font_size)
        self.tab_active_bar = tkinter.Frame(self, height = self.active_bar_thickness, bg = color_tuple_to_rgb(config.right_panel_color))
        self.tab_icon = tkinter.Canvas(self, height = config.right_panel_tabbar_height - self.active_bar_thickness, highlightthickness=0)
        self.tab_label = tkinter.Label(self, text = tab_display_name, font = self.font, fg = color_tuple_to_rgb(config.VSCode_font_grey_color))
        self.tab_status = tkinter.Canvas(self, height = config.right_panel_tabbar_height - self.active_bar_thickness, highlightthickness=0)

        if (config.current_editor_id == self.id or self.tab_status_display == "HOVER"): 
            self.tab_active_bar.configure(bg = color_tuple_to_rgb(config.VSCode_highlight_color))
            self.tab_icon.configure(bg = color_tuple_to_rgb(config.grey_color_43))
            self.tab_label.configure(bg = color_tuple_to_rgb(config.grey_color_43))
            self.tab_status.configure(bg = color_tuple_to_rgb(config.grey_color_43))
        else: 
            self.tab_icon.configure(bg = color_tuple_to_rgb(config.left_panel_color))
            self.tab_label.configure(bg = color_tuple_to_rgb(config.left_panel_color))
            self.tab_status.configure(bg = color_tuple_to_rgb(config.left_panel_color))
        
        '''
        Configure the width of items
        '''
        tab_label_width = math.ceil(self.measure_tab_label_width(self.tab_label) / config.label_width_ratio)
        self.tab_label.configure(width = tab_label_width)
        tab_icon_width = config.right_panel_tabbar_height - self.active_bar_thickness
        tab_status_width = config.right_panel_tabbar_height - self.active_bar_thickness
        self.tab_icon.configure(width = tab_icon_width)
        self.tab_status.configure(width = tab_status_width)
        self.width = int(tab_icon_width + (tab_label_width + 1) * config.label_width_ratio + tab_status_width)
        self.configure(width = self.width) 

        self.tab_active_bar.pack(side = 'top', fill = 'x')
        self.tab_icon.pack(side = 'left', expand = False)
        self.tab_label.pack(side = 'left', expand = False)
        self.tab_status.pack(side = 'left', expand = False)

        '''
        Bind tab events
        '''
        self.bind("<Configure>", lambda event: self.draw_tab_icon_status())
        self.tab_icon.bind("<Enter>", lambda event: self.hover_tab())
        self.tab_label.bind("<Enter>", lambda event: self.hover_tab())
        self.tab_status.bind("<Enter>", lambda event: self.hover_tab())
        self.tab_icon.bind("<Leave>", lambda event: self.leave_tab())
        self.tab_label.bind("<Leave>", lambda event: self.leave_tab())
        self.tab_status.bind("<Leave>", lambda event: self.leave_tab())
        self.tab_label.bind("<Button-1>", lambda event: self.click_tab())
        self.tab_status.bind("<Button-1>", lambda event: self.close_tab())

def configure_editor(): 
    '''
    Render the right_panel_main, and show the editor window
    '''
    if (debug == 0): print ("Configure editor window ... ")

    if (config.editor_updated): 
        return
    else: 
        if (config.current_editor): 
            config.current_editor.pack_forget()
        config.editor_updated = True

    if (config.current_editor_id != -1): 
        state = config.editor_states[config.current_editor_id]
        if (f"{state[0]}|{state[1]}" in config.editor_windows.keys()): 
            config.current_editor = config.editor_windows[f"{state[0]}|{state[1]}"]
        else: 
            config.current_editor = Right_Panel_Main_Window(f"{state[0]}|{state[1]}", state[0])
    else: 
        config.current_editor = tkinter.Frame(config.right_panel_main, bg = color_tuple_to_rgb(config.VSCode_new_color))
    config.current_editor.pack(side = 'top', fill = 'both', expand = True)

    '''
    Pack the right_panel_main panel to show the editor
    '''
    config.right_panel_main.pack(side='top', fill='both', expand=True)

def show_editor_tabbar(tabbar_width = None): 
    '''
    Show the tabbar in the right panel
    '''
    if (debug == 0): print (f"Show tabbar ... (width = {tabbar_width})")
    if (config.tabbar_shown): return
    else: config.tabbar_shown = True

    '''
    Create the tabbar
    Temporarily forget the right panel main as well as the scrollbar
    '''
    if (not tabbar_width): 
        tabbar_width = config.right_panel.winfo_width() - 4 * config.boundary_width
    if (not config.right_panel): return
    if (config.right_panel_tabbar): 
        if (debug == 0): print ("right panel tabbar pack forget. ")
        config.right_panel_tabbar.pack_forget()
    if (config.right_panel_tabbar_scrollbar): 
        config.right_panel_tabbar_scrollbar.pack_forget()
    if (config.right_panel_main): 
        config.right_panel_main.pack_forget()

    config.right_panel_tabbar = tkinter.Canvas(config.right_panel, height=config.right_panel_tabbar_height, 
                                                bg=color_tuple_to_rgb(config.VSCode_new_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
    if (debug == 1): print ("right panel tabbar pack back. ")
    config.right_panel_tabbar.pack(side='top', fill='x')
    total_width = 0; 
    tab_frame = tkinter.Frame(config.right_panel_tabbar); 
    config.right_panel_tabbar.create_window((0, 0), window=tab_frame, anchor="nw", tags="tab_frame")
    
    '''
    Create the tabs for each editor
    '''
    for tab_id, editor_tab in enumerate(config.editor_states): 
        tab_type = editor_tab[0]; tab_value = editor_tab[1]
        tab_display_name = editor_tab[2]; 



        tab_status = "SAVED" ### TO BE FIXED: detection method



        new_tab = Editor_Tab(tab_id, tab_frame, tab_type, tab_value, tab_display_name, tab_status)
        total_width += new_tab.width; 
        new_tab.pack(side = 'left')
    
    '''
    Create the scrollbar when there are too many editors
    '''
    if (config.right_panel.winfo_width() != 1 and total_width > tabbar_width): 
        config.right_panel_tabbar_scrollbar = tkinter.Scrollbar(config.right_panel, orient="horizontal", command=config.right_panel_tabbar.xview, width = config.right_panel_tabbar_scrollbar_width) # color setting options do not work
        config.right_panel_tabbar.configure(xscrollcommand=config.right_panel_tabbar_scrollbar.set)
        config.right_panel_tabbar_scrollbar.pack(side='top', fill='x')
        config.right_panel_tabbar_scrollbar_created = True
        if (config.right_panel_tabbar_scrollbar_position): 
            position = config.right_panel_tabbar_scrollbar_position
            config.right_panel_tabbar.after(1000, lambda: config.right_panel_tabbar.xview_moveto(position[0]))
        def right_panel_tabbar_scrollbar_save_scroll_position(): 
            config.right_panel_tabbar_scrollbar_position = config.right_panel_tabbar_scrollbar.get()
        config.right_panel_tabbar_scrollbar.bind("<Motion>", lambda event: right_panel_tabbar_scrollbar_save_scroll_position())

    '''
    Bind the tabbar with configuration event
    '''
    def configure_tab_frame(): 
        if (debug == 1): print (f"Configure right panel tab frame ... {new_ID()}")
        config.right_panel_tabbar.configure(scrollregion=config.right_panel_tabbar.bbox("all"))
        tabbar_width_new = config.right_panel.winfo_width() - 4 * config.boundary_width
        if (total_width <= tabbar_width_new and config.right_panel_tabbar_scrollbar): 
            config.right_panel_tabbar_scrollbar.pack_forget(); 
            config.right_panel_tabbar_scrollbar = None
            config.right_panel_tabbar_scrollbar_created = False
            config.right_panel_tabbar_scrollbar_position = None
        elif (total_width > tabbar_width_new and not config.right_panel_tabbar_scrollbar_created): 
            config.right_panel_tabbar_scrollbar_created = True
            config.tabbar_shown = False; config.right_panel_tabbar.after(100, show_editor_tabbar(tabbar_width = config.right_panel_width))
        config.editor_updated = False; configure_editor()

    tab_frame.bind("<Configure>", lambda event: configure_tab_frame())
    configure_tab_frame()

def hide_editor_tabbar(): 
    if (not config.right_panel): return
    if config.right_panel_tabbar:
        config.right_panel_tabbar.pack_forget()
        config.right_panel_tabbar = None

def check_editor_status (source_file): 
    opened_editors = [editor[0] for editor in config.editor_states]
    if (source_file not in opened_editors): return None
    else: return (config.editor_states[opened_editors.index(source_file)][1])
