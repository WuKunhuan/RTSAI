
from constants import RED, RESET

## This function gets the manual of the RTSAI command
## reads the manual from specific location f"/Users/{user}/opt/RTSAI/man"
from constants import SYSTEM_USER
def get_manual(command):
    usage_file = f"/Users/{SYSTEM_USER}/opt/RTSAI/manuals/{command}.txt"
    try:
        with open(usage_file, 'r') as f: return f.read()
    except Exception: raise Exception

## This function indexes a list safely
def index_safe(l, id): 
    if (len(l) <= id): return None
    return (l[id])

## This function converts some text to red
def convert_to_red(text):
    return f"{RED}{text}{RESET}"