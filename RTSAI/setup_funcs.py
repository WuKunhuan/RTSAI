
import os, subprocess, shutil
from RTSAI.config import DATA_PATH, PACKAGE_PATH, PRE_INSTALLED_KG_PATH
from RTSAI.config import CURRENT_ENV, PRE_INSTALLED_KG, operating_system

debug = 1

KEY_CHARACTER = '$'         # The information is a key
PROTOTYPE_CHARACTER = '#'   # The information is a prototype
TOKEN_CHARACTER = '|'       # separate the information. Primarily used to avoid confusion. For example: HKU|[2] means the second named entity that shared the name HKU. 

NAMED_ENTITY_SYMBOL = f"{KEY_CHARACTER}NAMED_ENTITY"  # for update.tsv to use
PROTOTYPE_SYMBOL = f"{KEY_CHARACTER}PROTOTYPE"        # for update.tsv to use
RELATIONSHIP_SYMBOL = f"{KEY_CHARACTER}RELATIONSHIP"  # for update.tsv to use

OBJECT_KEY = f"{KEY_CHARACTER}OBJECT"              # root of every named entity
RELATIONSHIP_KEY = f"{KEY_CHARACTER}RELATIONSHIP"  # root of every relationship

object_id = 0
def new_object_id(): 
    global object_id; object_id += 1
    return object_id

def RTSAI_setup(): 
    '''
    RTSAI Package setup
    '''

    '''
    For MacOS: Remove .DS_Store
    '''
    if (operating_system() == "MacOS"): 
        ds_store_files = subprocess.Popen(["find", PACKAGE_PATH, "-name", ".DS_Store"], stdout = subprocess.PIPE).stdout.read().decode('utf-8').strip().split('\n')
        if (ds_store_files[0] != ""): 
            find_ds_store_result = len(ds_store_files)
            if (debug == 1): print (f"Find {find_ds_store_result} .DS_Store files at {PACKAGE_PATH}: {', '.join(ds_store_files)}. ")
        subprocess.run(["find", PACKAGE_PATH, "-name", ".DS_Store", "-delete"])

    '''
    Pre-installation of Knowledge Graph files
    '''
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        os.makedirs(os.path.join(DATA_PATH, "environments"))
        os.makedirs(os.path.join(DATA_PATH, "environments", CURRENT_ENV))
        knowledge_graphs_path = os.path.join(DATA_PATH, "knowledge_graphs")

        '''
        Copy pre-installed Knowledge Graphs to the "knowledge_graphs" folder
        '''
        for graph_name in PRE_INSTALLED_KG:
            src_dir = os.path.join(PRE_INSTALLED_KG_PATH, graph_name)
            dst_dir = os.path.join(knowledge_graphs_path, graph_name)
            shutil.copytree(src_dir, dst_dir)
    
    '''
    Check whether the current environment exists
    '''
    if (not os.path.exists(os.path.join(DATA_PATH, "environments", CURRENT_ENV))): 
        os.makedirs(os.path.join(DATA_PATH, "environments", CURRENT_ENV))

