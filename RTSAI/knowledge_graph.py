
import os, shutil
from RTSAI.config import DATA_PATH, ASSETS_PATH
from RTSAI.tool_funcs import show_popup_message, new_name_check

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
