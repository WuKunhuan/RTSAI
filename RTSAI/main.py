
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

'''
Package setup
'''
def setup(): 
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
        if (showinfo == "print"): print(f"Knowledge Graph '{existing_graph_name}' does not exist{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
        else: show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist{" inside Environment '" + environment_name + "'" if environment_name else ""}.", parent = parent_item)
        return 1
    elif os.path.exists(os.path.join(graph_path, copied_graph_name)):
        if (showinfo == "print"): print(f"Knowledge Graph '{copied_graph_name}' already exists{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
        else: show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists{" inside Environment '" + environment_name + "'" if environment_name else ""}.", parent = parent_item)
        return 1
    elif (new_name_check(copied_graph_name, graph_path, showinfo = showinfo, parent_item = parent_item) == 0): 
        print  (os.path.join(graph_path, existing_graph_name))
        print  (os.path.join(graph_path, copied_graph_name))
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
        import tkinter as tk
        from tkinter import simpledialog, Scrollbar, Listbox, messagebox
        from tkinter.font import Font
        from PIL import Image, ImageTk

        class Editor_Tab(tk.Frame): 
            '''
            The editor tabs inside the tab bar
            '''
            def draw_tab_status(self): 
                pass

            def hover_tab_status(self): 
                pass

            def leave_tab_status(self): 
                pass

            def measure_label_width(self, label): 
                label_text = label.cget("text")
                font = Font(font=label.cget("font"))
                label_width = font.measure(label_text)
                if (debug == 0): print (f"Label width measuring: '{label_text}' [{label_width}]")
                return (label_width)

            def __init__(self, master, tab_type, tab_value, tab_display_name, tab_status): 
                super().__init__(master, bg = color_tuple_to_rgb(config.VSCode_new_color), 
                                 highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), 
                                 highlightthickness=config.boundary_width)
                
                self.tab_type = tab_type; self.tab_value = tab_value
                self.tab_display_name = tab_display_name; 
                self.tab_status = tab_status; 
                self.tab_status_display = "DOT"

                self.font = (config.standard_font_family, config.standard_font_size)
                self.tab_label = tkinter.Label(self, text = tab_display_name, font = self.font, 
                                            bg = color_tuple_to_rgb(config.VSCode_highlight_color), fg = color_tuple_to_rgb(config.VSCode_font_grey_color), )
                tab_label_width = math.ceil(self.measure_label_width(self.tab_label) / config.label_width_ratio)
                self.tab_label.configure(width = tab_label_width)
                self.tab_status = tkinter.Canvas(self, height = config.right_panel_tabbar_height, highlightthickness=0, 
                                            bg = color_tuple_to_rgb(config.left_panel_color))
                tab_status_width = config.right_panel_tabbar_height
                self.tab_status.configure(width = tab_status_width)
                self.width = int((tab_label_width + 1) * config.label_width_ratio + tab_status_width)
                self.configure(width = self.width) 

                self.tab_label.pack(side = 'left', expand = False); 
                self.tab_status.pack(side = 'left', expand = False)
                self.bind("<Configure>", lambda event: self.draw_tab_status())
                self.tab_label.bind("<Enter>", lambda event: self.hover_tab_status())
                self.tab_status.bind("<Enter>", lambda event: self.hover_tab_status())
                self.tab_label.bind("<Leave>", lambda event: self.leave_tab_status())
                self.tab_status.bind("<Leave>", lambda event: self.leave_tab_status())

        class Left_Panel_Toggle_Item(tk.Frame): 
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
                self.toggle_item_modify.create_oval(canvas_width * 0.25, canvas_height * 0.25, canvas_height * 0.75, canvas_height * 0.75, fill=color_tuple_to_rgb(config.default_grey_color), tags="modify", outline = color_tuple_to_rgb(config.left_panel_color))

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
                        select_knowledge_graph_window = tk.Toplevel(self)
                        select_knowledge_graph_window.title(f"Select Knowledge Graphs for the Environment '{environment_name}'")
                        select_knowledge_graph_window.resizable(width = False, height = False)
                        knowledge_graph_names = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs")) 
                        knowledge_graph_names.sort (key = lambda name: name.lower())
                        knowledge_graph_names_current = os.listdir(os.path.join(DATA_PATH, self.toggle_info[1])) 
                        knowledge_graph_names = [name for name in knowledge_graph_names if name not in knowledge_graph_names_current]
                        knowledge_graph_list = None

                        if (not knowledge_graph_names): select_knowledge_graph_prompt = tk.Label(select_knowledge_graph_window, text = f"No Knowledge Graphs are available! ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10); return

                        if (len(knowledge_graph_names) > 12): 
                            select_knowledge_graph_prompt = tk.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. \nPlease scroll down to see the full list ({len(knowledge_graph_names)} items). ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                            select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                        else: 
                            select_knowledge_graph_prompt = tk.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. ", font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                            select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                        
                        select_knowledge_graph_frame = tk.Frame(select_knowledge_graph_window, bg = color_tuple_to_rgb(config.left_panel_color))
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
                            show_popup_message (f"Knowledge Graphs {', '.join([f"'{item}'" for item in success_items])} successfully added to the Environment '{environment_name}'.")
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
                    modify_menu_list.add_command(label="Rename the Environment", command = rename_environment)
                    modify_menu_list.add_command(label="Delete the Environment", command = delete_environment)
                    modify_menu_list.add_command(label="Copy the Environment", command = copy_environment_menu)
                    modify_menu_list.add_command(label="Set as the current", command = set_as_current_environment)
                    modify_menu_list.add_command(label="Add Knowledge Graphs", command = add_knowledge_graphs)
                    modify_menu_list.add_command(label="Export the Environment (to be completed)", command = export_environment)
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
                    modify_menu_list.add_command(label="Rename the Knowledge Graph", command = rename_knowledge_graph)
                    modify_menu_list.add_command(label="Delete the Knowledge Graph", command = delete_knowledge_graph)
                    modify_menu_list.add_command(label="Copy the Knowledge Graph", command = copy_knowledge_graph_menu)
                    modify_menu_list.add_command(label="Save the Knowledge Graph", command = save_to_knowledge_graph)
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
                    modify_menu_list.add_command(label="Rename the Knowledge Graph", command = rename_knowledge_graph)
                    modify_menu_list.add_command(label="Delete the Knowledge Graph", command = delete_knowledge_graph)
                    modify_menu_list.add_command(label="Copy the Knowledge Graph", command = copy_knowledge_graph_menu)
                    modify_menu_list.add_command(label="Export the Knowledge Grpah (to be completed)", command = export_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)
                
                self.menu_open = False

            '''
            Click the item and change the focus
            '''
            def click_toggle_item(self, event): 

                config.toggle_item_on_focus = self.toggle_info[1]
                self.toggle_info[2][0] = not self.toggle_info[2][0]
                if (debug == 1): print (f"Change focus to {config.toggle_item_on_focus}")
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
                config.toggle_list_created = False; create_toggle_list()

            def __init__(self, master, toggle_display_name, toggle_info, bold=False):

                super().__init__(master, bg=color_tuple_to_rgb(config.left_panel_color))
                self.pack_propagate(False)
                self.toggle_info = toggle_info
                self.menu_open = False
                self.label = tk.Label(self, text=toggle_display_name, font=(config.standard_font_family, config.standard_font_size, "bold" if bold else "normal"), anchor = "w", 
                                    fg=color_tuple_to_rgb(config.VSCode_font_grey_color), bg=color_tuple_to_rgb(config.left_panel_color), 
                                    relief="flat", borderwidth=0)
                if (self.toggle_info[1].startswith("knowledge_graphs") or (self.toggle_info[1].startswith("environments"))): 
                    self.toggle_item_modify = tk.Canvas(self, width=config.toggle_modify_width, height=config.toggle_modify_height, 
                                                bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge')
                    self.toggle_item_modify.pack (side = 'right', padx = 0, pady = 0)
                    self.toggle_item_modify.bind('<Configure>', self.configure_canvas_modify)
                    self.toggle_item_modify.bind("<Button-1>", self.modify_toggle_item)

                self.label.pack (side = "top", fill = "x")
                if (config.toggle_item_on_focus == self.toggle_info[1]): 
                    self.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))
                    self.label.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))
                    if (self.toggle_info[1].startswith("knowledge_graphs") or self.toggle_info[1].startswith("environments")): 
                        self.toggle_item_modify.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))

                self.configure(height=config.toggle_item_height, width=config.left_panel_width - config.left_panel_sidebar_width)
                self.bind("<Button-1>", self.click_toggle_item)
                self.label.bind("<Button-1>", self.click_toggle_item)

                '''
                WARNING Some platforms may use Button-3 instead
                TO BE COMPLETED
                '''
                if (True): 
                    self.bind("<Button-2>", self.modify_toggle_item)
                    self.label.bind("<Button-2>", self.modify_toggle_item)
                    self.toggle_item_modify.bind("<Button-2>", self.modify_toggle_item)

        def color_tuple_to_rgb (color_tuple): 
            '''
            Convert color tuples to rgb string
            '''
            return ("#%02x%02x%02x" % color_tuple)

        def check_editor_status (source_file): 
            opened_editors = [editor[0] for editor in config.editor_states]
            if (source_file not in opened_editors): return None
            else: return (config.editor_states[opened_editors.index(source_file)][1])

        def resize_window(): 
            '''
            Resizes the main window. Toggle lists, etc. will be rendered again when appropriate. 
            '''
            window_geometry = list(map(int, config.window.geometry().replace('x', ' ').replace('+', ' ').split(' ')))
            config.window_width = window_geometry[0]
            config.window_height = window_geometry[1]

            '''
            Configure the overall panel
            '''
            left_panel_width = int(config.left_panel_relwidth * config.window_width)
            if (config.window_width >= config.window_width_min and left_panel_width < config.left_panel_width_min): 
                left_panel_width = config.left_panel_width_min; 
                config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                left_panel_width = int(config.left_panel_relwidth * config.window_width)

            config.left_panel_width = left_panel_width
            try: 
                config.left_panel.configure (width = config.left_panel_width, height = config.window_height)
                config.left_panel_sidebar.configure (width = config.left_panel_sidebar_width)
                config.toggle_list.configure (width = config.left_panel_width - config.left_panel_sidebar_width)
                config.right_panel.configure (height = config.window_height)
                config.left_panel_change_arrow.place(x = config.left_panel_width - 3 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tkinter.SE)
                config.right_panel_change_arrow.place(x = 1 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tk.SW)
            except: pass
            create_toggle_list()

        def render_right_panel(): 
            '''
            Retrieve the current editor opened and decide what to do
            '''
            pass

        def show_tabbar(): 
            if (not config.right_panel): return
            else: 
                if (config.right_panel_tabbar): config.right_panel_tabbar.pack_forget()
                config.right_panel_main.pack_forget()
            config.right_panel_tabbar = tk.Canvas(config.right_panel, height=config.right_panel_tabbar_height, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.right_panel_tabbar.pack(side='top', fill='x')
            total_width = 0; maximum_width = config.right_panel.winfo_width()
            tab_frame = tk.Frame(config.right_panel_tabbar); # tab_frame.pack(side = 'left', fill = 'both')
            config.right_panel_tabbar.create_window((0, 0), window=tab_frame, anchor="nw", tags="tab_frame")
            
            for editor_tab in config.editor_states: 
                tab_type = editor_tab[0][0]; tab_value = editor_tab[0][1]
                tab_display_name = editor_tab[0][2]; tab_status = editor_tab[1]
                new_tab = Editor_Tab(tab_frame, tab_type, tab_value, tab_display_name, tab_status)
                total_width += new_tab.width; 
                new_tab.pack(side = 'left')
            print  (total_width, config.right_panel.winfo_width() - 4 * config.boundary_width)
            if (total_width > config.right_panel.winfo_width() - 4 * config.boundary_width): 
                tab_scrollbar = tk.Scrollbar(config.right_panel, orient="horizontal", command=config.right_panel_tabbar.xview)
                config.right_panel_tabbar.configure(xscrollcommand=tab_scrollbar.set)
                tab_scrollbar.pack(side='top', fill='x')
                # config.right_panel_tabbar.create_window((0, 0), window=tab_frame, anchor="nw", tags="tab_frame")
                def tab_frame_configure(event): 
                    config.right_panel_tabbar.configure(scrollregion=config.right_panel_tabbar.bbox("all"))
                tab_frame.bind("<Configure>", tab_frame_configure)
            config.right_panel_main.pack(side='top', fill='both', expand=True)

        def hide_tabbar(): 
            if (not config.right_panel): return
            if config.right_panel_tabbar:
                config.right_panel_tabbar.pack_forget()
                config.right_panel_tabbar = None

        def create_left_panel(window):
            '''
            Create the left panel in the window
            '''

            class Left_Sidebar_Icon(tk.Canvas):
                '''
                The left sidebar icon entity
                '''
                def __init__(self):
                    super().__init__(master = config.left_panel_sidebar, width=config.left_panel_sidebar_width, height=config.left_panel_sidebar_width, 
                                     bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0)
                    self.hovered = False
                    self.items_in_panel = []
                    self.bind("<Enter>", self.on_enter)
                    self.bind("<Leave>", self.on_leave)
                    self.pack(side = "top")

                def on_enter(self, event): 
                    self.hovered = True
                    for item in self.items_in_panel: 
                        self.itemconfigure(item, fill=color_tuple_to_rgb(config.VSCode_highlight_color))

                def on_leave(self, event):
                    self.hovered = False
                    for item in self.items_in_panel: 
                        self.itemconfigure(item, fill=color_tuple_to_rgb(config.VSCode_font_grey_color))

            def draw_sidebar_chat(parent_canvas): 
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
                parent_canvas.create_polygon(item_1_rectangle_coords, fill = color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_1_rectangle", smooth=True, outline = "")
                parent_canvas.create_polygon(item_2_triangle_coords, fill = color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_2_triangle", outline = "")
                parent_canvas.items_in_panel = ["item_1_rectangle", "item_2_triangle"]

            def open_editor(tab_type, tab_value, tab_display_name): 
                config.editor_states.append([(tab_type, tab_value, tab_display_name), "SAVED"])
                show_tabbar()

            def draw_sidebar_crawl(parent_canvas): 
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
                
                parent_canvas.create_oval(0.3 * canvas_width, 0.3 * canvas_height, 0.7 * canvas_width, 0.7 * canvas_height, fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_1_spider_body", outline = "")
                parent_canvas.create_oval(0.4 * canvas_width, 0.2 * canvas_height, 0.6 * canvas_width, 0.4 * canvas_height, fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_8_spider_head", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.4 * canvas_height, 0.27 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_2_spider_leg_1", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.5 * canvas_height, 0.27 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_3_spider_leg_2", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.6 * canvas_height, 0.27 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_4_spider_leg_3", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.4 * canvas_height, 0.73 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_5_spider_leg_4", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.5 * canvas_height, 0.73 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_6_spider_leg_5", outline = "")
                parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.6 * canvas_height, 0.73 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=color_tuple_to_rgb(config.VSCode_font_grey_color), tags="item_7_spider_leg_6", outline = "")
                parent_canvas.items_in_panel = ["item_1_spider_body", "item_8_spider_head", "item_2_spider_leg_1", "item_3_spider_leg_2", "item_4_spider_leg_3", "item_5_spider_leg_4", "item_6_spider_leg_5", "item_7_spider_leg_6"]

            def create_left_sidebar(): 
                '''
                Fill in the sidebar of the left panel
                '''
                config.left_panel_sidebar_chat = Left_Sidebar_Icon()
                config.left_panel_sidebar_chat.bind("<Configure>", lambda event: draw_sidebar_chat(config.left_panel_sidebar_chat))
                config.left_panel_sidebar_chat.bind("<Button-1>", lambda event: open_editor("CHAT", config.CURRENT_ENV, config.CURRENT_ENV))
                config.left_panel_sidebar_crawl = Left_Sidebar_Icon()
                config.left_panel_sidebar_crawl.bind("<Configure>", lambda event: draw_sidebar_crawl(config.left_panel_sidebar_crawl))
                config.left_panel_sidebar_crawl.bind("<Button-1>", lambda event: open_editor("CRAWL", "Web Crawl", "wwww"))

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
                config.left_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(config.default_grey_color), tags="arrow")

            def resize_left_panel(event): 
                config.left_panel_relwidth += 0.05
                if config.left_panel_relwidth > config.left_panel_relwidth_max:
                    config.left_panel_relwidth = config.left_panel_relwidth_max
                config.left_panel_width = int(config.left_panel_relwidth * config.window_width)
                config.left_panel.configure(width=config.left_panel_width)

            def hover_left_panel_arrow(event):
                config.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def leave_left_panel_arrow(event):
                config.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.default_grey_color))

            '''
            Create the left panel background and bind events
            '''
            config.left_panel = tk.Frame(window, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.left_panel.pack(side='left', fill='y')
            config.left_panel_sidebar = tk.Frame(config.left_panel, width=config.left_panel_sidebar_width, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.left_panel_sidebar.pack(side="left", fill='y')
            config.left_panel_main = tk.Frame(config.left_panel, bg=color_tuple_to_rgb(config.left_panel_color))
            config.left_panel_main.pack(side="left", fill='both')

            config.left_panel_change_arrow = tk.Canvas(config.left_panel, width=config.size_increase_arrow_width, height=config.size_increase_arrow_height, bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge')
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
                config.right_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(config.default_grey_color), tags="arrow")

            def resize_right_panel(event): 
                config.left_panel_relwidth -= 0.05
                left_panel_width = int(config.left_panel_relwidth * config.window_width)
                if (left_panel_width < config.left_panel_width_min): 
                    left_panel_width = config.left_panel_width_min; 
                    config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                    left_panel_width = int(config.left_panel_relwidth * config.window_width)
                config.left_panel_width = left_panel_width
                config.left_panel.configure(width = config.left_panel_width)

            def arrow_hover(event):
                config.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def arrow_leave(event):
                config.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.default_grey_color))

            config.right_panel = tk.Frame(window, bg=color_tuple_to_rgb(config.right_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.right_panel.pack(side='left', fill='both', expand=True)

            config.right_panel_main = tk.Frame(config.right_panel, bg=color_tuple_to_rgb(config.right_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.right_panel_main.pack(side='top', fill='both', expand=True)
            config.right_panel_change_arrow = tk.Canvas(config.right_panel, width=config.size_increase_arrow_width, height=config.size_increase_arrow_height, bg=color_tuple_to_rgb(config.right_panel_color), highlightthickness=0, relief='ridge')
            config.right_panel_change_arrow.bind("<Enter>", arrow_hover)
            config.right_panel_change_arrow.bind("<Leave>", arrow_leave)
            config.right_panel_change_arrow.bind("<Configure>", draw_right_panel_arrow)
            config.right_panel_change_arrow.bind("<Button-1>", resize_right_panel)

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

            config.toggle_list = tk.Frame(config.left_panel_main, bg=color_tuple_to_rgb(config.VSCode_new_color))
            '''
            The toggle list stays on the top, expanding in the x direction
            Option: pack
            '''
            # config.toggle_list.place(x = 0, y = 0)
            config.toggle_list.pack(anchor="n", fill="x", expand = True)
            config.toggle_list.pack_propagate(False)
            total_height = 0
            if (debug == 0): print (config.toggle_list_states) 
            
            '''
            Add environment and Knowledge Graphs into the toggle list
            '''
            for name, value in config.toggle_list_states.items(): 
                total_height += create_toggle_list_recursive(config.toggle_list, 0, value)
                division_bar = tkinter.Frame (config.toggle_list, height = config.boundary_width, bg = color_tuple_to_rgb(config.boundary_grey_color))
                division_bar.pack(anchor = 'n', fill = 'x')
                total_height += config.boundary_width

            config.toggle_list.configure (height = total_height)
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

