
import tkinter, math
import RTSAI.config as config
import RTSAI.UI_config as UI_config
import RTSAI.UI_components as UI_components
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
        Represent different window (major) elements in the main panel
        '''
        def __init__ (self, element, side = tkinter.TOP, anchor = 'center', padx = 0, pady = 0, 
                      relwidth = None, text_based_element = False, text_relwidth = None, 
                      element_name = None): 
            self.element = element
            self.side = side
            self.anchor = anchor
            self.relwidth = relwidth # will be used in main window configure event
            self.text_based_element = text_based_element # will be used in main window configure event
            self.text_relwidth = text_relwidth # will be used in main window configure event
            if (not element_name): 
                element_name = f"window element (type: {element})"
            self.element_name = element_name
            if (self.relwidth != None): 
                self.element.pack(side = side, anchor = anchor, padx = padx, pady = pady)
            else: 
                self.element.pack(side = side, anchor = anchor, padx = padx, pady = pady, fill = 'x')

    def window_element_wrap_text(self, window_element, expected_width = None): 
        from RTSAI.UI_funcs import wrap_label_text
        if (expected_width == None): 
            right_panel_width = math.floor(config.window_width - UI_config.left_panel_width)
            if (window_element.text_relwidth != None): 
                expected_width = math.floor(right_panel_width * window_element.text_relwidth)
            else: 
                expected_width = math.floor(right_panel_width * 0.95)
        wrap_label_text(window_element.element, expected_width)

    def new_window_image_id(self): 
        self.window_image_id += 1
        return (self.window_image_id)
        
    def create_dialog_box(self, parent_frame, button_text, button_function, upload_file_function = None): 
        '''
        Create the dialog box and pack it to the parent frame. 
        The dialogue box is associated with an optional file upload option. 
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
            dialog_box_upload.create_polygon(box_points, tags = "box", fill=color_tuple_to_rgb(UI_config.VSCode_font_grey_color), smooth = False)
            dialog_box_upload.create_polygon(arrow_points, tags = "arrow", fill=color_tuple_to_rgb(UI_config.VSCode_font_grey_color), smooth = False)

        def dialog_box_text_change(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == "": 
                dialogue_box.master.focus_set()
                dialogue_box.after(10, lambda: dialog_box_restore_hint_text(dialogue_box))
            else: dialogue_box.config(fg="black")  # Change text color to black
            dialogue_box_height = dialogue_box.tk.call((dialogue_box._w, "count", "-update", "-displaylines", "1.0", "end"))
            dialogue_box.configure(height = dialogue_box_height)

        def dialog_box_restore_hint_text(dialogue_box): 
            '''
            Restore the dialog box hint text
            '''
            if dialogue_box.get("1.0", "end-1c") == "":
                dialogue_box.delete("1.0", "end")
                dialogue_box.insert("1.0", self.dialogue_box_hint_text)
                dialogue_box.config(fg="gray")

        def upload_hover_leave(parent_canvas, parent_elements, fill_color = UI_config.VSCode_new_color): 
            for element in parent_elements: 
                parent_canvas.itemconfigure(element, fill=color_tuple_to_rgb(fill_color))

        def upload_focus_in(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == self.dialogue_box_hint_text or dialogue_box.get("1.0", "end-1c") == self.dialogue_box_error_text:
                dialogue_box.delete("1.0", "end")  # Clear the hint text
                dialogue_box.config(fg="black")  # Restore black text color

        def upload_focus_out(dialogue_box):
            if dialogue_box.get("1.0", "end-1c") == "":
                dialogue_box.after(10, lambda: dialog_box_restore_hint_text(dialogue_box))

        def crawl_hover(crawl_canvas): 
            crawl_canvas.configure(fg = 'white', bg = color_tuple_to_rgb(UI_config.VSCode_new_color))

        def crawl_leave(crawl_canvas): 
            crawl_canvas.configure(fg = color_tuple_to_rgb(UI_config.VSCode_font_grey_color), bg = color_tuple_to_rgb(UI_config.grey_color_64))

        '''
        Create the dialog box main body
        '''
        dialogue_box = tkinter.Text(parent_frame, height=1, wrap="word", fg="gray", highlightthickness=0, relief='ridge', 
                                    font = (UI_config.standard_font_family, UI_config.dialog_box_font_size))
        dialogue_box.insert("1.0", self.dialogue_box_hint_text)
        dialogue_box.bind("<FocusIn>", lambda event: upload_focus_in(dialogue_box))
        dialogue_box.bind("<FocusOut>", lambda event: upload_focus_out(dialogue_box))
        dialogue_box.bind("<KeyRelease>", lambda event: dialog_box_text_change(dialogue_box))

        '''
        Create the dialog box button
        bind it to the web_crawl_function
        '''
        dialog_box_button = tkinter.Label(parent_frame, text = button_text, font = [UI_config.standard_font_family, UI_config.standard_font_size], 
                                            bg = color_tuple_to_rgb(UI_config.grey_color_64), fg = color_tuple_to_rgb(UI_config.VSCode_font_grey_color))
        dialog_box_button.pack(side="right", padx=5, pady=5)
        dialog_box_button.bind("<Enter>", lambda event: crawl_hover(dialog_box_button))
        dialog_box_button.bind("<Leave>", lambda event: crawl_leave(dialog_box_button))
        # button_function retrieves value from the dialogue box, and call the create_message function
        dialog_box_button.bind("<Button-1>", lambda event: button_function(dialogue_box))

        '''
        Create the dialog box upload button (if applicable)
        '''
        if (upload_file_function): 
            dialog_box_upload = tkinter.Canvas(parent_frame, width = UI_config.dialog_box_icon_size, height = UI_config.dialog_box_icon_size, 
                                                bg = color_tuple_to_rgb(UI_config.grey_color_43), highlightthickness=0, relief='ridge')
            dialog_box_upload.bind("<Enter>", lambda event: upload_hover_leave(dialog_box_upload, ["box", "arrow"], UI_config.VSCode_new_color))
            dialog_box_upload.bind("<Leave>", lambda event: upload_hover_leave(dialog_box_upload, ["box", "arrow"], UI_config.VSCode_font_grey_color))
            dialog_box_upload.bind("<Configure>", lambda event: dialog_box_upload_configure(dialog_box_upload))
            dialog_box_upload.bind("<Button-1>", lambda event: upload_file_function(dialogue_box))
            dialog_box_upload.pack(side="right", padx=5, pady=5)
            
        dialogue_box.pack(side="left", fill='both', expand=True, pady=5)

    def create_main_window_entry(self, sender, content_type, content): 
        '''
        Add the component as an entry in the window. 
        '''

        # contents can be various types: 
        # Text, Codes, Knowledge graphs, etc. now, we only consider natural language texts
        if (content_type == "TITLE"): 
            if (debug == 1): print (f"Right panel window add TITLE: {content}")
            window_title = tkinter.Label(self.main_editor_window_frame, text=content, font = [UI_config.standard_font_family, UI_config.h1_font_size, "bold"], 
                                            bg = color_tuple_to_rgb(UI_config.right_panel_color), fg = color_tuple_to_rgb(UI_config.VSCode_font_grey_color))
            window_title.pack (side = 'top', fill = 'x')
            self.window_elements.append(self.Window_Element(window_title, text_based_element = True, text_relwidth = 0.9, element_name = "Window Title"))
        elif (content_type == "INFORMATION"): 
            if (debug == 1): print (f"Right panel window add INFORMATION: {content}")
            window_info = tkinter.Label(self.main_editor_window_frame, text=content, 
                                            font = [UI_config.standard_font_family, UI_config.standard_font_size, "bold"], 
                                            bg = color_tuple_to_rgb(UI_config.right_panel_color), fg = color_tuple_to_rgb(UI_config.VSCode_font_grey_color))
            self.window_elements.append(self.Window_Element(window_info, text_based_element = True, text_relwidth = 0.9, element_name = "Window Info"))
        elif (content_type == "MESSAGE"): 
            from RTSAI.UI_funcs import measure_label_width, wrap_label_text
            from RTSAI.UI_Art import draw_message_callout
            from PIL import Image, ImageTk
            message_frame_width = 0.8 * self.winfo_width()
            message_frame = tkinter.Frame(self.main_editor_window_frame, bg = color_tuple_to_rgb(UI_config.right_panel_color))
            avatars_directory = f"{config.PACKAGE_PATH}/assets/images/avatars"

            '''
            Draw the avatar and keep some space between it and the message
            '''
            if (debug == 1): 
                if (sender == "USER"): print (f"Right panel window add USER MESSAGE: {content}")
                elif (sender == "RTSAI"): print (f"Right panel window add RTSAI MESSAGE: {content}")
            message_id = self.new_window_image_id()
            self.window_images[f"{self.winkey}|{message_id}:canvas"] = tkinter.Canvas(message_frame, width=UI_config.message_sender_icon_size + 6, height=UI_config.message_sender_icon_size + 6, 
                                                                                    bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightthickness=0)
            if (sender == "USER"): avatar_image = Image.open(f"{avatars_directory}/{self.user_avatar}")
            elif (sender == "RTSAI"): avatar_image = Image.open(f"{avatars_directory}/RTSAI_avatar.png")
            avatar_image_resized = avatar_image.resize((UI_config.message_sender_icon_size, UI_config.message_sender_icon_size))
            self.window_images[f"{self.winkey}|{message_id}:image"] = ImageTk.PhotoImage(avatar_image_resized)
            self.window_images[f"{self.winkey}|{message_id}:item"] = self.window_images[f"{self.winkey}|{message_id}:canvas"].create_image(3, 3, image=self.window_images[f"{self.winkey}|{message_id}:image"], anchor='nw')
            if (sender == "USER"): self.window_images[f"{self.winkey}|{message_id}:canvas"].pack(side = 'right')
            elif (sender == "RTSAI"): self.window_images[f"{self.winkey}|{message_id}:canvas"].pack(side = 'left')
            avatar_message_space_width = 10
            space_between_avatar_and_message = tkinter.Frame(message_frame, width = avatar_message_space_width, bg = color_tuple_to_rgb(UI_config.right_panel_color))
            if (sender == "USER"): space_between_avatar_and_message.pack(side = 'right', fill = 'y')
            elif (sender == "RTSAI"): space_between_avatar_and_message.pack(side = 'left', fill = 'y')

            '''
            Draw the message main body
            '''
            max_message_body_width = int(message_frame_width - (UI_config.message_sender_icon_size + 6) - avatar_message_space_width)
            message_body_canvas = tkinter.Canvas(message_frame, bg = color_tuple_to_rgb(UI_config.right_panel_color), width = max_message_body_width, highlightthickness = 0) # message_body_width
            if (sender == "USER"): message_body_label = tkinter.Label(message_body_canvas, text = content, bg = color_tuple_to_rgb(UI_config.avatar_message_box_color_list[self.user_avatar]), 
                                                font = (UI_config.standard_font_family, UI_config.standard_font_size), padx = 5)
            elif (sender == "RTSAI"): message_body_label = tkinter.Label(message_body_canvas, text = content, bg = color_tuple_to_rgb(UI_config.avatar_message_box_color_list["RTSAI_avatar.png"]), 
                                                font = (UI_config.standard_font_family, UI_config.standard_font_size), padx = 5)

            def adjust_message_label(message_sender): 
                '''
                Change the display label upon rendering
                '''

                message_frame_width = 0.8 * self.winfo_width()
                max_message_body_width = int(message_frame_width - (UI_config.message_sender_icon_size + 6) - avatar_message_space_width)

                # figure out how many rows the label should take
                def wrap_label_text_attempt(label_width_shrink = 2 * UI_config.message_callout_radius): 
                    message_body_label.configure(text = content)
                    label_width = measure_label_width(message_body_label)
                    if (debug == 0): print (f"message label width: {label_width} (max. {max_message_body_width - label_width_shrink})")
                    if (label_width < max_message_body_width - label_width_shrink): num_rows = 1; 
                    else: num_rows = math.ceil(label_width / (max_message_body_width - label_width_shrink)); 
                    message_body_label.configure(height = num_rows)
                    wrap_label_text(message_body_label, expected_width = max_message_body_width - label_width_shrink, text_align = tkinter.LEFT)

                    # find out the new width and new number of rows
                    # if num_rows is 1, force removing any newlines caused by wrapping
                    # otherwise, update num_rows based on the number of newline characters
                    message_body_label_text = message_body_label.cget("text")
                    if (num_rows == 1): message_body_label_text = message_body_label_text.replace('\n', '')
                    else: num_rows = message_body_label_text.count('\n') + 1
                    message_body_label_textlines = message_body_label_text.split('\n')
                    max_label_row_width = 0
                    for line in message_body_label_textlines: 
                        message_body_label.configure(text = line)
                        max_label_row_width = max(max_label_row_width, measure_label_width(message_body_label))
                    final_label_width = math.ceil(max_label_row_width / UI_config.label_width_ratio) + 0
                    final_label_rows = max(2, num_rows)
                    if (max_label_row_width <= max_message_body_width - 2 * UI_config.message_callout_radius): 
                        return (message_body_label_text, max_label_row_width, final_label_width, final_label_rows)
                    else: 
                        return (wrap_label_text_attempt(label_width_shrink + 20))

                message_body_label_text, max_label_row_width, final_label_width, final_label_rows = wrap_label_text_attempt()
                message_body_label.configure(text = message_body_label_text, width = final_label_width, height = final_label_rows)

                '''
                Lock the current frame and label size
                Draw the callout box
                '''
                message_body_width = max_label_row_width
                message_body_height = int(UI_config.standard_row_height_constant * final_label_rows + 10)
                message_body_canvas.configure(width = message_body_width + 2 * UI_config.message_callout_radius, height = message_body_height); 
                message_body_canvas.pack_propagate(False)
                message_frame.configure(width = message_frame_width, height = message_body_height)
                message_frame.pack_propagate(False)

                if (message_sender == "USER"): draw_message_callout(message_body_canvas, message_body_width + 2 * UI_config.message_callout_radius, 
                                    message_body_height, UI_config.message_callout_radius, fill = color_tuple_to_rgb(UI_config.avatar_message_box_color_list[self.user_avatar]))
                elif (message_sender == "RTSAI"): draw_message_callout(message_body_canvas, message_body_width + 2 * UI_config.message_callout_radius, 
                                    message_body_height, UI_config.message_callout_radius, fill = color_tuple_to_rgb(UI_config.avatar_message_box_color_list["RTSAI_avatar.png"]))
       
            if (sender == "USER"): message_body_canvas.pack(side = 'right')
            elif (sender == "RTSAI"): message_body_canvas.pack(side = 'left')

            ## TO BE COMPLETED: STILL NEED TO UPDATE THE LABEL WIDTH UPON WINDOW RESIZING
            message_frame.bind("<Configure>", lambda event: adjust_message_label(message_sender = sender))
            message_body_label.pack(anchor = 'center')

            if (sender == "USER"): self.window_elements.append(self.Window_Element(message_frame, anchor = 'ne', relwidth = 0.8, padx = 10, pady = UI_config.message_pady, element_name = f"User Message {message_id}"))
            elif (sender == "RTSAI"): self.window_elements.append(self.Window_Element(message_frame, anchor = 'nw', relwidth = 0.8, padx = 10, pady = UI_config.message_pady, element_name = f"RTSAI Message {message_id}"))

    def create_initial_window_elements(self): 
        '''
        Create the window components based on the window type
        '''

        if (debug == 0): print (f"Configure right panel main window ... {new_ID()}")

        self.window_elements = []
        self.main_editor_window = tkinter.Canvas(self, bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightthickness=0, relief='ridge')
        self.main_editor_window.pack(side = 'top', fill = 'both', expand = True)
        self.main_editor_window_frame = tkinter.Frame(self.main_editor_window, bg=color_tuple_to_rgb(UI_config.right_panel_color))
        self.main_editor_window_frame.pack (side = 'top', fill = 'x')
        
        if (self.wintype == "CRAWL"): 

            self.dialogue_box_hint_text = "Enter web URL ..."
            self.dialogue_box_error_text = "URL is not valid. Please enter the URL again ..."

            def web_crawl(dialogue_box): 
                '''
                Clear the crawl text box content, and get the URL from the box
                Crawl the URL, and create a knowledge graph with the crawl result
                '''

                import os
                request_url = dialogue_box.get("1.0", "end-1c")
                if (debug == 1): print (f"User request to crawl: {request_url}")

                '''
                Display the crawl request
                '''
                import validators
                def verify_url(url):
                    if validators.url(url): return url
                    elif validators.url('https://' + url): return ('https://' + url)
                    elif validators.url('http://' + url): return ('http://' + url)
                    else: return None
                expanded_url = verify_url(request_url)
                if expanded_url: 
                    if (debug == 1): print (f"Valid URL: {expanded_url}")
                    dialogue_box.delete("1.0", "end"); dialogue_box.master.focus_set() # lose dialogue box focus
                    dialogue_box.insert("1.0", self.dialogue_box_hint_text); dialogue_box.config(fg="gray") # fill the hint text
                else:
                    if (debug == 1): print (f"Invalid URL: {expanded_url}")
                    dialogue_box.delete("1.0", "end"); dialogue_box.master.focus_set() # lose dialogue box focus
                    dialogue_box.insert("1.0", self.dialogue_box_error_text); dialogue_box.config(fg="gray") # fill the error text
                dialogue_box_height = dialogue_box.tk.call((dialogue_box._w, "count", "-update", "-displaylines", "1.0", "end"))
                dialogue_box.configure(height = dialogue_box_height)

                '''
                Initialize a crawl request, and wait for the result
                '''
                if (expanded_url != None): 

                    '''
                    Add the corresponding message from USER to the web_crawl_main_panel_frame
                    '''
                    self.create_main_window_entry("USER", "MESSAGE", f"I want to crawl {expanded_url}")

                    

                    '''
                    Store the crawl result inside "web_crawl_{web_crawl_ID()}" knowledge graph
                    '''
                    from RTSAI.counter import web_crawl_ID
                    from RTSAI.UI_Left_Toggle_List import create_knowledge_graph_menu
                    from RTSAI.config import DATA_PATH
                    web_crawl_knowledge_graph_name = f"web_crawl_{web_crawl_ID()}"
                    while (os.path.exists(os.path.join(DATA_PATH, "Knowledge_graphs", web_crawl_knowledge_graph_name))): 
                        web_crawl_knowledge_graph_name = f"web_crawl_{web_crawl_ID()}"
                    create_knowledge_graph_menu(web_crawl_knowledge_graph_name, query = "Enter the name of the Knowledge Graph to store the crawl result: ")

                    '''
                    Add the corresponding message from RTSAI, saying that a knowledge graph has been created to store the result
                    '''
                
                else: 

                    '''
                    Add the corresponding message from RTSAI to the web_crawl_main_panel_frame
                    '''
                    self.create_main_window_entry("RTSAI", "MESSAGE", f"The URL {request_url} is not valid. Please enter the URL again. ")

                    pass
                    
            def file_upload(dialogue_box): 
                pass # TO BE COMPLETED
                # self.uploaded_files

            '''
            Generate the dialog box (including the upload and the crawl buttons) at the bottom
            The dialogue box is separated from the main_editor_window, staying at the bottom
            '''
            dialogue_box_panel = tkinter.Frame(self, bg=color_tuple_to_rgb(UI_config.grey_color_43))
            self.create_dialog_box(dialogue_box_panel, "Crawl", web_crawl, file_upload)
            dialogue_box_panel.pack(side='bottom', fill='x')

            '''
            Generate the main AI panel: The title, The introduction
            Note that more window entries (e.g., chats) will be generated with the same function self.create_main_window_entry, throughout the process
            '''
            self.create_main_window_entry(None, "TITLE", "Web Crawl")
            self.create_main_window_entry(None, "INFORMATION", "The web crawl function is designed to gather valuable data and construct a knowledge graph from the web, enabling the retrieval of useful information. ")

        elif (self.wintype == "TEXT"): 
            pass

    def configure_main_window(self): 
        '''
        Right_Panel_Main window configuration. 
        Update the element width, and render every element in the self.window_elements list
        '''
        
        self.width = self.winfo_width()
        if (debug == 1): print (f"Right panel window width: {self.width}")

        for window_element in self.window_elements: 
            if (window_element.relwidth != None): 
                if (self.width > 100): 
                    new_width = int(self.width * window_element.relwidth)
                    window_element.element.configure(width = new_width)
                    if (debug == 1): print (f"Configure Right Main Window: {window_element.element_name}'s new width: {new_width}")
            if (window_element.text_based_element == True): 
                self.window_element_wrap_text(window_element)

    def __init__(self, winkey, wintype): 

        super().__init__(master=UI_components.right_panel_main, bg=color_tuple_to_rgb(UI_config.right_panel_color))  # right_panel_main
        right_panel_main_bottom_arrow_area = tkinter.Canvas(self, height = UI_config.size_increase_arrow_height + 8 * UI_config.boundary_width, 
                                            bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightthickness = 0, relief='ridge')
        right_panel_main_bottom_arrow_area.pack(side="bottom", fill="x")
        self.winkey = winkey; self.wintype = wintype; self.status = "SAVED"
        self.width = 0; self.user_avatar = UI_config.user_avatar

        '''
        Save window operations. Allow restoration. 
        '''
        self.operations = []
        self.current_operation = -1

        '''
        Store window elements, and uploaded files (when applicable) 
        Bind the window with configuration event
        '''
        self.window_elements = []
        self.uploaded_files = []
        self.create_initial_window_elements() # pack them to the window & update self.window_elements list 
        self.bind("<Configure>", lambda event: self.configure_main_window())

        '''
        Store window images used
        '''
        self.window_image_id = 0; 
        self.window_images = dict()  # key: self.winkey|window_image_id

        '''
        No need to pack the window into the right panel
        Instead, we save it to the config list. 
        '''
        UI_components.editor_windows[winkey] = self
