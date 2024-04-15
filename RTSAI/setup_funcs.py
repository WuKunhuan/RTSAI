
import os, subprocess, shutil
from RTSAI.config import DATA_PATH, PACKAGE_PATH, PRE_INSTALLED_KG_PATH
from RTSAI.config import CURRENT_ENV, PRE_INSTALLED_KG, operating_system

debug = 1

def RTSAI_setup(): 
    '''
    RTSAI Package setup
    '''

    '''
    For MacOS: Remove .DS_Store
    '''
    if (operating_system() == "MacOS"): 
        ds_store_files = subprocess.Popen(["find", PACKAGE_PATH, "-name", ".DS_Store"], stdout = subprocess.PIPE).stdout.read().decode('utf-8').strip().split('\n')
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
