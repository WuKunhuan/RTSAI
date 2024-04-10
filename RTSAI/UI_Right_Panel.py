
import tkinter, math
import RTSAI.config as config
from RTSAI.tool_funcs import color_tuple_to_rgb
from RTSAI.counter import new_ID

debug = 1

class Right_Panel_Main_Window(tkinter.Frame): 

    class Window_Operation: 
        
        def __init__ (self, optype, opinfo): 
            pass
    
    class Window_File: 

        def __init__(self): 
            pass
    
    class Window_Element: 
        '''
        Encapsulate the window elements
        '''
        def __init__ (self, element): 
            self.element = element
            self.relwidth = 1

    def create_dialog_box(self, parent_frame, hint_text, button_text, web_crawl_function, upload_file_function = None): 
        '''
        Create the dialog box and pack it to the parent frame. 
        '''
        
        def dialog_box_upload_configure(dialog_box_upload): 
            canvas_width = dialog_box_upload.winfo_width()
            canvas_height = dialog_box_upload.winfo_height()
            dialog_box_upload.delete("box")
            dialog_box_upload.delete("arrow")
            box_points = [
                canvas_width * 0.1, canvas_height * 0.5, 
                canvas_width * 0.2, canvas_height * 0.5, 
                canvas_width * 0.2, canvas_height * 0.8, 
                canvas_width * 0.8, canvas_height * 0.8, 
                canvas_width * 0.8, canvas_height * 0.5, 
                canvas_width * 0.9, canvas_height * 0.5, 
                canvas_width * 0.9, canvas_height * 0.9, 
                canvas_width * 0.1, canvas_height * 0.9, 
            ]
            arrow_points = [
                canvas_width * 0.5, canvas_height * 0.05, 
                canvas_width * 0.75, canvas_height * 0.3, 
                canvas_width * 0.65, canvas_height * 0.3, 
                canvas_width * 0.55, canvas_height * 0.35, 
                canvas_width * 0.55, canvas_height * 0.7, 
                canvas_width * 0.45, canvas_height * 0.7, 
                canvas_width * 0.45, canvas_height * 0.35, 
                canvas_width * 0.35, canvas_height * 0.3, 
                canvas_width * 0.25, canvas_height * 0.3, 
            ]
            dialog_box_upload.create_polygon(box_points, tags = "box", fill=color_tuple_to_rgb(config.VSCode_font_grey_color), smooth = False)
            dialog_box_upload.create_polygon(arrow_points, tags = "arrow", fill=color_tuple_to_rgb(config.VSCode_font_grey_color), smooth = False)

        def dialog_box_text_change(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == "": 
                dialogue_box.master.focus_set()
                dialogue_box.after(10, lambda: dialog_box_restore_hint_text(dialogue_box))
            else: dialogue_box.config(fg="black")  # Change text color to black
            dialogue_box_height = dialogue_box.tk.call((dialogue_box._w, "count", "-update", "-displaylines", "1.0", "end"))
            dialogue_box.configure(height = dialogue_box_height)

        def dialog_box_restore_hint_text(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == "":
                dialogue_box.delete("1.0", "end")  # Clear the hint text
                dialogue_box.insert("1.0", hint_text)  # Restore the hint text
                dialogue_box.config(fg="gray")  # Change text color to gray

        def upload_hover_leave(parent_canvas, parent_elements, fill_color = config.VSCode_new_color): 
            for element in parent_elements: 
                parent_canvas.itemconfigure(element, fill=color_tuple_to_rgb(fill_color))

        def upload_focus_in(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == hint_text:
                dialogue_box.delete("1.0", "end")  # Clear the hint text
                dialogue_box.config(fg="black")  # Restore black text color

        def upload_focus_out(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == "":
                dialogue_box.after(10, lambda: dialog_box_restore_hint_text(dialogue_box))

        def crawl_hover(crawl_canvas): 
            crawl_canvas.configure(fg = 'white', bg = color_tuple_to_rgb(config.VSCode_new_color))

        def crawl_leave(crawl_canvas): 
            crawl_canvas.configure(fg = color_tuple_to_rgb(config.VSCode_font_grey_color), bg = color_tuple_to_rgb(config.grey_color_64))

        '''
        Create the dialog box
        '''
        dialogue_box = tkinter.Text(parent_frame, height=1, wrap="word", fg="gray", highlightthickness=0, relief='ridge')
        dialogue_box.insert("1.0", hint_text)
        dialogue_box.bind("<FocusIn>", lambda event: upload_focus_in(dialogue_box))
        dialogue_box.bind("<FocusOut>", lambda event: upload_focus_out(dialogue_box))
        dialogue_box.bind("<KeyRelease>", lambda event: dialog_box_text_change(dialogue_box))

        '''
        Create the dialog box button
        '''
        dialog_box_button = tkinter.Label(parent_frame, text = button_text, font = [config.standard_font_family, config.standard_font_size], 
                                            bg = color_tuple_to_rgb(config.grey_color_64), fg = color_tuple_to_rgb(config.VSCode_font_grey_color))
        dialog_box_button.pack(side="right", padx=5, pady=5)
        dialog_box_button.bind("<Enter>", lambda event: crawl_hover(dialog_box_button))
        dialog_box_button.bind("<Leave>", lambda event: crawl_leave(dialog_box_button))
        dialog_box_button.bind("<Button-1>", lambda event: web_crawl_function(dialogue_box))

        '''
        Create the dialog box upload button (if applicable)
        '''
        if (upload_file_function): 
            dialog_box_upload = tkinter.Canvas(parent_frame, width = config.dialog_box_icon_size, height = config.dialog_box_icon_size, 
                                                bg = color_tuple_to_rgb(config.grey_color_43), highlightthickness=0, relief='ridge')
            dialog_box_upload.bind("<Enter>", lambda event: upload_hover_leave(dialog_box_upload, ["box", "arrow"], config.VSCode_new_color))
            dialog_box_upload.bind("<Leave>", lambda event: upload_hover_leave(dialog_box_upload, ["box", "arrow"], config.VSCode_font_grey_color))
            dialog_box_upload.bind("<Configure>", lambda event: dialog_box_upload_configure(dialog_box_upload))
            dialog_box_upload.bind("<Button-1>", lambda event: upload_file_function(dialogue_box))
            dialog_box_upload.pack(side="right", padx=5, pady=5)
            
        dialogue_box.pack(side="left", fill='both', expand=True, pady=5)

    def configure(self): 
        if (debug == 0): print (f"Configure right panel main window ... {new_ID()}")
        pass

    def __init__(self, winkey, wintype): 
        super().__init__(master=config.right_panel_main, bg=color_tuple_to_rgb(config.right_panel_color))  # right_panel_main
        self.bind('<Configure>', lambda event: self.configure())

        right_panel_main_bottom_arrow_area = tkinter.Canvas(self, height = config.size_increase_arrow_height + 8 * config.boundary_width, 
                                            bg=color_tuple_to_rgb(config.right_panel_color), highlightthickness = 0, relief='ridge')
        right_panel_main_bottom_arrow_area.pack(side="bottom", fill="x")
        self.key = winkey; self.type = wintype; self.status = "SAVED"

        '''
        Save the window elements for dynamic rendering (especially considering the width)
        '''
        self.window_elements = []  # A sequence of Window_Element. Order matters. Elements will be packed. 

        '''
        Save window operations. Allow restoration. 
        '''
        self.operations = []
        self.current_operation = -1

        '''
        Create the main window components based on the window type
        '''
        if (wintype == "CRAWL"): 

            from RTSAI.UI_funcs import wrap_label_text
            def web_crawl(dialogue_box): 
                dialog_box_value = dialogue_box.get("1.0", "end-1c")
                print (dialog_box_value)

            dialog_box_uploaded_files = []
            def file_upload(dialogue_box): 
                pass

            web_crawl_main_panel = tkinter.Canvas(self, bg=color_tuple_to_rgb(config.right_panel_color), highlightthickness=0, relief='ridge')
            web_crawl_main_panel.pack(side = 'top', fill = 'both', expand = True)
            temp_frame = tkinter.Frame(web_crawl_main_panel, bg=color_tuple_to_rgb(config.VSCode_highlight_color))
            temp_frame.pack (side = 'top', fill = 'x')

            '''
            Generate the dialog box (including the upload and the crawl buttons) on the botton
            '''
            dialogue_box_panel = tkinter.Frame(self, bg=color_tuple_to_rgb(config.grey_color_43))
            self.create_dialog_box(dialogue_box_panel, "Enter web URL ...", "Crawl", web_crawl, file_upload)
            dialogue_box_panel.pack(side='bottom', fill='x')

            '''
            Generate the main AI panel
            -  The title
            -  The introduction
            -  The existing chats
            '''
            right_panel_width = math.floor(config.window_width - config.left_panel_width)
            web_crawl_title = tkinter.Label(temp_frame, text="Web Crawl", font = [config.standard_font_family, config.h1_font_size, "bold"], 
                                            bg = color_tuple_to_rgb(config.right_panel_color), fg = color_tuple_to_rgb(config.VSCode_font_grey_color))
            wrap_label_text(web_crawl_title, math.floor(right_panel_width * 0.95))
            web_crawl_title.pack (side = 'top', fill = 'x')
            self.window_elements.append(self.Window_Element(web_crawl_title))
            web_crawl_intro = tkinter.Label(temp_frame, text="The web crawl function is designed to gather valuable data and construct a knowledge graph from the web, enabling the retrieval of useful information. ", 
                                            font = [config.standard_font_family, config.standard_font_size, "bold"], 
                                            bg = color_tuple_to_rgb(config.right_panel_color), fg = color_tuple_to_rgb(config.VSCode_font_grey_color))
            wrap_label_text(web_crawl_intro, math.floor(right_panel_width * 0.95))
            web_crawl_intro.pack(side = 'top', fill = 'x')
            self.window_elements.append(self.Window_Element(web_crawl_intro))

        elif (wintype == "TEXT"): 
            pass

        '''
        No need to pack the window into the right panel
        Instead, we save it to the config list. 
        '''
        config.editor_windows[winkey] = self
