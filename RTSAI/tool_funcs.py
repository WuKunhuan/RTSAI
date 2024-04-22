
import os, re
from RTSAI.config import DATA_PATH
from RTSAI.UI_funcs import show_popup_message

def color_tuple_to_rgb(color_tuple): 
    '''
    Convert color tuples to rgb string
    '''
    return ("#%02x%02x%02x" % color_tuple)

def new_name_check(name, path = DATA_PATH, showinfo = "print", keyword = "", max_length = 30, parent_item = None): 
    '''
    Check whether creating a file/folder with the name under the path is valid
    '''
    try: 
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
    except: return 1
