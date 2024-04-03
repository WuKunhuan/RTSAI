
'''
Tasks: 
1. Import and Export functions
2. Revert the editing process. For key steps, define a function and have a space to store relevant files for recovery
3. Align Terminal and UI functions
4. Change the modify status area (remove it; replace it to the editor)
'''


import sys, os, shutil, re, math
import RTSAI.config as config
from RTSAI.config import EXECUTABLE_PATH, PACKAGE_PATH, DATA_PATH, ASSETS_PATH
from RTSAI.config import PRE_INSTALLED_KG, PRE_INSTALLED_KG_PATH
from RTSAI.config import COMMAND_NAME, DESKTOP_SIZE

'''
Debug purpose codes
'''
debug = 1
ID_counter = 0
def new_ID(): 
    global ID_counter; ID_counter += 1
    return ID_counter

resize_window_ID_counter = 0
def new_resize_window_ID(): 
    global resize_window_ID_counter; resize_window_ID_counter += 1
    return resize_window_ID_counter

def setup(): 
    '''
    RTSAI Package setup
    '''

    '''
    For MacOS: Remove .DS_Store
    '''
    os.system("find . -name '.DS_Store' -delete")

    '''
    Pre-installation of Knowledge Graph files
    '''
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        os.makedirs(os.path.join(DATA_PATH, "environments"))
        os.makedirs(os.path.join(DATA_PATH, "environments", config.CURRENT_ENV))
        knowledge_graphs_path = os.path.join(DATA_PATH, "knowledge_graphs")

        '''
        Copy pre-installed Knowledge Graphs to the "knowledge_graphs" folder
        '''
        for graph_name in PRE_INSTALLED_KG:
            src_dir = os.path.join(PRE_INSTALLED_KG_PATH, graph_name)
            dst_dir = os.path.join(knowledge_graphs_path, graph_name)
            shutil.copytree(src_dir, dst_dir)

def color_tuple_to_rgb (color_tuple): 
    '''
    Convert color tuples to rgb string
    '''
    return ("#%02x%02x%02x" % color_tuple)

def show_popup_message(message, title = "Message", parent_item = None):
    import tkinter
    tkinter.messagebox.showinfo(title, message, parent = parent_item)

def new_name_check(name, path = DATA_PATH, showinfo = "print", keyword = "", max_length = 30, parent_item = None): 
    '''
    Check whether creating a file/folder with the name under the path is valid
    '''
    if os.path.exists(os.path.join(path, name)): 
        if (showinfo == "print"): print(f"{keyword} Name '{name}' already exists.")
        else: show_popup_message(f"{keyword} '{name}' already exists.", parent_item = parent_item)
    elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name): 
        if (len(name) <= max_length): return 0
        else: 
            if (showinfo == "print"): print(f"{keyword} Name '{name}' too long (max. 30 characters).")
            else: show_popup_message(f"{keyword} '{name}' too long (max. 30 characters).", parent_item = parent_item)
    else: 
        if (showinfo == "print"): print(f"Invalid {keyword} Name '{name}'. Please follow the rules for Python identifiers.")
        else: show_popup_message(f"Invalid {keyword} Name '{name}'. Please follow the rules for Python identifiers.", parent_item = parent_item)
    return 1

def create_environment(environment_name, previous_environment_name = None, showinfo = "print", parent_item = None):
    '''
    Create a new environment folder with the given name. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        environment_path = os.path.join(DATA_PATH, "environments", environment_name)
        if previous_environment_name and os.path.exists(os.path.join(DATA_PATH, "environments", previous_environment_name)):
            previous_environment_path = os.path.join(DATA_PATH, "environments", previous_environment_name)
            os.rename(previous_environment_path, environment_path)
            return 0
        else: os.makedirs(environment_path); return 0
    except: return 1

def copy_environment(existing_environment_name, copied_environment_name, showinfo = "print", parent_item = None):
    '''
    Copy an existing environment to create a new environment. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        environment_path = os.path.join(DATA_PATH, "environments")
        if not os.path.exists(os.path.join(environment_path, existing_environment_name)): 
            if (showinfo == "print"): print(f"Environment '{existing_environment_name}' does not exist.")
            else: show_popup_message(f"Environment '{existing_environment_name}' does not exist.", parent = parent_item)
            return 1
        print (os.path.join(environment_path, existing_environment_name))
        print (os.path.join(environment_path, copied_environment_name))
        shutil.copytree(os.path.join(environment_path, existing_environment_name), os.path.join(environment_path, copied_environment_name))
        return 0
    except: return 1

def create_knowledge_graph(graph_name, previous_graph_name = None, showinfo = "print", parent_item = None):
    '''
    Create or rename a Knowledge Graph. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        graph_path = os.path.join(DATA_PATH, "knowledge_graphs", graph_name)
        if previous_graph_name:
            previous_graph_path = os.path.join(DATA_PATH, "knowledge_graphs", previous_graph_name)
            if (os.path.exists(previous_graph_path)): 
                os.rename(previous_graph_path, graph_path)
                return 0
            else: 
                if (showinfo == "print"): print(f"Knowledge Graph '{previous_graph_name}' does not exist.")
                else: show_popup_message(f"Knowledge Graph '{previous_graph_name}' does not exist.", parent = parent_item)
                return 1
        else: 
            template_path = os.path.join(ASSETS_PATH, "templates", "template_knowledge_graph")
            shutil.copytree(template_path, graph_path)
            return 0
    except: return 1

def copy_knowledge_graph(existing_graph_name, copied_graph_name, environment_name = None, showinfo = "print", parent_item = None): 
    '''
    Copy an Knowledge Graph. 
    Before this function, necessary name checking should be performed. 
    '''
    if (environment_name): graph_path = os.path.join(DATA_PATH, "environments", environment_name)
    else: graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
    if not os.path.exists(os.path.join(graph_path, existing_graph_name)):
        if (showinfo == "print"): 
            if (environment_name): 
                print(f"Knowledge Graph '{existing_graph_name}' does not exist inside Environment '{environment_name}'. ")
            else: 
                print(f"Knowledge Graph '{existing_graph_name}' does not exist." )
        else: 
            if (environment_name): 
                show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist inside Environment '{environment_name}'. ", parent = parent_item)
            else: 
                show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist.", parent = parent_item)
        return 1
    elif os.path.exists(os.path.join(graph_path, copied_graph_name)):
        if (showinfo == "print"): 
            if (environment_name): 
                print(f"Knowledge Graph '{copied_graph_name}' already exists inside Environment '{environment_name}'. ")
            else: 
                print(f"Knowledge Graph '{copied_graph_name}' already exists." )
        else: 
            if (environment_name): 
                show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists inside Environment '{environment_name}'. ", parent = parent_item)
            else: 
                show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists.", parent = parent_item)
        return 1
    elif (new_name_check(copied_graph_name, graph_path, showinfo = showinfo, parent_item = parent_item) == 0): 
        shutil.copytree(os.path.join(graph_path, existing_graph_name), os.path.join(graph_path, copied_graph_name))
        return 0

def environment_add_knowledge_graphs(environment_name, graph_names, showinfo = "print", parent_item = None): 
    '''
    Add Knowledge Graphs to the specified environment. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        imported_knowledge_graphs = []
        for graph_name in graph_names: 
            graph_src_path = os.path.join(DATA_PATH, "knowledge_graphs")
            graph_dst_path = os.path.join(DATA_PATH, "environments", environment_name)
            if not os.path.exists(graph_src_path): 
                if (showinfo == "print"): print(f"Knowledge Graph '{graph_name}' does not exist."); continue
                else: show_popup_message(f"Knowledge Graph '{graph_name}' does not exist.", parent = parent_item); continue
            if (new_name_check(graph_name, graph_dst_path, showinfo, "Knowledge Graph", parent_item = parent_item) == 0): 
                shutil.copytree(os.path.join(graph_src_path, graph_name), os.path.join(graph_dst_path, graph_name))
                imported_knowledge_graphs.append(graph_name)
        return imported_knowledge_graphs
    except: return imported_knowledge_graphs

