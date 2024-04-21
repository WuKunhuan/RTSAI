
import tkinter, os, shutil
from tkinter import simpledialog, messagebox, Listbox
import RTSAI.config as config
import RTSAI.UI_config as UI_config
import RTSAI.UI_components as UI_components
from RTSAI.tool_funcs import show_popup_message, new_name_check, color_tuple_to_rgb
from RTSAI.environment import create_environment, copy_environment, environment_add_knowledge_graphs, environment_rename_knowledge_graph
from RTSAI.knowledge_graph import create_knowledge_graph, copy_knowledge_graph

debug = 1

'''
Knowledge Graph menu operations
'''
def create_knowledge_graph_menu(graph_name = None, query = "Enter the name of the Knowledge Graph: ", parent = UI_components.window): 
    '''
    Create a knowledge graph from the menu. 
    '''
    if (not graph_name): 
        graph_name = simpledialog.askstring("Create Knowledge Graph", query, parent = parent)
    if graph_name:
        graph_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
        if (new_name_check(graph_name, graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = parent) == 0): 
            create_knowledge_graph(graph_name)
            UI_components.toggle_list_created = False; create_toggle_list()
            show_popup_message(f"Knowledge Graph '{graph_name}' successfully created.", parent_item = parent)

def import_knowledge_graph_menu(parent = UI_components.window): 
    '''
    '''
    pass


