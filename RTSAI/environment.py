
import os, shutil
from RTSAI.config import DATA_PATH
from RTSAI.tool_funcs import show_popup_message, new_name_check

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
