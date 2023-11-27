
import subprocess
from constants import RED, RESET, DEBUG_MODE

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

## This function prints error message
def print_error(error_message): 
    print(f"{convert_to_red('Error')}: {error_message}")

## This function returns all names, in a location, match the regular expression
def find_name_regex(location, regex): 

    command = ["find", location, "-name", regex]
    if (DEBUG_MODE == 0): 
        print (f"find_name_regex command: {command}")

    ## Execute the command and capture the output
    output = subprocess.check_output(command).decode("utf-8")
    if (DEBUG_MODE == 0): 
        print (f"find_name_regex output: \'{output}\'")

    if (output == ''): 
        ## Nothing is returned
        return []
    else: 
        ## Split the output into individual lines
        lines = output.strip().split("\n")
        if (DEBUG_MODE == 0): 
            print (f"find_name_regex result: {lines}")

        ## Store the lines in a Python array
        return([line.strip() for line in lines])