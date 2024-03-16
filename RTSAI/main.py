
import sys, os, shutil, re, math

import RTSAI.config as config
from RTSAI.config import EXECUTABLE_PATH, PACKAGE_PATH, DATA_PATH, ASSETS_PATH
from RTSAI.config import DEFAULT_ENV, CURRENT_ENV
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
    Pre-installation of knowledge graph files
    '''
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        os.makedirs(os.path.join(DATA_PATH, "environments"))
        os.makedirs(os.path.join(DATA_PATH, "environments", DEFAULT_ENV))
        knowledge_graphs_path = os.path.join(DATA_PATH, "knowledge_graphs")

        '''
        Copy pre-installed knowledge graphs to the "knowledge_graphs" folder
        '''
        for graph_name in PRE_INSTALLED_KG:
            src_dir = os.path.join(PRE_INSTALLED_KG_PATH, graph_name)
            dst_dir = os.path.join(knowledge_graphs_path, graph_name)
            shutil.copytree(src_dir, dst_dir)

def show_popup_message(message, title = "Message"):
    import tkinter
    tkinter.messagebox.showinfo(title, message)

def new_name_check(name, path = DATA_PATH, showinfo = "print", keyword = "", max_length = 30): 
    if os.path.exists(os.path.join(path, name)): 
        if (showinfo == "print"): print(f"{keyword} Name '{name}' already exists.")
        else: show_popup_message(f"{keyword} '{name}' already exists.")
    elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name): 
        if (len(name) <= max_length): return 0
        else: 
            if (showinfo == "print"): print(f"{keyword} Name '{name}' too long (max. 30 characters).")
            else: show_popup_message(f"{keyword} '{name}' too long (max. 30 characters).")
    else: 
        if (showinfo == "print"): print(f"Invalid {keyword} Name '{name}'. Please follow the rules for Python identifiers.")
        else: show_popup_message(f"Invalid {keyword} Name '{name}'. Please follow the rules for Python identifiers.")
    return 1

'''
Create or rename an environment
'''
def create_environment(environment_name, previous_environment_name = None):
    '''
    Create a new environment folder with the given name
    Before this function, necessary name checking should be performed. 
    '''
    environment_path = os.path.join(DATA_PATH, "environments", environment_name)
    if previous_environment_name and os.path.exists(os.path.join(DATA_PATH, "environments", previous_environment_name)):
        previous_environment_path = os.path.join(DATA_PATH, "environments", previous_environment_name)
        os.rename(previous_environment_path, environment_path)
    else: os.makedirs(environment_path)

'''
'''
def copy_environment(existing_environment_name, copied_environment_name):
    '''
    Copy an existing environment to create a new environment
    '''
    existing_environment_path = os.path.join(DATA_PATH, "environments", existing_environment_name)
    copied_environment_path = os.path.join(DATA_PATH, "environments", copied_environment_name)
    shutil.copytree(existing_environment_path, copied_environment_path)

'''
Create or rename a knowledge graph
'''
def create_knowledge_graph(graph_name, previous_graph_name = None):
    '''
    Create a new knowledge graph folder with the given name. 
    Before this function, necessary name checking should be performed. 
    '''
    graph_path = os.path.join(DATA_PATH, "knowledge_graphs", graph_name)
    if previous_graph_name and os.path.exists(os.path.join(DATA_PATH, "environments", previous_graph_name)):
        previous_graph_path = os.path.join(DATA_PATH, "environments", previous_graph_name)
        os.rename(previous_graph_path, graph_path)
    else:
        os.makedirs(graph_path)
        template_path = os.path.join(ASSETS_PATH, "templates", "template_knowledge_graph")
        shutil.copytree(template_path, graph_path)

'''
'''
def copy_knowledge_graph(existing_graph_name, copied_graph_name, environment_name = None, showinfo = "print"):
    '''
    Copy an existing knowledge graph to create a new knowledge graph
    '''
    if (environment_name): 
        existing_graph_path = os.path.join(DATA_PATH, "environments", environment_name, existing_graph_name)
        copied_graph_path = os.path.join(DATA_PATH, "environments", environment_name, copied_graph_name)
    else: 
        existing_graph_path = os.path.join(DATA_PATH, "knowledge_graphs", existing_graph_name)
        copied_graph_path = os.path.join(DATA_PATH, "knowledge_graphs", copied_graph_name)
    if not os.path.exists(existing_graph_path):
        if (showinfo == "print"): print(f"Knowledge Graph '{existing_graph_name}' does not exist{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
        else: show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
    elif os.path.exists(copied_graph_path):
        if (showinfo == "print"): print(f"Knowledge Graph '{copied_graph_name}' already exists{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
        else: show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
    else: 
        shutil.copytree(existing_graph_path, copied_graph_path)
        if (showinfo == "print"): print(f"Knowledge Graph '{copied_graph_name}' copied to '{copied_graph_name}{" inside Environment '" + environment_name + "'" if environment_name else ""}.")
        else: show_popup_message(f"Knowledge Graph '{copied_graph_name}' copied to '{copied_graph_name}{" inside Environment '" + environment_name + "'" if environment_name else ""}.")

'''
'''
def environment_add_knowledge_graphs(environment_name, graph_names, showinfo = "print"):
    '''
    Add knowledge graphs to the specified environment
    '''
    imported_knowledge_graphs = []
    for graph_name in graph_names: 
        graph_src_path = os.path.join(DATA_PATH, "knowledge_graphs")
        graph_dst_path = os.path.join(DATA_PATH, "environments", environment_name)
        if not os.path.exists(graph_src_path): 
            if (showinfo == "print"): print(f"Knowledge Graph '{graph_name}' does not exist."); continue
            else: show_popup_message(f"Knowledge Graph '{graph_name}' does not exist."); continue
        if (new_name_check(graph_name, graph_dst_path, showinfo, "Knowledge Graph") == 0): 
            shutil.copytree(os.path.join(graph_src_path, graph_name), os.path.join(graph_dst_path, graph_name))
            imported_knowledge_graphs.append(graph_name)
    return imported_knowledge_graphs

'''
Rename a knowledge graph inside an environment. 
'''
def environment_rename_knowledge_graph(environment_name, graph_name, previous_graph_name, showinfo = "print"): 
    '''
    Rename a knowledge graph inside an environment
    '''
    graph_path = os.path.join(DATA_PATH, "environments", environment_name)
    if not os.path.exists(os.path.join(graph_path, previous_graph_name)): 
        if (showinfo == "print"): print(f"Knowledge Graph '{graph_name}' does not exist in the Environment '{environment_name}'."); 
        else: show_popup_message(f"Knowledge Graph '{graph_name}' does not exist in the Environment '{environment_name}'."); 
    elif (new_name_check(graph_name, graph_path, showinfo, "Knowledge Graph") == 0): 
        shutil.move(os.path.join(graph_path, previous_graph_name), os.path.join(graph_path, graph_name))
        return 0

'''
The main function handling both the UI and the Terminal Application
'''
def main(): 

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
        from PIL import Image, ImageTk

        '''
        Convert color tuples to rgb
        '''
        def color_tuple_to_rgb(color_tuple): 
            return ("#%02x%02x%02x" % color_tuple)

        '''
        Create the left panel in the window
        '''
        def create_left_panel():

            def configure_canvas_arrow(event):
                canvas_width = config.left_panel_change_arrow.winfo_width()
                canvas_height = config.left_panel_change_arrow.winfo_height()
                config.left_panel_change_arrow.delete("arrow")
                config.left_panel_change_arrow.config(width=canvas_width, height=canvas_height)
                arrow_coords = [
                    canvas_width * 0.9, canvas_height * 0.5,
                    canvas_width * 0.5, canvas_height * 0,
                    canvas_width * 0.5, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 1
                ]
                config.left_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(config.default_grey_color), tags="arrow")

            def resize_left_panel(event): 
                config.left_panel_relwidth += 0.05
                if config.left_panel_relwidth > config.left_panel_relwidth_max:
                    config.left_panel_relwidth = config.left_panel_relwidth_max
                config.left_panel_width = int(config.left_panel_relwidth * config.window_width)
                config.left_panel.configure(width=config.left_panel_width)

            def arrow_hover(event):
                config.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def arrow_leave(event):
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
            config.left_panel_change_arrow.bind("<Enter>", arrow_hover)
            config.left_panel_change_arrow.bind("<Leave>", arrow_leave)
            config.left_panel_change_arrow.bind("<Configure>", configure_canvas_arrow)
            config.left_panel_change_arrow.bind("<Button-1>", resize_left_panel)
            config.toggle_list_states = dict()

        '''
        Create the right panel in the window
        '''
        def create_right_panel(): 

            def show_tabbar(): 
                config.right_panel_tabbar = tk.Frame(config.right_panel, height=config.right_panel_tabbar_height, bg=color_tuple_to_rgb(config.left_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
                config.right_panel_tabbar.pack(side='top', fill='x')
            
            def hide_tabbar(): 
                if config.right_panel_tabbar:
                    config.right_panel_tabbar.pack_forget()
                    config.right_panel_tabbar = None

            def configure_canvas_arrow(event):
                canvas_width = config.right_panel_change_arrow.winfo_width()
                canvas_height = config.right_panel_change_arrow.winfo_height()
                config.right_panel_change_arrow.delete("arrow")
                config.right_panel_change_arrow.config(width=canvas_width, height=canvas_height)
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

            '''
            Show the tab bar when the editor is active. 
            '''
            show_tabbar()

            config.right_panel_main = tk.Frame(config.right_panel, bg=color_tuple_to_rgb(config.right_panel_color), highlightbackground=color_tuple_to_rgb(config.boundary_grey_color), highlightthickness=config.boundary_width)
            config.right_panel_main.pack(side='top', fill='both', expand=True)
            
            config.right_panel_change_arrow = tk.Canvas(config.right_panel, width=config.size_increase_arrow_width, height=config.size_increase_arrow_height, bg=color_tuple_to_rgb(config.right_panel_color), highlightthickness=0, relief='ridge')
            config.right_panel_change_arrow.bind("<Enter>", arrow_hover)
            config.right_panel_change_arrow.bind("<Leave>", arrow_leave)
            config.right_panel_change_arrow.bind("<Configure>", configure_canvas_arrow)
            config.right_panel_change_arrow.bind("<Button-1>", resize_right_panel)

        '''
        Toggle Item class objects in the left panel main
        '''
        class Toggle_Item(tk.Frame): 

            '''
            Generates the modify sign again when applicable
            '''
            def configure_canvas_modify(self, event):
                canvas_width = config.toggle_create_new_modify_width
                canvas_height = config.toggle_create_new_modify_height
                self.toggle_item_modify.delete("modify")
                self.toggle_item_modify.config(width=canvas_width, height=canvas_height)
                modify_coords = [
                    canvas_width * 0.8, canvas_height * 1, 
                    canvas_width * 1, canvas_height * 1, 
                    canvas_width * 1, canvas_height * 0, 
                    canvas_width * 0.8, canvas_height * 0, 
                ]
                self.toggle_item_modify.create_polygon(modify_coords, fill=color_tuple_to_rgb(config.default_grey_color), tags="modify")

            def modify_hover(self, event): 
                self.toggle_item_modify.itemconfigure("modify", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

            def modify_leave(self, event): 
                if (self.menu_open): self.toggle_item_modify.itemconfigure("modify", fill=color_tuple_to_rgb(config.VSCode_highlight_color))
                else: self.toggle_item_modify.itemconfigure("modify", fill=color_tuple_to_rgb(config.default_grey_color))

            def modify_menu(self, event): 

                self.menu_open = True
                self.toggle_item_modify.itemconfigure("modify", fill=color_tuple_to_rgb(config.VSCode_highlight_color))

                if (self.toggle_info[1] == "environments"): 

                    '''
                    Menu for the Environment toggle item
                    '''
                    def menu_create_environment(): 
                        environment_name = simpledialog.askstring("Create Environment", "Enter the name of the environment: ", parent = self.toggle_item_modify)
                        if environment_name:
                            environment_path = os.path.join(DATA_PATH, "environments")
                            if (new_name_check(environment_name, environment_path, showinfo="messagebox", keyword="Environment") == 0): 
                                create_environment(environment_name)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Environment '{environment_name}' successfully created.")

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Create an Environment", command = menu_create_environment)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1].startswith("environments") and self.toggle_info[1].count('/') == 1): 

                    '''
                    Menu for the Environment's knowledge graph toggle item
                    '''
                    environment_name = self.toggle_info[1].split('/')[1]

                    '''
                    Rename the environment
                    '''
                    def rename(): 
                        environment_name_new = simpledialog.askstring("Rename Environment", f"Enter the new name of the Environment '{environment_name}': ", parent = self.toggle_item_modify)
                        if environment_name_new:
                            environment_path = os.path.join(DATA_PATH, "environments")
                            if (new_name_check(environment_name_new, environment_path, showinfo="messagebox", keyword="Environment") == 0): 
                                create_environment(environment_name_new, environment_name)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Environment '{environment_name}' successfully renamed to '{environment_name_new}'.")

                    def delete(): 

                        if environment_name == CURRENT_ENV:
                            messagebox.showwarning("Cannot Delete", "Cannot delete the Current Environment.")
                        else:
                            confirm = messagebox.askyesno("Confirm Environment Deletion", f"Are you sure you want to delete the Environment '{environment_name}'?")
                            if confirm:
                                environment_path = os.path.join(DATA_PATH, "environments", environment_name)
                                try:
                                    shutil.rmtree(environment_path)
                                    config.toggle_list_created = False; create_toggle_list()
                                    show_popup_message(f"Environment '{environment_name}' successfully deleted.")
                                except OSError:
                                    messagebox.showerror("Environment Deletion Failed", f"Failed to delete the Environment '{environment_name}'.")

                    def copy(): 
                        pass

                    def set_as_default(): 
                        pass

                    def add_knowledge_graphs(): 
                        select_knowledge_graph_window = tk.Toplevel(self)
                        select_knowledge_graph_window.title(f"Select Knowledge Graphs for the Environment '{environment_name}'")
                        select_knowledge_graph_window.resizable(width = False, height = False)
                        knowledge_graph_names = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs")) 
                        knowledge_graph_names.sort (key = lambda name: name.lower())
                        knowledge_graph_names_current = os.listdir(os.path.join(DATA_PATH, self.toggle_info[1])) 
                        knowledge_graph_names = [name for name in knowledge_graph_names if name not in knowledge_graph_names_current]
                        knowledge_graph_list = None

                        if (knowledge_graph_names): 
                            select_knowledge_graph_prompt = tk.Label(select_knowledge_graph_window, text = f"Select all knowledge graphs to be added from the below list. ", 
                                                                    font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                        else: 
                            select_knowledge_graph_prompt = tk.Label(select_knowledge_graph_window, text = f"No knowledge graphs are available! ", 
                                                                    font = (config.standard_font_family, int(config.standard_font_size * 1.2)), padx = 10, pady = 10)
                        select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                        if (knowledge_graph_names): 
                            select_knowledge_graph_frame = tk.Frame(select_knowledge_graph_window, bg = color_tuple_to_rgb(config.left_panel_color))
                            select_knowledge_graph_frame.pack(side = "top", anchor = "n", fill = "both", 
                                                            padx = 10, pady = 0)
                            knowledge_graph_list = Listbox(select_knowledge_graph_frame, selectmode = "multiple", 
                                                        bg = color_tuple_to_rgb(config.left_panel_color), 
                                                        fg = color_tuple_to_rgb(config.VSCode_font_grey_color), 
                                                        selectbackground = color_tuple_to_rgb(config.VSCode_highlight_color), 
                                                        selectforeground = color_tuple_to_rgb(config.left_panel_color), 
                                                        font = (config.standard_font_family, config.standard_font_size), 
                                                        height = len(knowledge_graph_names), activestyle='none')
                            for knowledge_graph_name in knowledge_graph_names: 
                                knowledge_graph_list.insert("end", f"{knowledge_graph_name}")
                            if (len(knowledge_graph_names) > 12): 
                                select_knowledge_graph_frame_scrollbar = Scrollbar(select_knowledge_graph_frame)
                                select_knowledge_graph_frame_scrollbar.pack(side = "right", fill = "y")
                                select_knowledge_graph_frame_scrollbar.config(command = knowledge_graph_list.yview, 
                                                                            yscrollcommand = select_knowledge_graph_frame_scrollbar.set) 
                                select_knowledge_graph_window.geometry(f'600x300+{max(event.x_root-300, 0)}+{max(event.y_root-150, 0)}')
                            else: 
                                select_knowledge_graph_window.geometry(f'600x{84+18*len(knowledge_graph_names)}+{max(event.x_root-300, 0)}+{max(int(event.y_root-(84+18*len(knowledge_graph_names))/2), 0)}')
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
                        pass

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Rename", command = rename)
                    modify_menu_list.add_command(label="Delete", command = delete)
                    modify_menu_list.add_command(label="Copy", command = copy)
                    modify_menu_list.add_command(label="Set as default", command = set_as_default)
                    modify_menu_list.add_command(label="Add Knowledge Graphs", command = add_knowledge_graphs)
                    modify_menu_list.add_command(label="Export Environment", command = export_environment)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1].startswith("environments") and self.toggle_info[1].count('/') == 2): 

                    environment_name = self.toggle_info[1].split('/')[1]
                    knowledge_graph_name = self.toggle_info[1].split('/')[2]

                    '''
                    Rename the knowledge graph inside an environment
                    '''
                    def rename(): 
                        knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the new name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self.toggle_item_modify)
                        if knowledge_graph_name_new:
                            if (environment_rename_knowledge_graph(environment_name, knowledge_graph_name_new, knowledge_graph_name, showinfo = "messagebox") == 0): 
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}' inside Environment '{environment_name}'.")

                    '''
                    Delete the knowledge graph inside an environment
                    '''
                    def delete(): 
                        confirm = messagebox.askyesno("Confirm Knowledge Graph Deletion", f"Are you sure you want to delete the Knowledge Graph '{knowledge_graph_name}'?")
                        if confirm:
                            knowledge_graph_path = os.path.join(DATA_PATH, "environments", environment_name, knowledge_graph_name)
                            try:
                                shutil.rmtree(knowledge_graph_path)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully deleted inside Environment {environment_name}.")
                            except OSError:
                                messagebox.showerror("Knowledge Graph Deletion Failed", f"Failed to delete the Knowledge Graph {knowledge_graph_name} inside Environment '{environment_name}'.")

                    '''
                    Copy the knowledge graph inside an environment
                    '''
                    def copy(): 
                        knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the copy name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self.toggle_item_modify)
                        if knowledge_graph_name_new:
                            knowledge_graph_path = os.path.join(DATA_PATH, "environments", environment_name)
                            if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, environment_name, showinfo="messagebox", keyword="Knowledge Graph") == 0): 
                                copy_knowledge_graph(knowledge_graph_name, knowledge_graph_name_new, environment_name, showinfo="messagebox")
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Environment '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}'.")

                    '''
                    Save the knowledge graph to the knowledge graph folder
                    '''
                    def save_to_knowledge_graph(): 
                        knowledge_graph_export_path = os.path.join(DATA_PATH, "knowledge_graphs")
                        if (new_name_check(knowledge_graph_name, knowledge_graph_export_path, showinfo="messagebox", keyword="Knowledge Graph") == 0): 
                            shutil.copy(os.path.join(DATA_PATH, "environments", environment_name, knowledge_graph_name), os.path.join(knowledge_graph_export_path, knowledge_graph_name))
                            config.toggle_list_created = False; create_toggle_list()
                            show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully saved to the Knowledge Graph folder.")

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Rename", command = rename)
                    modify_menu_list.add_command(label="Delete", command = delete)
                    modify_menu_list.add_command(label="Make a Copy", command = copy)
                    modify_menu_list.add_command(label="Save the Graph", command = save_to_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)

                elif (self.toggle_info[1] == "knowledge_graphs"): 

                    def create_knowledge_graph_menu(): 
                        graph_name = simpledialog.askstring("Create Knowledge Graph", "Enter the name of the knowledge graph: ", parent = self.toggle_item_modify)
                        if graph_name:
                            graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
                            if (new_name_check(graph_name, graph_path, showinfo="messagebox", keyword="Knowledge Graph") == 0): 
                                create_knowledge_graph(graph_name)
                                config.toggle_list_created = False; create_toggle_list()
                                show_popup_message(f"Knowledge Graph '{graph_name}' successfully created.")

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Create a Knowledge Graph", command = create_knowledge_graph_menu)
                    modify_menu_list.post(event.x_root, event.y_root)
                
                elif (self.toggle_info[1].startswith("knowledge_graphs") and self.toggle_info[1].count('/') == 1): 
                    '''
                    Export the knowledge graph as a file
                    '''
                    def export_knowledge_graph(): 
                        pass

                    modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
                    modify_menu_list.add_command(label="Export for reuse", command = export_knowledge_graph)
                    modify_menu_list.post(event.x_root, event.y_root)
                self.menu_open = False
                self.toggle_item_modify.itemconfigure("modify", fill=color_tuple_to_rgb(config.default_grey_color))

            '''
            Click the item and change the focus
            '''
            def click_toggle_item(self, event): 

                config.toggle_selected = self.toggle_info[1]
                self.toggle_info[2][0] = not self.toggle_info[2][0]
                if (debug == 1): print (f"Change focus to {config.toggle_selected}")
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
                    self.toggle_item_modify = tk.Canvas(self, width=config.toggle_create_new_modify_width, height=config.toggle_create_new_modify_height, 
                                                bg=color_tuple_to_rgb(config.left_panel_color), highlightthickness=0, relief='ridge')
                    self.toggle_item_modify.pack (side = 'right', padx = 0, pady = 0)
                    self.toggle_item_modify.bind('<Configure>', self.configure_canvas_modify)
                    self.toggle_item_modify.bind("<Enter>", self.modify_hover)
                    self.toggle_item_modify.bind("<Leave>", self.modify_leave)
                    self.toggle_item_modify.bind("<Button-1>", self.modify_menu)

                self.label.pack (side = "top", fill = "x")
                if (config.toggle_selected == self.toggle_info[1]): 
                    self.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))
                    self.label.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))
                    if (self.toggle_info[1].startswith("knowledge_graphs") or self.toggle_info[1].startswith("environments")): 
                        self.toggle_item_modify.configure(bg=color_tuple_to_rgb(config.clicked_grey_color))

                self.configure(height=config.toggle_item_height, width=config.left_panel_width - config.left_panel_sidebar_width)
                self.bind("<Button-1>", self.click_toggle_item)
                self.label.bind("<Button-1>", self.click_toggle_item)

                '''
                WARNING Some platforms may use Button-3 instead
                '''
                if (True): 
                    self.bind("<Button-2>", self.modify_menu)
                    self.label.bind("<Button-2>", self.modify_menu)
                    self.toggle_item_modify.bind("<Button-2>", self.modify_menu)
        
        '''
        Creates the toggle list (for Environments, or Knowledge Graphs)
        '''
        def create_toggle_list_recursive(master, toggle_level, toggle_info): 

            if (toggle_info[3] != None): display_name = '  ' * toggle_level + ('▿  ' if toggle_info[2][0] else '▹  ') + toggle_info[0]
            else: display_name = '  ' * toggle_level + '   ' + toggle_info[0]
            if (toggle_info[1].startswith("environments") and toggle_info[1].count('/') == 1 and toggle_info[1].split('/')[1] == CURRENT_ENV): 
                display_name += " (*)"
            entry_frame = Toggle_Item(master, display_name, toggle_info, True if toggle_level == 0 else False)
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

            if (not config.toggle_list_created): 

                if (config.toggle_list): config.toggle_list.pack_forget()

                '''
                Generate the toggle environment name list
                Check whether the previous state is valid: Remove missed environments
                '''
                # from pprint import pprint
                # pprint (config.toggle_list_states)
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
                Generate the toggle knowledge graph list
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
                Add environment and knowledge graphs into the toggle list
                '''
                for name, value in config.toggle_list_states.items(): 
                    total_height += create_toggle_list_recursive(config.toggle_list, 0, value)
                    division_bar = tkinter.Frame (config.toggle_list, height = config.boundary_width, bg = color_tuple_to_rgb(config.boundary_grey_color))
                    division_bar.pack(anchor = 'n', fill = 'x')
                    total_height += config.boundary_width

                config.toggle_list.configure (height = total_height)
                config.toggle_list_created = True
            
            else: pass

        '''
        Resizes window event. 
        Toggle lists, and other elements will be recreated when appropriate. 
        '''
        def resize_window(): 
            if (debug == 0): print (f"Event triggered ({new_ID()}): {window.geometry()}")
            window_geometry = list(map(int, window.geometry().replace('x', ' ').replace('+', ' ').split(' ')))
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
            config.left_panel.configure (width = config.left_panel_width, height = config.window_height)
            config.left_panel_sidebar.configure (width = config.left_panel_sidebar_width)
            config.toggle_list.configure (width = config.left_panel_width - config.left_panel_sidebar_width)
            config.right_panel.configure (height = config.window_height)
            config.left_panel_change_arrow.place(x = config.left_panel_width - 3 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tkinter.SE)
            config.right_panel_change_arrow.place(x = 1 * config.boundary_width, y = config.window_height - 4 * config.boundary_width, anchor = tk.SW)

            '''
            Configure the environment and knowledge graph toggle lists
            '''
            create_toggle_list()

        '''
        Create the main window
        '''
        window = tkinter.Tk()
        window.title("RTSAI")
        if (debug == 0): print (f"sys.platform: {sys.platform}")
        if (sys.platform.startswith("darwin")): window.iconphoto(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png")))
        else: window.iconbitmap(False, ImageTk.PhotoImage(Image.open(f"{PACKAGE_PATH}/assets/images/RTSAI_logo_iconphoto.png"))) # to be tested
        window.geometry(f"{config.window_width}x{config.window_height}")
        window.maxsize(config.window_width_max, config.window_height_max)
        window.minsize(config.window_width_min, config.window_height_min)

        '''
        Create the window components
        '''
        create_left_panel()
        create_right_panel()
        config.toggle_list_created = False
        create_toggle_list()

        '''
        Starts running the main window
        '''
        window.bind("<Configure>", lambda event: resize_window())
        window.mainloop()

    elif (sys.argv[1] == "graph"): 

        if (len(sys.argv) < 3): 
            print ("Unknown command. ")
            return
            
        if (len(sys.argv) == 3 and sys.argv[2] == "list"): 
            '''
            List all the current knowledge graphs
            '''
            knowledge_graphs = os.listdir(os.path.join(DATA_PATH, "knowledge_graphs"))
            knowledge_graphs.sort()
            if knowledge_graphs:
                print("Current knowledge graphs:")
                for environment_name in knowledge_graphs:
                    print(environment_name)
            else:
                print("No knowledge graphs found.")

        if len(sys.argv) == 4 and sys.argv[2] == "create":
            '''
            Create a new knowledge graph
            '''
            graph_name = sys.argv[3]
            graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
            if (new_name_check(graph_name, graph_path, showinfo="print", keyword="Knowledge Graph") == 0): 
                create_knowledge_graph(graph_name)
                print(f"Knowledge Graph {graph_name} successfully created.")

        if len(sys.argv) == 5 and sys.argv[2] == "copy":
            '''
            Copy an existing knowledge graph to create a new knowledge graph
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
                    if (environment_name == CURRENT_ENV): print(f"{environment_name} (*)")
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
            Add knowledge graphs to an environment
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

