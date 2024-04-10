
import os, shutil
from RTSAI.config import DATA_PATH, CURRENT_ENV, PRE_INSTALLED_KG, PRE_INSTALLED_KG_PATH

def RTSAI_setup(): 
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
        os.makedirs(os.path.join(DATA_PATH, "environments", CURRENT_ENV))
        knowledge_graphs_path = os.path.join(DATA_PATH, "knowledge_graphs")

        '''
        Copy pre-installed Knowledge Graphs to the "knowledge_graphs" folder
        '''
        for graph_name in PRE_INSTALLED_KG:
            src_dir = os.path.join(PRE_INSTALLED_KG_PATH, graph_name)
            dst_dir = os.path.join(knowledge_graphs_path, graph_name)
            shutil.copytree(src_dir, dst_dir)