class Left_Panel_Toggle_Item(tkinter.Frame): 
    '''
    Toggle Item class objects in the left panel main
    '''

    def configure_canvas_modify(self, event): 
        '''
        Generates the modify sign. 
        '''
        canvas_width = UI_config.toggle_modify_width
        canvas_height = UI_config.toggle_modify_height
        self.toggle_item_modify.delete("modify")
        self.toggle_item_modify.config(width=canvas_width, height=canvas_height)
        self.toggle_item_modify.create_oval(canvas_width * 0.25, canvas_height * 0.25, canvas_height * 0.75, canvas_height * 0.75, fill=color_tuple_to_rgb(UI_config.grey_color_64), tags="modify", outline = color_tuple_to_rgb(UI_config.left_panel_color))

    def operate_toggle_item(self, event, key_pressed = None): 
        '''
        Display the menu when right clicking the toggle item. 
        '''

        if (key_pressed == "<BackSpace>" and ((self.toggle_info[1] != UI_components.toggle_item_on_focus) or ('/' not in self.toggle_info[1]))): return

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
                    environment_path = os.path.join(config.DATA_PATH, "environments")
                    if (new_name_check(environment_name, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                        create_environment(environment_name)
                        UI_components.toggle_list_created = False; create_toggle_list()
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
                    environment_path = os.path.join(config.DATA_PATH, "environments")
                    if (new_name_check(environment_name_new, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                        if (create_environment(environment_name_new, environment_name, showinfo="messagebox") == 0): 
                            if (environment_name == config.CURRENT_ENV): 
                                config.CURRENT_ENV = environment_name_new
                            UI_components.toggle_list_created = False; create_toggle_list()
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
                        environment_path = os.path.join(config.DATA_PATH, "environments")
                        try:
                            shutil.rmtree(os.path.join(environment_path, environment_name))
                            UI_components.toggle_list_created = False; create_toggle_list()
                            show_popup_message(f"Environment '{environment_name}' successfully deleted.", parent_item = self)
                        except OSError:
                            messagebox.showerror("Environment Deletion Failed", f"Environment '{environment_name}' deletion FAILED.", parent = self)

            def copy_environment_menu(): 
                '''
                Copy the Environment
                '''
                environment_name_new = simpledialog.askstring("Copy Environment", f"Enter the copy name of the Environment '{environment_name}': ", parent = self)
                if environment_name_new:
                    environment_path = os.path.join(config.DATA_PATH, "environments")
                    if (new_name_check(environment_name_new, environment_path, showinfo="messagebox", keyword="Environment", parent_item = self) == 0): 
                        copy_environment(environment_name, environment_name_new, showinfo="messagebox")
                        UI_components.toggle_list_created = False; create_toggle_list()
                        show_popup_message(f"Environment '{environment_name}' successfully copied as '{environment_name_new}'.", parent_item = self)

            def set_as_current_environment(): 
                '''
                Set the Environment as the Current Environment
                '''
                config.CURRENT_ENV = environment_name
                UI_components.toggle_list_created = False; create_toggle_list()
                show_popup_message(f"Environment '{environment_name}' successfully set as the Current Environment.", parent_item = self)

            def add_knowledge_graphs(): 
                '''
                Add Knowledge Graphs to the Environment
                '''
                select_knowledge_graph_window = tkinter.Toplevel(self)
                select_knowledge_graph_window.title(f"Select Knowledge Graphs for the Environment '{environment_name}'")
                select_knowledge_graph_window.resizable(width = False, height = False)
                knowledge_graph_names = os.listdir(os.path.join(config.DATA_PATH, "knowledge_graphs")) 
                knowledge_graph_names.sort (key = lambda name: name.lower())
                knowledge_graph_names_current = os.listdir(os.path.join(config.DATA_PATH, self.toggle_info[1])) 
                knowledge_graph_names = [name for name in knowledge_graph_names if name not in knowledge_graph_names_current]
                knowledge_graph_list = None

                if (not knowledge_graph_names): select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"No Knowledge Graphs are available! ", font = (UI_config.standard_font_family, int(UI_config.standard_font_size * 1.2)), padx = 10, pady = 10); return

                if (len(knowledge_graph_names) > 12): 
                    select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. \nPlease scroll down to see the full list ({len(knowledge_graph_names)} items). ", font = (UI_config.standard_font_family, int(UI_config.standard_font_size * 1.2)), padx = 10, pady = 10)
                    select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                else: 
                    select_knowledge_graph_prompt = tkinter.Label(select_knowledge_graph_window, text = f"Select all Knowledge Graphs to be added from the below list. ", font = (UI_config.standard_font_family, int(UI_config.standard_font_size * 1.2)), padx = 10, pady = 10)
                    select_knowledge_graph_prompt.pack(side = "top", anchor = "n")
                
                select_knowledge_graph_frame = tkinter.Frame(select_knowledge_graph_window, bg = color_tuple_to_rgb(UI_config.left_panel_color))
                select_knowledge_graph_frame.pack(side = "top", anchor = "n", fill = "both", padx = 10, pady = 0)
                knowledge_graph_list = Listbox(select_knowledge_graph_frame, selectmode = "multiple", 
                                            bg = color_tuple_to_rgb(UI_config.left_panel_color), 
                                            fg = color_tuple_to_rgb(UI_config.VSCode_font_grey_color), 
                                            selectbackground = color_tuple_to_rgb(UI_config.VSCode_highlight_color), 
                                            selectforeground = color_tuple_to_rgb(UI_config.left_panel_color), 
                                            font = (UI_config.standard_font_family, UI_config.standard_font_size), 
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
                    UI_components.toggle_list_created = False; create_toggle_list()
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
                        UI_components.toggle_list_created = False; create_toggle_list()
                        show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}' inside Environment '{environment_name}'.", parent_item = self)

            def delete_knowledge_graph(): 
                '''
                Delete the Knowledge Graph inside an environment
                '''
                confirm = messagebox.askyesno("Confirm Knowledge Graph Deletion", f"Are you sure you want to delete the Knowledge Graph '{knowledge_graph_name}'?", parent = self)
                if confirm:
                    knowledge_graph_path = os.path.join(config.DATA_PATH, "environments", environment_name, knowledge_graph_name)
                    try:
                        shutil.rmtree(knowledge_graph_path)
                        UI_components.toggle_list_created = False; create_toggle_list()
                        show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' inside Environment {environment_name} successfully deleted.", parent_item = self)
                    except OSError:
                        messagebox.showerror("Knowledge Graph Deletion Failed", f"Knowledge Graph '{knowledge_graph_name}' inside Environment '{environment_name}' deletion FAILED.", parent = self)

            def copy_knowledge_graph_menu(): 
                '''
                Copy the Knowledge Graph inside an environment
                '''
                knowledge_graph_name_new = simpledialog.askstring("Rename Knowledge Graph", f"Enter the copy name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                if knowledge_graph_name_new:
                    knowledge_graph_path = os.path.join(config.DATA_PATH, "environments", environment_name)
                    if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                        if (copy_knowledge_graph(knowledge_graph_name, knowledge_graph_name_new, environment_name, showinfo="messagebox", parent_item = self) == 0): 
                            UI_components.toggle_list_created = False; create_toggle_list()
                            show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully copied as '{knowledge_graph_name_new}'.", parent_item = self)
                        else: show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' copy FAILED.", parent_item = self)

            def save_to_knowledge_graph(): 
                '''
                Save the Knowledge Graph to the Knowledge Graph folder
                '''
                knowledge_graph_export_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
                if (new_name_check(knowledge_graph_name, knowledge_graph_export_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                    shutil.copytree(os.path.join(config.DATA_PATH, "environments", environment_name, knowledge_graph_name), os.path.join(knowledge_graph_export_path, knowledge_graph_name))
                    UI_components.toggle_list_created = False; create_toggle_list()
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

            modify_menu_list = tkinter.Menu(self.toggle_item_modify, tearoff=0)
            modify_menu_list.add_command(label="Create a Knowledge Graph", command = create_knowledge_graph_menu(self))
            modify_menu_list.add_command(label="Import a Knowledge Graph (to be completed)", command = import_knowledge_graph_menu(self))
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
                    knowledge_graph_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
                    if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                        if (create_knowledge_graph(knowledge_graph_name_new, knowledge_graph_name, showinfo="messagebox") == 0): 
                            UI_components.toggle_list_created = False; create_toggle_list()
                            show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully renamed to '{knowledge_graph_name_new}'.", parent_item = self)
                    else: show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' rename FAILED.", parent_item = self)

            def delete_knowledge_graph(): 
                '''
                Delete the Knowledge Graph
                '''
                confirm = messagebox.askyesno("Confirm Knowledge Graph Deletion", f"Are you sure you want to delete the Knowledge Graph '{knowledge_graph_name}'?", parent = self)
                if confirm:
                    knowledge_graph_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
                    try:
                        shutil.rmtree(os.path.join(knowledge_graph_path, knowledge_graph_name))
                        UI_components.toggle_list_created = False; create_toggle_list()
                        show_popup_message(f"Knowledge Graph '{knowledge_graph_name}' successfully deleted.", parent_item = self)
                    except OSError:
                        messagebox.showerror("Knowledge Graph Deletion Failed", f"Knowledge Graph '{knowledge_graph_name}' deletion FAILED.", parent = self)

            def copy_knowledge_graph_menu(): 
                '''
                Copy the Knowledge Graph
                '''
                knowledge_graph_name_new = simpledialog.askstring("Copy Knowledge Graph", f"Enter the copy name of the Knowledge Graph '{knowledge_graph_name}': ", parent = self)
                if knowledge_graph_name_new:
                    knowledge_graph_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
                    if (new_name_check(knowledge_graph_name_new, knowledge_graph_path, showinfo="messagebox", keyword="Knowledge Graph", parent_item = self) == 0): 
                        copy_knowledge_graph(knowledge_graph_name, knowledge_graph_name_new, showinfo="messagebox", parent_item = self)
                        UI_components.toggle_list_created = False; create_toggle_list()
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
        self.bind("<BackSpace>", lambda event: self.operate_toggle_item(event, key_pressed = "<BackSpace>"))
        '''
        Set the current focus to Toggle List -> Current Item
        '''
        self.focus_set()
        if (UI_components.toggle_item_on_focus == self.toggle_info[1]): 
            UI_components.toggle_list_created = False; create_toggle_list()
            self.operate_toggle_item(event)
        else: 
            UI_components.toggle_item_on_focus = self.toggle_info[1]
            UI_components.toggle_list_created = False; create_toggle_list()
            if (debug == 0): print (f"Change focus to {self.toggle_info[1]}")

    def __init__(self, master, toggle_display_name, toggle_info, bold=False):

        super().__init__(master, bg=color_tuple_to_rgb(UI_config.left_panel_color))
        self.pack_propagate(False)
        self.toggle_info = toggle_info
        self.menu_open = False
        self.label = tkinter.Label(self, text=toggle_display_name, font=(UI_config.standard_font_family, UI_config.standard_font_size, "bold" if bold else "normal"), anchor = "w", 
                            fg=color_tuple_to_rgb(UI_config.VSCode_font_grey_color), bg=color_tuple_to_rgb(UI_config.left_panel_color), 
                            relief="flat", borderwidth=0)
        if (self.toggle_info[1].startswith("knowledge_graphs") or (self.toggle_info[1].startswith("environments"))): 
            self.toggle_item_modify = tkinter.Canvas(self, width=UI_config.toggle_modify_width, height=UI_config.toggle_modify_height, 
                                        bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness=0, relief='ridge')
            self.toggle_item_modify.pack (side = 'right', padx = 0, pady = 0)
            self.toggle_item_modify.bind('<Configure>', self.configure_canvas_modify)
            self.toggle_item_modify.bind("<Button-1>", self.operate_toggle_item)

        self.label.pack (side = "top", fill = "x")
        if (UI_components.toggle_item_on_focus == self.toggle_info[1]): 
            self.configure(bg=color_tuple_to_rgb(UI_config.grey_color_51))
            self.label.configure(bg=color_tuple_to_rgb(UI_config.grey_color_51))
            if (self.toggle_info[1].startswith("knowledge_graphs") or self.toggle_info[1].startswith("environments")): 
                self.toggle_item_modify.configure(bg=color_tuple_to_rgb(UI_config.grey_color_51))

        self.configure(height=UI_config.toggle_item_height, width=UI_config.left_panel_width - UI_config.left_panel_sidebar_width)
        self.bind("<Button-1>", self.click_toggle_item)
        self.label.bind("<Button-1>", self.click_toggle_item)

        '''
        WARNING Some platforms may use Button-3 instead
        TO BE COMPLETED / VERIFIED
        '''
        if (True): 
            self.bind("<Button-2>", self.operate_toggle_item)
            self.label.bind("<Button-2>", self.operate_toggle_item)
            self.toggle_item_modify.bind("<Button-2>", self.operate_toggle_item)

def create_toggle_list_recursive(master, toggle_level, toggle_info): 
    '''
    Recursively create a sub toggle list
    '''

    if (toggle_info[3] != None): display_name = '  ' * toggle_level + ('▿  ' if toggle_info[2][0] else '▹  ') + toggle_info[0]
    else: display_name = '  ' * toggle_level + '   ' + toggle_info[0]
    if (toggle_info[1].startswith("environments") and toggle_info[1].count('/') == 1 and toggle_info[1].split('/')[1] == config.CURRENT_ENV): 
        display_name += " (*)"
    entry_frame = Left_Panel_Toggle_Item(master, display_name, toggle_info, True if toggle_level == 0 else False)
    entry_frame.pack_propagate(False)
    entry_frame.pack(anchor = "n", fill = 'x', expand = True, pady=0)
    total_height = UI_config.toggle_item_height
    if (toggle_info[2][0] and toggle_info[3] != None): 
        toggle_child = list(toggle_info[3].keys())
        toggle_child.sort(key = lambda item: item.lower())
        for name in toggle_child: 
            toggle_child_list = toggle_info[3][name]
            total_height += create_toggle_list_recursive(master, toggle_level + 1, toggle_child_list)
    entry_frame.configure (height = UI_config.toggle_item_height)
    return total_height

def create_toggle_list(): 
    '''
    Create the toggle list under the left panel
    '''

    if (UI_components.toggle_list_created): return
    if (UI_components.toggle_list): UI_components.toggle_list.pack_forget()

    '''
    Generate the toggle environment name list
    Check whether the previous state is valid: Remove missed environments
    '''
    environment_dict = dict()
    if ("environments" in UI_components.toggle_list_states): 
        environment_dict = UI_components.toggle_list_states["environments"][3]
    previous_environment_names = list(environment_dict.keys())
    for environment_name in previous_environment_names: 
        if (not os.path.exists(os.path.join(config.DATA_PATH, "environments", environment_name))): 
            del(environment_dict[environment_name]); continue
        environment_knowkedge_graphs = list(environment_dict[environment_name][3].keys())
        for knowledge_graph_name in environment_knowkedge_graphs: 
            if (not os.path.exists(os.path.join(config.DATA_PATH, "environments", environment_name, knowledge_graph_name))): 
                del(environment_dict[environment_name][3][knowledge_graph_name]); continue
    environment_names = os.listdir(os.path.join(config.DATA_PATH, "environments")) 
    environment_names.sort (key = lambda name: name.lower())
    for environment_name in environment_names: 
        '''
        Toggle List Structure: 
        -  name
        -  value
        -  [toggle status, "edit status"]
        -  toggle items
        '''
        if (not environment_name in environment_dict): 
            environment_dict[environment_name] = [environment_name, f"environments/{environment_name}", [False, None], dict()] 
        knowledge_graph_names = os.listdir(os.path.join(config.DATA_PATH, "environments", environment_name)) 
        knowledge_graph_names.sort (key = lambda name: name.lower())
        for knowledge_graph_name in knowledge_graph_names: 
            if (not knowledge_graph_name in environment_dict[environment_name][3]): 
                environment_dict[environment_name][3][knowledge_graph_name] = [f"KG: {knowledge_graph_name}", f"environments/{environment_name}/{knowledge_graph_name}", [False, "saved"], None]
    if ("environments" not in UI_components.toggle_list_states): 
        UI_components.toggle_list_states["environments"] = ["ENVIRONMENTS", "environments", [True, None], environment_dict]

    '''
    Generate the toggle Knowledge Graph list
    '''
    knowledge_graph_dict = dict()
    if ("knowledge_graphs" in UI_components.toggle_list_states): 
        knowledge_graph_dict = UI_components.toggle_list_states["knowledge_graphs"][3]
    previous_knowledge_graph_names = list(knowledge_graph_dict.keys())
    for knowledge_graph_name in previous_knowledge_graph_names: 
        if (not os.path.exists(os.path.join(config.DATA_PATH, "knowledge_graphs", knowledge_graph_name))): 
            del(knowledge_graph_dict[knowledge_graph_name]); continue
    knowledge_graph_names = os.listdir(os.path.join(config.DATA_PATH, "knowledge_graphs")) 
    knowledge_graph_names.sort (key = lambda name: name.lower())
    for knowledge_graph_name in knowledge_graph_names: 
        ## Toggle List Structure: name, value, [toggle status, "edit status"], toggle items
        if (not knowledge_graph_name in knowledge_graph_dict): 
            knowledge_graph_dict[knowledge_graph_name] = [knowledge_graph_name, f"knowledge_graphs/{knowledge_graph_name}", [False, "saved"], None]
    if ("knowledge_graphs" not in UI_components.toggle_list_states): 
        UI_components.toggle_list_states["knowledge_graphs"] = ["KNOWLEDGE GRAPHS", "knowledge_graphs", [True, None], knowledge_graph_dict]

    '''
    The toggle list stays on the top, expanding in the x direction
    '''
    UI_components.toggle_list = tkinter.Frame(UI_components.left_panel_main, bg=color_tuple_to_rgb(UI_config.VSCode_highlight_color))
    UI_components.toggle_list.pack(anchor="n", fill="both", expand = True)
    UI_components.toggle_list.pack_propagate(False)
    
    '''
    Add environment and Knowledge Graphs into the toggle list
    '''
    left_panel_main_bottom_arrow_area = tkinter.Canvas(UI_components.toggle_list, height = UI_config.size_increase_arrow_height + 8 * UI_config.boundary_width, 
                                        bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness = 0, relief='ridge')
    left_panel_main_bottom_arrow_area.pack(side="bottom", fill="x")
    temp_canvas = tkinter.Canvas(UI_components.toggle_list, bg = color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness=0, relief='ridge'); 
    temp_canvas.pack(side="top", fill="both", expand=True)
    temp_frame = tkinter.Frame(temp_canvas, highlightthickness=0, relief='ridge')
    temp_canvas.create_window((0, 0), window=temp_frame, anchor="nw", tags="temp_frame")
    total_height = 0
    if (debug == 0): print (UI_components.toggle_list_states) 
    for name, value in UI_components.toggle_list_states.items(): 
        total_height += create_toggle_list_recursive(temp_frame, 0, value)
        division_bar = tkinter.Frame (temp_frame, height = UI_config.boundary_width, bg = color_tuple_to_rgb(UI_config.grey_color_43))
        division_bar.pack(anchor = 'n', fill = 'x')
        total_height += UI_config.boundary_width

    '''
    Create the scrollbar, when applicable
    '''
    if (UI_components.left_panel.winfo_height() != 1 and total_height > config.window_height - UI_config.size_increase_arrow_height): 
        if (UI_components.left_panel_main_scrollbar): 
            UI_components.left_panel_main_scrollbar.pack_forget()
        UI_components.left_panel_main_scrollbar = tkinter.Scrollbar(temp_canvas, orient="vertical", command=temp_canvas.yview, width = UI_config.left_panel_main_scrollbar_width)
        temp_canvas.configure(yscrollcommand = UI_components.left_panel_main_scrollbar.set)
        UI_components.left_panel_main_scrollbar.pack(side='right', fill='y')
        UI_components.toggle_list_scrollbar_created = True

        if (UI_components.left_panel_main_scrollbar_position): 
            position = UI_components.left_panel_main_scrollbar_position
            temp_canvas.after(100, lambda: temp_canvas.yview_moveto(position[0]))
        def left_panel_main_scrollbar_save_scroll_position(): 
            UI_components.left_panel_main_scrollbar_position = UI_components.left_panel_main_scrollbar.get()
        UI_components.left_panel_main_scrollbar.bind("<Motion>", lambda event: left_panel_main_scrollbar_save_scroll_position())

    def toggle_list_configure(event): 
        temp_canvas.configure(scrollregion=temp_canvas.bbox("all"))
        if (UI_components.left_panel.winfo_height() != 1 and total_height > config.window_height - UI_config.size_increase_arrow_height): 
            temp_canvas.itemconfigure("temp_frame", width=temp_canvas.winfo_width() - UI_config.left_panel_main_scrollbar_width)
        else: temp_canvas.itemconfigure("temp_frame", width=temp_canvas.winfo_width())
        
        tabbar_height_new = config.window_height - UI_config.size_increase_arrow_height
        if (total_height <= tabbar_height_new and UI_components.left_panel_main_scrollbar): 
            UI_components.left_panel_main_scrollbar.pack_forget(); 
            UI_components.left_panel_main_scrollbar = None
            UI_components.toggle_list_scrollbar_created = False
            UI_components.left_panel_main_scrollbar_position = None
        elif (total_height > tabbar_height_new and not UI_components.toggle_list_scrollbar_created): 
            UI_components.toggle_list_scrollbar_created = True
            UI_components.toggle_list_created = False; create_toggle_list()

    temp_frame.bind("<Configure>", toggle_list_configure)
    UI_components.toggle_list_created = True
