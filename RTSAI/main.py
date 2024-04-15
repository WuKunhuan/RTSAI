'''
Tasks: 
1. Import and Export functions
2. Revert the editing process. For key steps, define a function and have a space to store relevant files for recovery
3. Align Terminal and UI functions
4. Change the modify status area (remove it; replace it to the editor)
'''


import sys, os, math
import RTSAI.config as config
import RTSAI.UI_config as UI_config
import RTSAI.UI_components as UI_components
from RTSAI.counter import new_ID

debug = 1

def main(): 
    '''
    The main function handling both the UI and the Terminal Applications
    '''

    '''
    Run setup codes
    '''
    if (not (len(sys.argv) >= 1 and sys.argv[0] == f'{config.EXECUTABLE_PATH}/{config.COMMAND_NAME}')): return
    from RTSAI.setup_funcs import RTSAI_setup
    RTSAI_setup()

    if (len(sys.argv) == 1): 
        '''
        Create the RTSAI graphical window
        '''

        import tkinter
        from PIL import Image, ImageTk

        def configure_window(): 
            '''
            Resizes the main window. 
            Toggle lists, etc. will be rendered again when appropriate. 
            '''
            if (debug == 0): print (f"Configure window ... {new_ID()}")

            window_geometry = list(map(int, config.window.geometry().replace('x', ' ').replace('+', ' ').split(' ')))
            config.window_width = window_geometry[0]
            config.window_height = window_geometry[1]

            left_panel_width = int(UI_config.left_panel_relwidth * config.window_width)
            if (config.window_width >= UI_config.window_width_min and left_panel_width < UI_config.left_panel_width_min): 
                left_panel_width = UI_config.left_panel_width_min; 
                UI_config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                left_panel_width = int(UI_config.left_panel_relwidth * config.window_width)

            UI_config.left_panel_width = left_panel_width
            UI_config.right_panel_width = config.window_width - UI_config.left_panel_width - 4 * UI_config.boundary_width
            try: 
                UI_components.toggle_list.configure (width = UI_config.left_panel_width - UI_config.left_panel_sidebar_width)
                UI_components.left_panel_change_arrow.place(x = UI_config.left_panel_width - 3 * UI_config.boundary_width, y = config.window_height - 4 * UI_config.boundary_width, anchor = tkinter.SE)
                UI_components.right_panel_change_arrow.place(x = 1 * UI_config.boundary_width, y = config.window_height - 4 * UI_config.boundary_width, anchor = tkinter.SW)
            except: pass  # window already closed

        def create_left_panel(window):
            '''
            Create the left panel in the window
            '''

            from RTSAI.tool_funcs import color_tuple_to_rgb
            from RTSAI.UI_Editor_tabs import show_editor_tabbar, configure_editor
            from RTSAI.UI_Left_Toggle_List import create_toggle_list
            from RTSAI.UI_Left_Sidebar import create_left_sidebar

            def open_editor(tab_type, tab_value, tab_display_name): 
                UI_components.editor_states.append([tab_type, tab_value, tab_display_name])
                if (debug == 0): print (f"Tab '{tab_value}' ({tab_type}) opened. ")
                UI_components.current_editor_id = len(UI_components.editor_states) - 1
                UI_components.tabbar_shown = False; show_editor_tabbar()
                UI_components.editor_updated = False; configure_editor()

            def draw_left_panel_arrow(event):
                canvas_width = UI_components.left_panel_change_arrow.winfo_width()
                canvas_height = UI_components.left_panel_change_arrow.winfo_height()
                UI_components.left_panel_change_arrow.delete("arrow")
                arrow_coords = [
                    canvas_width * 0.9, canvas_height * 0.5,
                    canvas_width * 0.5, canvas_height * 0,
                    canvas_width * 0.5, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.25,
                    canvas_width * 0.1, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 1, 
                ]
                UI_components.left_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(UI_config.grey_color_64), tags="arrow")

            def resize_left_panel(event): 
                UI_config.left_panel_relwidth += 0.05
                if UI_config.left_panel_relwidth > UI_config.left_panel_relwidth_max:
                    UI_config.left_panel_relwidth = UI_config.left_panel_relwidth_max
                UI_config.left_panel_width = int(UI_config.left_panel_relwidth * config.window_width)
                UI_components.left_panel.configure(width=UI_config.left_panel_width)
                if (UI_components.editor_states): 
                    UI_components.tabbar_shown = False; show_editor_tabbar(tabbar_width = config.window_width - UI_config.left_panel_width - 4 * UI_config.boundary_width)

            def hover_left_panel_arrow(event):
                UI_components.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(UI_config.VSCode_highlight_color))

            def leave_left_panel_arrow(event):
                UI_components.left_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(UI_config.grey_color_64))

            '''
            Create the left panel background and bind events
            '''
            UI_components.left_panel = tkinter.Frame(window, bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightbackground=color_tuple_to_rgb(UI_config.grey_color_43), highlightthickness=UI_config.boundary_width)
            UI_components.left_panel.pack(side='left', fill='y')
            UI_components.left_panel_sidebar = tkinter.Frame(UI_components.left_panel, width=UI_config.left_panel_sidebar_width, bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightbackground=color_tuple_to_rgb(UI_config.grey_color_43), highlightthickness=UI_config.boundary_width)
            UI_components.left_panel_sidebar.pack(side="left", fill='y')
            UI_components.left_panel_main = tkinter.Frame(UI_components.left_panel, bg=color_tuple_to_rgb(UI_config.left_panel_color))
            UI_components.left_panel_main.pack(side="left", fill='both')

            UI_components.left_panel_change_arrow = tkinter.Canvas(UI_components.left_panel, width=UI_config.size_increase_arrow_width, height=UI_config.size_increase_arrow_height, bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness=0, relief='ridge')
            UI_components.left_panel_change_arrow.bind("<Enter>", hover_left_panel_arrow)
            UI_components.left_panel_change_arrow.bind("<Leave>", leave_left_panel_arrow)
            UI_components.left_panel_change_arrow.bind("<Configure>", draw_left_panel_arrow)
            UI_components.left_panel_change_arrow.bind("<Button-1>", resize_left_panel)

            UI_components.toggle_list_states = dict()
            UI_components.toggle_list_created = False; create_toggle_list()

            create_left_sidebar()
            UI_components.left_panel_sidebar_chat.bind("<Button-1>", lambda event: open_editor("CHAT", config.CURRENT_ENV, f"Chat: {config.CURRENT_ENV}"))
            UI_components.left_panel_sidebar_crawl.bind("<Button-1>", lambda event: open_editor("CRAWL", f"Web Crawl {new_ID()}", "Web Crawl"))

        def create_right_panel(window): 
            '''
            Create the right panel in the window
            '''

            from RTSAI.UI_Editor_tabs import show_editor_tabbar, configure_editor
            from RTSAI.tool_funcs import color_tuple_to_rgb

            def draw_right_panel_arrow(event):
                canvas_width = UI_components.right_panel_change_arrow.winfo_width()
                canvas_height = UI_components.right_panel_change_arrow.winfo_height()
                UI_components.right_panel_change_arrow.delete("arrow")
                arrow_coords = [
                    canvas_width * 0.1, canvas_height * 0.5,
                    canvas_width * 0.5, canvas_height * 0,
                    canvas_width * 0.5, canvas_height * 0.25,
                    canvas_width * 0.9, canvas_height * 0.25,
                    canvas_width * 0.9, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 0.75,
                    canvas_width * 0.5, canvas_height * 1
                ]
                UI_components.right_panel_change_arrow.create_polygon(arrow_coords, fill=color_tuple_to_rgb(UI_config.grey_color_64), tags="arrow")

            def resize_right_panel(event): 
                UI_config.left_panel_relwidth -= 0.05
                left_panel_width = int(UI_config.left_panel_relwidth * config.window_width)
                if (left_panel_width < UI_config.left_panel_width_min): 
                    left_panel_width = UI_config.left_panel_width_min; 
                    UI_config.left_panel_relwidth = math.ceil(left_panel_width * 100 / config.window_width) / 100
                    left_panel_width = int(UI_config.left_panel_relwidth * config.window_width)
                UI_config.left_panel_width = left_panel_width
                UI_components.left_panel.configure(width = UI_config.left_panel_width)
                if (UI_components.editor_states): 
                    UI_components.tabbar_shown = False; show_editor_tabbar(tabbar_width = config.window_width - UI_config.left_panel_width - 4 * UI_config.boundary_width)

            def arrow_hover(event):
                UI_components.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(UI_config.VSCode_highlight_color))

            def arrow_leave(event):
                UI_components.right_panel_change_arrow.itemconfigure("arrow", fill=color_tuple_to_rgb(UI_config.grey_color_64))

            UI_components.right_panel = tkinter.Frame(window, bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightbackground=color_tuple_to_rgb(UI_config.grey_color_43), highlightthickness=UI_config.boundary_width)
            UI_components.right_panel.pack(side='left', fill='both', expand=True)
            UI_components.right_panel_main = tkinter.Frame(UI_components.right_panel, bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightbackground=color_tuple_to_rgb(UI_config.grey_color_43), highlightthickness=UI_config.boundary_width)
            UI_components.right_panel_main.pack(side='top', fill='both', expand=True)
            UI_components.right_panel_main.bind("<Configure>", lambda event: configure_editor())
            UI_components.right_panel_change_arrow = tkinter.Canvas(UI_components.right_panel, width=UI_config.size_increase_arrow_width, height=UI_config.size_increase_arrow_height, bg=color_tuple_to_rgb(UI_config.right_panel_color), highlightthickness=0, relief='ridge')
            UI_components.right_panel_change_arrow.bind("<Enter>", arrow_hover)
            UI_components.right_panel_change_arrow.bind("<Leave>", arrow_leave)
            UI_components.right_panel_change_arrow.bind("<Configure>", draw_right_panel_arrow)
            UI_components.right_panel_change_arrow.bind("<Button-1>", resize_right_panel)

        '''
        Create the main window
        '''
        config.window = tkinter.Tk()
        config.window.title("RTSAI")
        
        if (config.operating_system() == "MacOS"): 
            config.window.iconphoto(False, ImageTk.PhotoImage(Image.open(f"{config.PACKAGE_PATH}/assets/images/avatars/RTSAI_avatar.png")))
        else: 
            ### TO BE COMPLETED (Tested)
            config.window.iconbitmap(False, ImageTk.PhotoImage(Image.open(f"{config.PACKAGE_PATH}/assets/images/avatars/RTSAI_avatar.png")))
        config.window.geometry(f"{UI_config.window_width}x{UI_config.window_height}")
        config.window.maxsize(UI_config.window_width_max, UI_config.window_height_max)
        config.window.minsize(UI_config.window_width_min, UI_config.window_height_min)

        '''
        Create the window components
        '''
        create_left_panel(config.window)
        create_right_panel(config.window)
        config.window.bind("<Configure>", lambda event: configure_window())

        '''
        Start the window loop
        '''
        config.window.mainloop()

    elif (sys.argv[1] == "graph"): 

        from RTSAI.knowledge_graph import create_knowledge_graph, copy_knowledge_graph

        if (len(sys.argv) < 3): 
            print ("Unknown command. ")
            return
            
        if (len(sys.argv) == 3 and sys.argv[2] == "list"): 
            '''
            List all the current Knowledge Graphs
            '''
            knowledge_graphs = os.listdir(os.path.join(config.DATA_PATH, "knowledge_graphs"))
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
            graph_path = os.path.join(config.DATA_PATH, "knowledge_graphs")
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

        from RTSAI.tool_funcs import new_name_check
        from RTSAI.environment import create_environment, copy_environment, environment_add_knowledge_graphs
        
        if (len(sys.argv) < 3): 
            print ("Unknown command. ")
            return
            
        if (len(sys.argv) == 3 and sys.argv[2] == "list"): 
            '''
            List all the current environments
            '''
            environments = os.listdir(os.path.join(config.DATA_PATH, "environments"))
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
            environment_path = os.path.join(config.DATA_PATH, "environments")
            if (new_name_check(environment_name, environment_path, showinfo="print", keyword="Environment") == 0): 
                create_environment(environment_name)
                print(f"Environment {environment_name} successfully created.")

        if len(sys.argv) >= 5 and sys.argv[2] == "add":
            '''
            Add Knowledge Graphs to an environment
            '''
            environment_name = sys.argv[3]
            graph_names = sys.argv[4:]
            environment_path = os.path.join(config.DATA_PATH, "environments", environment_name)
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
            existing_environment_path = os.path.join(config.DATA_PATH, "environments", existing_environment_name)
            copied_environment_path = os.path.join(config.DATA_PATH, "environments", copied_environment_name)
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