def environment_rename_knowledge_graph(environment_name, graph_name, previous_graph_name, showinfo = "print", parent_item = None): 
    '''
    Rename a Knowledge Graph inside an environment. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        graph_path = os.path.join(DATA_PATH, "environments", environment_name)
        if not os.path.exists(os.path.join(graph_path, previous_graph_name)): 
            if (showinfo == "print"): print(f"Knowledge Graph '{graph_name}' does not exist in the Environment '{environment_name}'."); 
            else: show_popup_message(f"Knowledge Graph '{graph_name}' does not exist in the Environment '{environment_name}'.", parent = parent_item); 
            return 1
        elif (new_name_check(graph_name, graph_path, showinfo, "Knowledge Graph", parent_item = parent_item) == 0): 
            shutil.move(os.path.join(graph_path, previous_graph_name), os.path.join(graph_path, graph_name))
            return 0
    except: return 1

def main(): 
    '''
    The main function handling both the UI and the Terminal Application
    '''

    print  (sys.argv[0])
    
    if (not (len(sys.argv) >= 1 and sys.argv[0] == f'{EXECUTABLE_PATH}/{COMMAND_NAME}')): 
        return

    '''
    Run setup codes
    '''
    setup()

    if (len(sys.argv) == 1): 

        '''
        Create the RTSAI graphical window
        '''
        import tkinter
        from tkinter import simpledialog, Scrollbar, Listbox, messagebox
        from tkinter.font import Font
        from PIL import Image, ImageTk

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

        class Left_Panel_Toggle_Item(tkinter.Frame): 
            '''
            Toggle Item class objects in the left panel main
            '''

            def configure_canvas_modify(self, event): 
                '''
                Generates the modify sign. 
                '''
                canvas_width = config.toggle_modify_width
                canvas_height = config.toggle_modify_height
                self.toggle_item_modify.delete("modify")
                self.toggle_item_modify.config(width=canvas_width, height=canvas_height)
                self.toggle_item_modify.create_oval(canvas_width * 0.25, canvas_height * 0.25, canvas_height * 0.75, canvas_height * 0.75, fill=color_tuple_to_rgb(config.grey_color_64), tags="modify", outline = color_tuple_to_rgb(config.left_panel_color))

            def modify_toggle_item(self, event, key_pressed = None): 
                '''
                Display the menu when right clicking the toggle item. 
                '''
                if (key_pressed == "<BackSpace>" and ((self.toggle_info[1] != config.toggle_item_on_focus) or ('/' not in self.toggle_info[1]))): return

                self.menu_open = True
                if (self.toggle_info[1] == "environments"): 
                    '''
                    Environment toggle item
                    '''
                    def create_environment_menu(): 
                        '''
                        Create a new Environment
                        '''
                        environment_name = simpledialog.askstring("Create Environment", "Enter the name of the environment: ", parent = self)
                        if environment_name:
                            environment_path = os.path.join(DATA_PATH, "environments")
                            if (new_name_check(environment_name, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                                create_environment(environment_name)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Environment '{environment_name}' successfully created.", parent_item = self)
                    
                    def import_environment(): 
                        '''
                        Import a new Environment
                        '''
                        pass

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Create an Environment", command = create_environment_menu)
                    modify_menu_list.add_command(label="Import an Environment (to be completed)", command = import_environment)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1].startswith("environments") and self.toggle_info[1].count('/') == 1): 
                    '''
                    Environment's Knowledge Graph toggle item
                    '''
                    environment_name = self.toggle_info[1].split('/')[1]

                    def rename_environment(): 
                        '''
                        Rename the Environment
                        '''
                        environment_name_new = simpledialog.askstring("Rename Environment", f"Enter the new name of the Environment '{environment_name}': ", parent = self)
                        if environment_name_new:
                            environment_path = os.path.join(DATA_PATH, "environments")
                            if (new_name_check(environment_name_new, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                                if (create_environment(environment_name_new, environment_name, showinfo="messagebox") == 0): 
                                    if (environment_name == config.CURRENT_ENV): 
                                        config.CURRENT_ENV = environment_name_new
                                    config.toggle_list_created = False; create_toggle_list()
                                    show_popup_message(f"Environment '{environment_name}' successfully renamed to '{environment_name_new}'.", parent_item = self.toggle_item_modify)
                                else: show_popup_message(f"Environment '{environment_name}' rename FAILED.", parent_item = self.toggle_item_modify)

                    def delete_environment(): 
                        '''
                        Delete the Environment
                        '''
                        if environment_name == config.CURRENT_ENV:
                            messagebox.showwarning("Cannot Delete", "Cannot delete the Current Environment.", parent = self)
                        else:
                            confirm = messagebox.askyesno("Confirm Environment Deletion", f"Are you sure you want to delete the Environment '{environment_name}'?", parent = self)
                            if confirm:
                                environment_path = os.path.join(DATA_PATH, "environments")
                                try:
                                    shutil.rmtree(os.path.join(environment_path, environment_name))
                                    config.toggle_list_created = False; create_toggle_list()
                                    show_popup_message(f"Environment '{environment_name}' successfully deleted.", parent_item = self)
                                except OSError:
                                    messagebox.showerror("Environment Deletion Failed", f"Environment '{environment_name}' deletion FAILED.", parent = self)

                    def copy_environment_menu(): 
                        '''
                        Copy the Environment
                        '''
                        environment_name_new = simpledialog.askstring("Copy Environment", f"Enter the copy name of the Environment '{environment_name}': ", parent = self)
                        if environment_name_new:
                            environment_path = os.path.join(DATA_PATH, "environments")
                            if (new_name_check(environment_name_new, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                                copy_environment(environment_name, environment_name_new, showinfo="messagebox")
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Environment '{environment_name}' successfully copied as '{environment_name_new}'.", parent_item = self)

                    def set_as_current_environment(): 
                        '''
                        Set the Environment as the Current Environment
                        '''
                        config.CURRENT_ENV = environment_name
                        config.toggle_list_created = False; create_toggle_list()
                        show_popup_message(f"Environment '{environment_name}' successfully set as the Current Environment.", parent_item = self)

                    def add_knowledge_graphs(): 
                        '''
                        Add Knowledge Graphs to the Environment
                        '''
                        select_knowledge_graph_window = tkinter.Toplevel(self)
                        select_knowledge_graph_window.title(f"Select Knowledge Graphs for the Environment '{environment_name}'")
                        select_knowledge_graph_window.resizable(width = False, height = False)
                        knowledge_graph_names = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs")) 
                        knowledge_graph_names.sort (key = lambda name: name.lower())
                        knowledge_graph_names_current = os.listdir(os.path.join(DATA_PATH, self.toggle_info[1])) 
                        knowledge_graph_names = [name for name in knowledge_graph_names if name not in knowledge_graph_names_current]
                        knowledge_graph_list = None

                        if (not knowledge_graph_names): select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"No Knowledge Graphs are available! ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10); return

                        if (len(knowledge_graph_names) > 12): 
                            select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. \nPlease scroll down to see the full list ({len(knowledge_graph_names)} items). ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                            select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                        else: 
                            select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                            select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                        
                        select_knowledge_graph_frame = tkinter.Frame(select_knowledge_graph_window, bg = color_tuple_to_rgb(config.left_panel_color))
                        select_knowledge_graph_frame.pack(side = "top", anchor = "n", fill = "both", padx = 10, pady = 0)
                        knowledge_graph_list = Listbox(select_knowledge_graph_frame, selectmode = "multiple", 
                                                    bg = color_tuple_to_rgb(config.left_panel_color), 
                                                    fg = color_tuple_to_rgb(config.VSCode_font_grey_color), 
                                                    selectbackground = color_tuple_to_rgb(config.VSCode_highlight_color), 
                                                    selectforeground = color_tuple_to_rgb(config.left_panel_color), 
                                                    font = (config.standard_font_family, config.standard_font_size), 
                                                    height = min(len(knowledge_graph_names), 12), activestyle='none')
                        for knowledge_graph_name in knowledge_graph_names: knowledge_graph_list.insert("end", f"{knowledge_graph_name}")
                        if (len(knowledge_graph_names) > 12): 
                            select_knowledge_graph_window.geometry(f'600x300+{max(event.x_root-300, 0)}+{max(event.y_root-150, 0)}')
                        else: 
                            select_knowledge_graph_window.geometry(f'600x{int((292-12*16.8)+16.8*len(knowledge_graph_names))}+{max(event.x_root-300, 0)}+{max(int(event.y_root-(84+18*len(knowledge_graph_names))/2), 0)}')
                        knowledge_graph_list.pack(fill='x', expand=True)
                            
                        '''
                        Cancel and OK buttons
                        '''
                        button_frame = tkinter.Frame (select_knowledge_graph_window)
                        button_frame.pack (side = 'top', fill = 'x', expand = True)
                        def select_knowledge_graph_cancel(event): 
                            select_knowledge_graph_window.destroy()
                            select_knowledge_graph_window.update()
                        def select_knowledge_graph_OK(event): 
                            selected_items = [knowledge_graph_names[item] for item in knowledge_graph_list.curselection()]
                            success_items = environment_add_knowledge_graphs(environment_name, selected_items)
                            select_knowledge_graph_window.destroy()
                            select_knowledge_graph_window.update()
                            config.toggle_list_created = False; create_toggle_list()
                            temp_string = ', '.join([f"'{item}'" for item in success_items]) # fit python 3.9 version
                            show_popup_message (f"Knowledge Graphs {temp_string} successfully added to the Environment '{environment_name}'.")
                        if (knowledge_graph_names): 
                            Cancel_button = tkinter.Button(button_frame, text = "Cancel")
                            Cancel_button.pack (side = 'left', padx = 100)
                            Cancel_button.bind("<Button-1>", lambda event: select_knowledge_graph_cancel (event))
                            OK_button = tkinter.Button(button_frame, text = "OK")
                            OK_button.pack (side = 'right', padx = 100)
                            OK_button.bind("<Button-1>", lambda event: select_knowledge_graph_OK (event))
                        else: 
                            Cancel_button = tkinter.Button(button_frame, text = "Cancel")
                            Cancel_button.pack (side = 'top')
                            Cancel_button.bind("<Button-1>", lambda event: select_knowledge_graph_cancel (event))

                    def export_environment(): 
                        '''
                        Export the whole environment as a Zip file
                        '''
                        pass

                    if (key_pressed == "<BackSpace>"): delete_environment(); return
                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label=f"Rename the Environment '{environment_name}'", command = rename_environment)
                    modify_menu_list.add_command(label=f"Delete the Environment '{environment_name}'", command = delete_environment)
                    modify_menu_list.add_command(label=f"Copy the Environment '{environment_name}'", command = copy_environment_menu)
                    modify_menu_list.add_command(label=f"Set '{environment_name}' as the Current Environment", command = set_as_current_environment)
                    modify_menu_list.add_command(label=f"Add Knowledge Graphs to the Environment '{environment_name}'", command = add_knowledge_graphs)
                    modify_menu_list.add_command(label=f"Export the Environment '{environment_name}' (to be completed)", command = export_environment)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1].startswith("environments") and self.toggle_info[1].count('/') == 2): 

                    environment_name = self.toggle_info[1].split('/')[1]
                    knowledge_graph_name = self.toggle_info[1].split('/')[2]

                    def rename_knowledge_graph(): 
                        '''
                        Rename the Knowledge Graph inside an environment
                        '''
                        knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the new name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                        if knowledge_graph_name_new:
                            if (environment_rename_knowledge_graph(environment_name, knowledge_graph_name_new, knowledge_graph_name, showinfo = "messagebox", parent_item = self) == 0): 
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}' inside Environment '{environment_name}'.", parent_item = self)

                    def delete_knowledge_graph(): 
                        '''
                        Delete the Knowledge Graph inside an environment
                        '''
                        confirm = messagebox.askyesno("Confirm Knowledge Graph Deletion", f"Are you sure you want to delete the Knowledge Graph '{knowledge_graph_name}'?", parent = self)
                        if confirm:
                            knowledge_graph_path = os.path.join(DATA_PATH, "environments", environment_name, knowledge_graph_name)
                            try:
                                shutil.rmtree(knowledge_graph_path)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' inside Environment {environment_name} successfully deleted.", parent_item = self)
                            except OSError:
                                messagebox.showerror("Knowledge Graph Deletion Failed", f"Knowledge Graph '{knowledge_graph_name}' inside Environment '{environment_name}' deletion FAILED.", parent = self)

                    def copy_knowledge_graph_menu(): 
                        '''
                        Copy the Knowledge Graph inside an environment
                        '''
                        knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the copy name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                        if knowledge_graph_name_new:
                            knowledge_graph_path = os.path.join(DATA_PATH, "environments", environment_name)
                            if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                                if (copy_knowledge_graph(knowledge_graph_name, knowledge_graph_name_new, environment_name, showinfo="messagebox", parent_item = self) == 0): 
                                    config.toggle_list_created = False; create_toggle_list()
                                    show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully copied as '{knowledge_graph_name_new}'.", parent_item = self)
                                else: show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' copy FAILED.", parent_item = self)

                    def save_to_knowledge_graph(): 
                        '''
                        Save the Knowledge Graph to the Knowledge Graph folder
                        '''
                        knowledge_graph_export_path = os.path.join(DATA_PATH, "knowledge_graphs")
                        if (new_name_check(knowledge_graph_name, knowledge_graph_export_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                            shutil.copytree(os.path.join(DATA_PATH, "environments", environment_name, knowledge_graph_name), os.path.join(knowledge_graph_export_path, knowledge_graph_name))
                            config.toggle_list_created = False; create_toggle_list()
                            show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully saved to the Knowledge Graph folder.", parent_item = self)

                    if (key_pressed == "<BackSpace>"): delete_knowledge_graph(); return
                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label=f"Rename the Knowledge Graph '{knowledge_graph_name}'", command = rename_knowledge_graph)
                    modify_menu_list.add_command(label=f"Delete the Knowledge Graph '{knowledge_graph_name}'", command = delete_knowledge_graph)
                    modify_menu_list.add_command(label=f"Copy the Knowledge Graph '{knowledge_graph_name}'", command = copy_knowledge_graph_menu)
                    modify_menu_list.add_command(label=f"Save the Knowledge Graph '{knowledge_graph_name}'", command = save_to_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1] == "knowledge_graphs"): 
                    '''
                    Knowledge graph folder toggle item
                    '''
                    def create_knowledge_graph_menu(): 
                        '''
                        Create a knowledge graph from the menu. 
                        '''
                        graph_name = simpledialog.askstring("Create Knowledge Graph", "Enter the name of the Knowledge Graph: ", parent = self)
                        if graph_name:
                            graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
                            if (new_name_check(graph_name, graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                                create_knowledge_graph(graph_name)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{graph_name}' successfully created.", parent_item = self)
                    
                    def import_knowledge_graph(): 
                        '''
                        '''
                        pass

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Create a Knowledge Graph", command = create_knowledge_graph_menu)
                    modify_menu_list.add_command(label="Import a Knowledge Graph (to be completed)", command = import_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)
                
                elif (self.toggle_info[1].startswith("knowledge_graphs") and self.toggle_info[1].count('/') == 1): 
                    '''
                    Single Knowledge Graph toggle item
                    '''
                    knowledge_graph_name = self.toggle_info[1].split('/')[1]

                    def rename_knowledge_graph(): 
                        '''
                        Rename the Knowledge Graph
                        '''
                        knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the new name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                        if knowledge_graph_name_new:
                            knowledge_graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
                            if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                                if (create_knowledge_graph(knowledge_graph_name_new, knowledge_graph_name, showinfo="messagebox") == 0): 
                                    config.toggle_list_created = False; create_toggle_list()
                                    show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}'.", parent_item = self)
                            else: show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' rename FAILED.", parent_item = self)

                    def delete_knowledge_graph(): 
                        '''
                        Delete the Knowledge Graph
                        '''
                        confirm = messagebox.askyesno("Confirm Knowledge Graph Deletion", f"Are you sure you want to delete the Knowledge Graph '{knowledge_graph_name}'?", parent = self)
                        if confirm:
                            knowledge_graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
                            try:
                                shutil.rmtree(os.path.join(knowledge_graph_path, knowledge_graph_name))
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully deleted.", parent_item = self)
                            except OSError:
                                messagebox.showerror("Knowledge Graph Deletion Failed", f"Knowledge Graph '{knowledge_graph_name}' deletion FAILED.", parent = self)

                    def copy_knowledge_graph_menu(): 
                        '''
                        Copy the Knowledge Graph
                        '''
                        knowledge_graph_name_new = simpledialog.askstring("Copy Knowledge Graph", f"Enter the copy name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                        if knowledge_graph_name_new:
                            knowledge_graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
                            if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                                copy_knowledge_graph(knowledge_graph_name, knowledge_graph_name_new, showinfo="messagebox", parent_item = self)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully copied as '{knowledge_graph_name_new}'.", parent_item = self)

                    def export_knowledge_graph(): 
                        '''
                        Export the Knowledge Graph as a zip file
                        '''
                        pass

                    if (key_pressed == "<BackSpace>"): delete_knowledge_graph(); return
                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label=f"Rename the Knowledge Graph '{knowledge_graph_name}'", command = rename_knowledge_graph)
                    modify_menu_list.add_command(label=f"Delete the Knowledge Graph '{knowledge_graph_name}'", command = delete_knowledge_graph)
                    modify_menu_list.add_command(label=f"Copy the Knowledge Graph '{knowledge_graph_name}'", command = copy_knowledge_graph_menu)
                    modify_menu_list.add_command(label=f"Export the Knowledge Grpah '{knowledge_graph_name}' (to be completed)", command = export_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)
                
                self.menu_open = False

            def click_toggle_item(self, event): 
                '''
                Click the item and change the focus
                '''

                self.toggle_info[2][0] = not self.toggle_info[2][0]
                '''
                Bind BackSpace to delete the current Environment / Knowledge Graph
                Bind Command + Z (MAC SYSTEM) to revert; Bind Command + Shift + Z
                TO BE COMPLETED
                '''
                self.bind("<BackSpace>", lambda event: self.modify_toggle_item(event, key_pressed = "<BackSpace>"))
                '''
                Set the current focus to Toggle List -> Current Item
                '''
                self.focus_set()
                if (config.toggle_item_on_focus == self.toggle_info[1]): 
                    config.toggle_list_created = False; create_toggle_list()
                    self.modify_toggle_item(event)
                else: 
                    config.toggle_item_on_focus = self.toggle_info[1]
                    config.toggle_list_created = False; create_toggle_list()
                    if (debug == 1): print (f"Change focus to {self.toggle_info[1]}")

            def __init__(self, master, toggle_display_name, toggle_info, bold=False):

                super().__init__(master, bg=color_tuple_to_rgb(config.left_panel_color))
                self.pack_propagate(False)
                self.toggle_info = toggle_info
                self.menu_open = False
                self.label = tkinter.Label(self, text=toggle_display_name, font=(config.standard_font_family, config.standard_font_size, "bold" if bold else "normal"), anchor = "w", 
                                    fg=color_tuple_to_rgb(config.VSCode_font_grey_color), bg=color_tuple_to_rgb(config.left_panel_color), 
                                    relief="flat", borderwidth=0)
                if (self.toggle_info[1].startswith("knowledge_graphs") or (self.toggle_info[1].startswith("environments"))): 
                    self.toggle_item_modify = tkinter.Canvas(self, width=config.toggle_modify_width, height=config.toggle_modify_height, 
                                                bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge')
                    self.toggle_item_modify.pack (side = 'right', padx = 0, pady = 0)
                    self.toggle_item_modify.bind('<Configure>', self.configure_canvas_modify)
                    self.toggle_item_modify.bind("<Button-1>", self.modify_toggle_item)

                self.label.pack (side = "top", fill = "x")
                if (config.toggle_item_on_focus == self.toggle_info[1]): 
                    self.configure(bg=color_tuple_to_rgb(config.grey_color_51))
                    self.label.configure(bg=color_tuple_to_rgb(config.grey_color_51))
                    if (self.toggle_info[1].startswith("knowledge_graphs") or self.toggle_info[1].startswith("environments")): 
                        self.toggle_item_modify.configure(bg=color_tuple_to_rgb(config.grey_color_51))

                self.configure(height=config.toggle_item_height, width=config.left_panel_width - config.left_panel_sidebar_width)
                self.bind("<Button-1>", self.click_toggle_item)
                self.label.bind("<Button-1>", self.click_toggle_item)

                '''
                WARNING Some platforms may use Button-3 instead
                TO BE COMPLETED / VERIFIED
                '''
                if (True): 
                    self.bind("<Button-2>", self.modify_toggle_item)
                    self.label.bind("<Button-2>", self.modify_toggle_item)
                    self.toggle_item_modify.bind("<Button-2>", self.modify_toggle_item)

        class Right_Panel_Tab(tkinter.Frame): 
            '''
            The editor tabs inside the tab bar
            '''

            def draw_tab_icon_status(self): 
                '''
                Draw tab icon and status
                '''

                canvas_width = config.right_panel_tabbar_height - self.active_bar_thickness; 
                canvas_height = config.right_panel_tabbar_height - self.active_bar_thickness; 
                self.tab_status.delete("tab_status_indicator")
                '''
                Draw tab icon
                '''
                if (self.tab_type == "CHAT"): draw_chat_icon(self.tab_icon, color_tuple_to_rgb(config.chat_icon_color))
                elif (self.tab_type == "CRAWL"): draw_crawl_icon(self.tab_icon, color_tuple_to_rgb(config.crawl_icon_color))
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
                    config.tabbar_created = False; show_tabbar()

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
                    config.tabbar_created = False; show_tabbar()
                else: hide_tabbar()

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
                self.tab_label = tkinter.Label(self, text = tab_display_name, font = self.font, 
                                            fg = color_tuple_to_rgb(config.VSCode_font_grey_color))
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

        '''
        CURRENT
        The main window of right panel
        '''
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
                print (new_resize_window_ID())
        
            def __init__(self, winkey, wintype): 

                print  (f"Right_Panel_Main_Window init ...")

                print  (f"new_resize_window_ID: {new_resize_window_ID()}")

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
                config.main_windows[winkey] = self

        def check_editor_status (source_file): 
            opened_editors = [editor[0] for editor in config.editor_states]
            if (source_file not in opened_editors): return None
            else: return (config.editor_states[opened_editors.index(source_file)][1])

        '''
        Draw the icons for chat & web crawling
        '''
        def draw_chat_icon(parent_canvas, fill = color_tuple_to_rgb(config.VSCode_font_grey_color)): 
            '''
            Draw the chat logo
            '''
            canvas_width = parent_canvas.winfo_width()
            canvas_height = parent_canvas.winfo_height()
            parent_canvas.delete("item_1_rectangle")
            parent_canvas.delete("item_2_triangle")
            def round_rectangle_points(x1, y1, x2, y2, radius): 
                return([
                    x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
                    x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                    x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                    x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                    x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
                ])
            item_1_rectangle_coords = round_rectangle_points(0.2 * canvas_width, 0.2 * canvas_height, 0.8 * canvas_width, 0.6 * canvas_height, 0.2 * canvas_height)
            item_2_triangle_coords = [
                canvas_width * 0.35, canvas_height * 0.6,
                canvas_width * 0.3, canvas_height * 0.75,
                canvas_width * 0.5, canvas_height * 0.6, 
            ]
            parent_canvas.create_polygon(item_1_rectangle_coords, fill = fill, tags="item_1_rectangle", smooth=True, outline = "")
            parent_canvas.create_polygon(item_2_triangle_coords, fill = fill, tags="item_2_triangle", outline = "")
            parent_canvas.items_in_panel = ["item_1_rectangle", "item_2_triangle"]

        def draw_crawl_icon(parent_canvas, fill = color_tuple_to_rgb(config.VSCode_font_grey_color)): 
            '''
            Draw the web crawl logo
            '''
            canvas_width = parent_canvas.winfo_width()
            canvas_height = parent_canvas.winfo_height()
            parent_canvas.delete("item_1_spider_body")
            parent_canvas.delete("item_8_spider_head")
            parent_canvas.delete("item_2_spider_leg_1")
            parent_canvas.delete("item_3_spider_leg_2")
            parent_canvas.delete("item_4_spider_leg_3")
            parent_canvas.delete("item_5_spider_leg_4")
            parent_canvas.delete("item_6_spider_leg_5")
            parent_canvas.delete("item_7_spider_leg_6")

            def spider_leg_points(x, y, x_first_joint, y_first_joint, thickness):
                return [
                    x, y - thickness / 2, 
                    x, y + thickness / 2, 
                    x_first_joint, y_first_joint + thickness / 2, 
                    2 * x_first_joint - x, 3 * y_first_joint - 2 * y + thickness / 2, 
                    2 * x_first_joint - x, 3 * y_first_joint - 2 * y - thickness / 2, 
                    x_first_joint, y_first_joint - thickness / 2, 
                ]
            
            parent_canvas.create_oval(0.3 * canvas_width, 0.3 * canvas_height, 0.7 * canvas_width, 0.7 * canvas_height, fill=fill, tags="item_1_spider_body", outline = "")
            parent_canvas.create_oval(0.4 * canvas_width, 0.2 * canvas_height, 0.6 * canvas_width, 0.4 * canvas_height, fill=fill, tags="item_8_spider_head", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.4 * canvas_height, 0.27 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_2_spider_leg_1", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.5 * canvas_height, 0.27 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=fill, tags="item_3_spider_leg_2", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.6 * canvas_height, 0.27 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_4_spider_leg_3", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.4 * canvas_height, 0.73 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_5_spider_leg_4", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.5 * canvas_height, 0.73 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=fill, tags="item_6_spider_leg_5", outline = "")
            parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.6 * canvas_height, 0.73 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_7_spider_leg_6", outline = "")
            parent_canvas.items_in_panel = ["item_1_spider_body", "item_8_spider_head", "item_2_spider_leg_1", "item_3_spider_leg_2", "item_4_spider_leg_3", "item_5_spider_leg_4", "item_6_spider_leg_5", "item_7_spider_leg_6"]

        def wrap_label_text(parent_label, expected_row_width, label_text_original = None): 
            '''
            Rendering the label_text, by adding necessary newline characters
            '''

            # Calculate the expected row width
            font = Font(font=parent_label.cget("font"))
            if (not label_text_original): 
                label_text_original = parent_label.cget("text")
            remaining_text = label_text_original
            rendered_text = ""

            while remaining_text: 

                remaining_width = font.measure(remaining_text)
                remaining_density = remaining_width / len(remaining_text)
                total_characters = min(len(remaining_text), math.floor(expected_row_width / remaining_width * len(remaining_text)))
                cropped_text = remaining_text[0:total_characters]

                if (total_characters != len(remaining_text)): 
                    # diff_char_nums can either be positive (need more characters) or negative
                    diff_char_nums = math.floor((expected_row_width - font.measure(cropped_text)) / remaining_density)
                    while (abs(diff_char_nums) > 3): # let us fix the error threshold to be 3
                        print (diff_char_nums)
                        total_characters += diff_char_nums
                        cropped_text = remaining_text[0:total_characters]
                        remaining_density = remaining_width / len(remaining_text)
                        diff_char_nums = math.floor((expected_row_width - font.measure(cropped_text)) / remaining_density)

                # Check if the next character is not a space to avoid breaking words
                if total_characters < len(remaining_text) and remaining_text[total_characters] != ' ':
                    last_space_index = cropped_text.rfind(' ')
                    if last_space_index != -1:
                        cropped_text = cropped_text[:last_space_index + 1]
                        total_characters = last_space_index + 1

                # Add the cropped text to the rendered text with a newline character
                # Skip multiple new line characters
                if (not (rendered_text.endswith('\n\n') and cropped_text == '\n')): 
                    rendered_text += cropped_text + '\n'
                remaining_text = remaining_text[total_characters:]

            '''
            Finalize the label text
            '''
            parent_label.configure(text=rendered_text.rstrip())
            parent_label.configure(width=expected_row_width)

        def resize_window(): 
            '''
            Resizes the main window. 
            Toggle lists, etc. will be rendered again when appropriate. 
            '''
            # if (config.current_editor): 
            #     config.current_editor.pack_forget()

            window_geometry = list(map(int, config.window.geometry().replace('x', ' ').replace('+', ' ').split(' ')))
            config.window_width = window_geometry[0]
            config.window_height = window_geometry[1]

            left_panel_width = int(config.left_panel_relwidth * config.window_width)
            if (config.window_width >= config.window_width_min and left_panel_width < config.left_panel_width_min): 
                left_panel_width = config.left_panel_width_min; 
                config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                left_panel_width = int(config.left_panel_relwidth * config.window_width)

            config.left_panel_width = left_panel_width
            config.left_panel.configure (width = config.left_panel_width, height = config.window_height)
            config.left_panel_sidebar.configure (width = config.left_panel_sidebar_width)
            config.toggle_list.configure (width = config.left_panel_width - config.left_panel_sidebar_width)
            config.right_panel.configure (height = config.window_height)
            config.left_panel_change_arrow.place(x = config.left_panel_width - 3 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tkinter.SE)
            config.right_panel_change_arrow.place(x = 1 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tkinter.SW)

            # TO BE VERIFIED: WHETHER I CAN REMOVE THE LINE
            # create_toggle_list()

        def show_tabbar(tabbar_width = None): 
            '''
            Show the tab bar in the right panel
            '''

            '''
            Create the tab bar
            Temporarily forget the right panel main as well as the scrollbar
            '''
            if (not tabbar_width): 
                tabbar_width = config.right_panel.winfo_width() - 4 * config.boundary_width
            if (config.tabbar_created): return
            else: config.tabbar_created = True
            if (not config.right_panel): return
            if (config.right_panel_tabbar): config.right_panel_tabbar.pack_forget()

            if (config.right_panel_tabbar_scrollbar): 
                config.right_panel_tabbar_scrollbar.pack_forget()

            config.right_panel_main.pack_forget()

            config.right_panel_tabbar = tkinter.Canvas(config.right_panel, height=config.right_panel_tabbar_height, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
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




                new_tab = Right_Panel_Tab(tab_id, tab_frame, tab_type, tab_value, tab_display_name, tab_status)
                total_width += new_tab.width; 
                new_tab.pack(side = 'left')
            
            '''
            Create the scrollbar when there are too many editors
            '''
            if (config.right_panel.winfo_width() != 1 and total_width > tabbar_width): 
                config.right_panel_tabbar_scrollbar = tkinter.Scrollbar(config.right_panel, orient="horizontal", command=config.right_panel_tabbar.xview, width = config.right_panel_tabbar_scrollbar_width) # color setting options do not work
                config.right_panel_tabbar.configure(xscrollcommand=config.right_panel_tabbar_scrollbar.set)
                config.right_panel_tabbar_scrollbar.pack(side='top', fill='x')
                config.tabbar_scrollbar_created = True
                if (config.right_panel_tabbar_scrollbar_position): 
                    position = config.right_panel_tabbar_scrollbar_position
                    config.right_panel_tabbar.after(1000, lambda: config.right_panel_tabbar.xview_moveto(position[0]))
                def right_panel_tabbar_scrollbar_save_scroll_position(): 
                    config.right_panel_tabbar_scrollbar_position = config.right_panel_tabbar_scrollbar.get()
                config.right_panel_tabbar_scrollbar.bind("<Motion>", lambda event: right_panel_tabbar_scrollbar_save_scroll_position())

            '''
            Bind the tabbar with configuration event
            '''
            def tab_frame_configure(event): 
                config.right_panel_tabbar.configure(scrollregion=config.right_panel_tabbar.bbox("all"))
                tabbar_width_new = config.right_panel.winfo_width() - 4 * config.boundary_width
                if (total_width <= tabbar_width_new and config.right_panel_tabbar_scrollbar): 
                    config.right_panel_tabbar_scrollbar.pack_forget(); 
                    config.right_panel_tabbar_scrollbar = None
                    config.tabbar_scrollbar_created = False
                    config.right_panel_tabbar_scrollbar_position = None
                elif (total_width > tabbar_width_new and not config.tabbar_scrollbar_created): 
                    config.tabbar_scrollbar_created = True
                    config.tabbar_created = False; config.right_panel_tabbar.after(100, show_tabbar)
            
            tab_frame.bind("<Configure>", tab_frame_configure)
            update_editor()

        def hide_tabbar(): 
            if (not config.right_panel): return
            if config.right_panel_tabbar:
                config.right_panel_tabbar.pack_forget()
                config.right_panel_tabbar = None

        def update_editor(): 
            '''
            Render the right_panel_main if editor_tab_on_focus is set
            '''
            if (config.current_editor and not config.open_editor_configure): 
                print ("pack forget current editor")
                config.current_editor.pack_forget()
            else: 
                print ("open new editor - protection")
                # config.open_editor_configure = False
            print  (f"config.current_editor_id: {config.current_editor_id}")
            if (config.current_editor_id != -1): 
                config.open_editor_configure = True
                state = config.editor_states[config.current_editor_id]
                print  (config.editor_states, config.current_editor_id, state)
                if (f"{state[0]}|{state[1]}" in config.main_windows.keys()): 
                    config.current_editor = config.main_windows[f"{state[0]}|{state[1]}"]
                else: 
                    config.current_editor = Right_Panel_Main_Window(f"{state[0]}|{state[1]}", state[0])
                config.current_editor.pack(side = 'top', fill = 'both', expand = True)

            '''
            Pack the right_panel_main panel back after updating the tab bar
            '''
            config.right_panel_main.pack(side='top', fill='both', expand=True)

        def create_left_panel(window):
            '''
            Create the left panel in the window
            '''
            def open_editor(tab_type, tab_value, tab_display_name): 
                config.editor_states.append([tab_type, tab_value, tab_display_name])
                if (debug == 1): print (f"Tab '{tab_value}' ({tab_type}) opened. ")
                config.current_editor_id = len(config.editor_states) - 1
                config.tabbar_created = False; show_tabbar()

            def create_left_sidebar(): 
                '''
                Fill in the sidebar of the left panel
                binds open editor to create the right panel editor
                '''
                config.left_panel_sidebar_chat = Left_Sidebar_Icon(hover_color = config.chat_icon_color)
                config.left_panel_sidebar_chat.bind("<Configure>", lambda event: draw_chat_icon(config.left_panel_sidebar_chat))
                config.left_panel_sidebar_chat.bind("<Button-1>", lambda event: open_editor("CHAT", config.CURRENT_ENV, f"Chat: {config.CURRENT_ENV}"))
                config.left_panel_sidebar_crawl = Left_Sidebar_Icon(hover_color = config.crawl_icon_color)
                config.left_panel_sidebar_crawl.bind("<Configure>", lambda event: draw_crawl_icon(config.left_panel_sidebar_crawl))
                config.left_panel_sidebar_crawl.bind("<Button-1>", lambda event: open_editor("CRAWL", f"Web Crawl {new_ID()}", "Web Crawl"))

            def draw_left_panel_arrow(event):
                canvas_width = config.left_panel_change_arrow.winfo_width()
                canvas_height = config.left_panel_change_arrow.winfo_height()
                config.left_panel_change_arrow.delete("arrow")
                arrow_coords = [
                    canvas_width * 0.9, canvas_height * 0.5,
                    canvas_width * 0.5, canvas_height * 0,
                    canvas_width * 0.5, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 1, 
                ]
                config.left_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(config.grey_color_64), tags="arrow")

            def resize_left_panel(event): 
                config.left_panel_relwidth += 0.05
                if config.left_panel_relwidth > config.left_panel_relwidth_max:
                    config.left_panel_relwidth = config.left_panel_relwidth_max
                config.left_panel_width = int(config.left_panel_relwidth * config.window_width)
                config.left_panel.configure(width=config.left_panel_width)
                if (config.editor_states): 
                    config.tabbar_created = False; show_tabbar(tabbar_width = config.window_width - config.left_panel_width - 4 * config.boundary_width)

            def hover_left_panel_arrow(event):
                config.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def leave_left_panel_arrow(event):
                config.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.grey_color_64))

            '''
            Create the left panel background and bind events
            '''
            config.left_panel = tkinter.Frame(window, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
            config.left_panel.pack(side='left', fill='y')
            config.left_panel_sidebar = tkinter.Frame(config.left_panel, width=config.left_panel_sidebar_width, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
            config.left_panel_sidebar.pack(side="left", fill='y')
            config.left_panel_main = tkinter.Frame(config.left_panel, bg=color_tuple_to_rgb(config.left_panel_color))
            config.left_panel_main.pack(side="left", fill='both')

            config.left_panel_change_arrow = tkinter.Canvas(config.left_panel, width=config.size_increase_arrow_width, height=config.size_increase_arrow_height, bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge')
            config.left_panel_change_arrow.bind("<Enter>", hover_left_panel_arrow)
            config.left_panel_change_arrow.bind("<Leave>", leave_left_panel_arrow)
            config.left_panel_change_arrow.bind("<Configure>", draw_left_panel_arrow)
            config.left_panel_change_arrow.bind("<Button-1>", resize_left_panel)

            config.toggle_list_states = dict()
            config.toggle_list_created = False; create_toggle_list()
            create_left_sidebar()

        def create_right_panel(window): 
            '''
            Create the right panel in the window
            '''
            def draw_right_panel_arrow(event):
                canvas_width = config.right_panel_change_arrow.winfo_width()
                canvas_height = config.right_panel_change_arrow.winfo_height()
                config.right_panel_change_arrow.delete("arrow")
                arrow_coords = [
                    canvas_width * 0.1, canvas_height * 0.5,
                    canvas_width * 0.5, canvas_height * 0,
                    canvas_width * 0.5, canvas_height * 0.25,
                    canvas_width * 0.9, canvas_height * 0.25,
                    canvas_width * 0.9, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 1
                ]
                config.right_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(config.grey_color_64), tags="arrow")

            def resize_right_panel(event): 
                config.left_panel_relwidth -= 0.05
                left_panel_width = int(config.left_panel_relwidth * config.window_width)
                if (left_panel_width < config.left_panel_width_min): 
                    left_panel_width = config.left_panel_width_min; 
                    config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                    left_panel_width = int(config.left_panel_relwidth * config.window_width)
                config.left_panel_width = left_panel_width
                config.left_panel.configure(width = config.left_panel_width)
                if (config.editor_states): 
                    config.tabbar_created = False; show_tabbar(tabbar_width = config.window_width - config.left_panel_width - 4 * config.boundary_width)

            def arrow_hover(event):
                config.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def arrow_leave(event):
                config.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.grey_color_64))

            def configure_editor(event): 
                if (config.current_editor and not config.open_editor_configure): 
                    print ("Configure right panel main")
                    config.current_editor.pack_forget()
                    config.current_editor = None
                    config.right_panel_main.after(100, update_editor())
                else: 
                    print ("New editor")
                    config.open_editor_configure = False

            config.right_panel = tkinter.Frame(window, bg=color_tuple_to_rgb(config.right_panel_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
            config.right_panel.pack(side='left', fill='both', expand=True)
            config.right_panel_main = tkinter.Frame(config.right_panel, bg=color_tuple_to_rgb(config.right_panel_color), highlightbackground=color_tuple_to_rgb(config.grey_color_43), highlightthickness=config.boundary_width)
            config.right_panel_main.pack(side='top', fill='both', expand=True)
            config.right_panel_main.bind("<Configure>", configure_editor)
            config.right_panel_change_arrow = tkinter.Canvas(config.right_panel, width=config.size_increase_arrow_width, height=config.size_increase_arrow_height, bg=color_tuple_to_rgb(config.right_panel_color), highlightthickness=0, relief='ridge')
            config.right_panel_change_arrow.bind("<Enter>", arrow_hover)
            config.right_panel_change_arrow.bind("<Leave>", arrow_leave)
            config.right_panel_change_arrow.bind("<Configure>", draw_right_panel_arrow)
            config.right_panel_change_arrow.bind("<Button-1>", resize_right_panel)

        '''
        Create the left panel toggle lists
        '''
        def create_toggle_list_recursive(master, toggle_level, toggle_info): 

            if (toggle_info[3] != None): display_name = '  ' * toggle_level + ('▿  ' if toggle_info[2][0] else '▹  ') + toggle_info[0]
            else: display_name = '  ' * toggle_level + '   ' + toggle_info[0]
            if (toggle_info[1].startswith("environments") and toggle_info[1].count('/') == 1 and toggle_info[1].split('/')[1] == config.CURRENT_ENV): 
                display_name += " (*)"
            entry_frame = Left_Panel_Toggle_Item(master, display_name, toggle_info, True if toggle_level == 0 else False)
            entry_frame.pack_propagate(False)
            entry_frame.pack(anchor = "n", fill = 'x', expand = True, pady=0)
            total_height = config.toggle_item_height
            if (toggle_info[2][0] and toggle_info[3] != None): 
                toggle_child = list(toggle_info[3].keys())
                toggle_child.sort(key = lambda item: item.lower())
                for name in toggle_child: 
                    toggle_child_list = toggle_info[3][name]
                    total_height += create_toggle_list_recursive(master, toggle_level + 1, toggle_child_list)
            entry_frame.configure (height = config.toggle_item_height)
            return total_height
        
        def create_toggle_list(): 
            '''
            Create the toggle list under the left panel
            '''
            if (config.toggle_list_created): return
            if (config.toggle_list): config.toggle_list.pack_forget()

            '''
            Generate the toggle environment name list
            Check whether the previous state is valid: Remove missed environments
            '''
            environment_dict = dict()
            if ("environments" in config.toggle_list_states): 
                environment_dict = config.toggle_list_states["environments"][3]
            previous_environment_names = list(environment_dict.keys())
            for environment_name in previous_environment_names: 
                if (not os.path.exists(os.path.join(DATA_PATH, "environments", environment_name))): 
                    del(environment_dict[environment_name]); continue
                environment_knowkedge_graphs = list(environment_dict[environment_name][3].keys())
                for knowledge_graph_name in environment_knowkedge_graphs: 
                    if (not os.path.exists(os.path.join(DATA_PATH, "environments", environment_name, knowledge_graph_name))): 
                        del(environment_dict[environment_name][3][knowledge_graph_name]); continue
            environment_names = os.listdir(os.path.join(DATA_PATH, "environments")) 
            environment_names.sort (key = lambda name: name.lower())
            for environment_name in environment_names: 
                ## Toggle List Structure: name, value, [toggle status, "edit status"], toggle items
                if (not environment_name in environment_dict): 
                    environment_dict[environment_name] = [environment_name, f"environments/{environment_name}", [False, None], dict()] 
                knowledge_graph_names = os.listdir(os.path.join(DATA_PATH, "environments", environment_name)) 
                knowledge_graph_names.sort (key = lambda name: name.lower())
                for knowledge_graph_name in knowledge_graph_names: 
                    if (not knowledge_graph_name in environment_dict[environment_name][3]): 
                        environment_dict[environment_name][3][knowledge_graph_name] = [f"KG: {knowledge_graph_name}", f"environments/{environment_name}/{knowledge_graph_name}", [False, "saved"], None]
            if ("environments" not in config.toggle_list_states): 
                config.toggle_list_states["environments"] = ["ENVIRONMENTS", "environments", [True, None], environment_dict]

            '''
            Generate the toggle Knowledge Graph list
            '''
            knowledge_graph_dict = dict()
            if ("knowledge_graphs" in config.toggle_list_states): 
                knowledge_graph_dict = config.toggle_list_states["knowledge_graphs"][3]
            previous_knowledge_graph_names = list(knowledge_graph_dict.keys())
            for knowledge_graph_name in previous_knowledge_graph_names: 
                if (not os.path.exists(os.path.join(DATA_PATH, "knowledge_graphs", knowledge_graph_name))): 
                    del(knowledge_graph_dict[knowledge_graph_name]); continue
            knowledge_graph_names = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs")) 
            knowledge_graph_names.sort (key = lambda name: name.lower())
            for knowledge_graph_name in knowledge_graph_names: 
                ## Toggle List Structure: name, value, [toggle status, "edit status"], toggle items
                if (not knowledge_graph_name in knowledge_graph_dict): 
                    knowledge_graph_dict[knowledge_graph_name] = [knowledge_graph_name, f"knowledge_graphs/{knowledge_graph_name}", [False, "saved"], None]
            if ("knowledge_graphs" not in config.toggle_list_states): 
                config.toggle_list_states["knowledge_graphs"] = ["KNOWLEDGE GRAPHS", "knowledge_graphs", [True, None], knowledge_graph_dict]

            '''
            The toggle list stays on the top, expanding in the x direction
            '''
            config.toggle_list = tkinter.Frame(config.left_panel_main, bg=color_tuple_to_rgb(config.VSCode_highlight_color))
            config.toggle_list.pack(anchor="n", fill="both", expand = True)
            config.toggle_list.pack_propagate(False)
            
            '''
            Add environment and Knowledge Graphs into the toggle list
            '''
            left_panel_main_bottom_arrow_area = tkinter.Canvas(config.toggle_list, height = config.size_increase_arrow_height + 8 * config.boundary_width, 
                                               bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness = 0, relief='ridge')
            left_panel_main_bottom_arrow_area.pack(side="bottom", fill="x")
            temp_canvas = tkinter.Canvas(config.toggle_list, bg = color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge'); 
            temp_canvas.pack(side="top", fill="both", expand=True)
            temp_frame = tkinter.Frame(temp_canvas, highlightthickness=0, relief='ridge')
            temp_canvas.create_window((0, 0), window=temp_frame, anchor="nw", tags="temp_frame")
            total_height = 0
            if (debug == 0): print (config.toggle_list_states) 
            for name, value in config.toggle_list_states.items(): 
                total_height += create_toggle_list_recursive(temp_frame, 0, value)
                division_bar = tkinter.Frame (temp_frame, height = config.boundary_width, bg = color_tuple_to_rgb(config.grey_color_43))
                division_bar.pack(anchor = 'n', fill = 'x')
                total_height += config.boundary_width

            '''
            Create the scrollbar, when applicable
            '''
            if (config.left_panel.winfo_height() != 1 and total_height > config.window_height - config.size_increase_arrow_height): 
                if (config.left_panel_main_scrollbar): 
                    config.left_panel_main_scrollbar.pack_forget()
                config.left_panel_main_scrollbar = tkinter.Scrollbar(temp_canvas, orient="vertical", command=temp_canvas.yview, width = config.left_panel_main_scrollbar_width)
                temp_canvas.configure(yscrollcommand = config.left_panel_main_scrollbar.set)
                config.left_panel_main_scrollbar.pack(side='right', fill='y')
                config.toggle_list_scrollbar_created = True

                if (config.left_panel_main_scrollbar_position): 
                    position = config.left_panel_main_scrollbar_position
                    temp_canvas.after(1000, lambda: temp_canvas.yview_moveto(position[0]))
                def left_panel_main_scrollbar_save_scroll_position(): 
                    config.left_panel_main_scrollbar_position = config.left_panel_main_scrollbar.get()
                config.left_panel_main_scrollbar.bind("<Motion>", lambda event: left_panel_main_scrollbar_save_scroll_position())

            def toggle_list_configure(event): 
                temp_canvas.configure(scrollregion=temp_canvas.bbox("all"))
                if (config.left_panel.winfo_height() != 1 and total_height > config.window_height - config.size_increase_arrow_height): 
                    temp_canvas.itemconfigure("temp_frame", width=temp_canvas.winfo_width() - config.left_panel_main_scrollbar_width)
                else: temp_canvas.itemconfigure("temp_frame", width=temp_canvas.winfo_width())
                
                tabbar_height_new = config.window_height - config.size_increase_arrow_height
                if (total_height <= tabbar_height_new and config.left_panel_main_scrollbar): 
                    config.left_panel_main_scrollbar.pack_forget(); 
                    config.left_panel_main_scrollbar = None
                    config.toggle_list_scrollbar_created = False
                    config.left_panel_main_scrollbar_position = None
                elif (total_height > tabbar_height_new and not config.toggle_list_scrollbar_created): 
                    config.toggle_list_scrollbar_created = True
                    config.toggle_list_created = False; create_toggle_list()

            temp_frame.bind("<Configure>", toggle_list_configure)
            config.toggle_list_created = True

        def create_main_window(): 
            '''
            Create the main window
            '''
            config.window = tkinter.Tk()
            config.window.title("RTSAI")
            
            if (config.operating_system() == "MacOS"): 
                config.window.iconphoto(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png")))
            else: 
                '''
                TO BE COMPLETED (Tested)
                '''
                config.window.iconbitmap(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png")))
            config.window.geometry(f"{config.window_width}x{config.window_height}")
            config.window.maxsize(config.window_width_max, config.window_height_max)
            config.window.minsize(config.window_width_min, config.window_height_min)

            '''
            Create the window components
            '''
            create_left_panel(config.window)
            create_right_panel(config.window)
            
            config.window.bind("<Configure>", lambda event: resize_window())

        create_main_window()
        config.window.mainloop()

    elif (sys.argv[1] == "graph"): 

        if (len(sys.argv) < 3): 
            print ("Unknown command. ")
            return
            
        if (len(sys.argv) == 3 and sys.argv[2] == "list"): 
            '''
            List all the current Knowledge Graphs
            '''
            knowledge_graphs = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs"))
            knowledge_graphs.sort()
            if knowledge_graphs:
                print("Current Knowledge Graphs:")
                for environment_name in knowledge_graphs:
                    print(environment_name)
            else:
                print("No Knowledge Graphs found.")

        if len(sys.argv) == 4 and sys.argv[2] == "create":
            '''
            Create a new Knowledge Graph
            '''
            graph_name = sys.argv[3]
            graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
            if (new_name_check(graph_name, graph_path, showinfo="print", keyword="Knowledge Graph") == 0): 
                create_knowledge_graph(graph_name)
                print(f"Knowledge Graph {graph_name} successfully created.")

        if len(sys.argv) == 5 and sys.argv[2] == "copy":
            '''
            Copy an existing Knowledge Graph to create a new Knowledge Graph
            '''
            existing_graph_name = sys.argv[3]
            copied_graph_name = sys.argv[4]
            copy_knowledge_graph(existing_graph_name, copied_graph_name)

        else: 
            print ("Unknown command. ")
            
    elif (sys.argv[1] == "env"): 

        if (len(sys.argv) < 3): 
            print ("Unknown command. ")
            return
            
        if (len(sys.argv) == 3 and sys.argv[2] == "list"): 
            '''
            List all the current environments
            '''
            environments = os.listdir(os.path.join(DATA_PATH, "environments"))
            environments.sort()
            if environments:
                print("Current environments:")
                for environment_name in environments: 
                    if (environment_name == config.CURRENT_ENV): print(f"{environment_name} (*)")
                    else: print (environment_name)
            else:
                print("No environments found.")

        if len(sys.argv) == 4 and sys.argv[2] == "create": 
            '''
            Create a new environment
            '''
            environment_name = sys.argv[3]
            environment_path = os.path.join(DATA_PATH, "environments")
            if (new_name_check(environment_name, environment_path, showinfo="print", keyword="Environment") == 0): 
                create_environment(environment_name)
                print(f"Environment {environment_name} successfully created.")

        if len(sys.argv) >= 5 and sys.argv[2] == "add":
            '''
            Add Knowledge Graphs to an environment
            '''
            environment_name = sys.argv[3]
            graph_names = sys.argv[4:]
            environment_path = os.path.join(DATA_PATH, "environments", environment_name)
            if not os.path.exists(environment_path):
                print(f"Environment '{environment_name}' does not exist.")
            else: 
                for graph_name in graph_names:
                    environment_add_knowledge_graphs(environment_name, graph_names)
                    print(f"Knowledge Graph '{graph_name}' added to environment '{environment_name}'.")

        if len(sys.argv) == 5 and sys.argv[2] == "copy":
            '''
            Copy an existing environment to create a new environment
            '''
            existing_environment_name = sys.argv[3]
            copied_environment_name = sys.argv[4]
            existing_environment_path = os.path.join(DATA_PATH, "environments", existing_environment_name)
            copied_environment_path = os.path.join(DATA_PATH, "environments", copied_environment_name)
            if not os.path.exists(existing_environment_path):
                print(f"Environment '{existing_environment_name}' does not exist.")
            if os.path.exists(copied_environment_path):
                print(f"Environment '{copied_environment_name}' already exists.")
            
            copy_environment(existing_environment_name, copied_environment_name)
            print(f"Environment '{existing_environment_name}' copied to '{copied_environment_name}'.")

        else: 
            print ("Unknown command. ")

    else: 
        print ("Unknown command. ")
        
if __name__ == '__main__': 
    main()

