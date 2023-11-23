import sys
import os
from RTSAI_env import create_env, list_envs

# 1. Global Variables
CURRENT_ENV = "default"
RED = "\033[91m"
RESET = "\033[0m"

# 2. Functions

## This function gets the manual of the RTSAI command
## reads the manual from specific location f"/Users/{user}/opt/RTSAI/man"
user = os.getenv('USER')
def get_manual(command):
    usage_file = f"/Users/{user}/opt/RTSAI/man/{command}.txt"
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

# 3. The Main function

## The main function handles RTSAI commands
def main():

    # 3.1 Handle the command : RTSAI
    ## This command display a Hello World message
    if (index_safe(sys.argv, 0) == 'RTSAI'): 
        if (len(index_safe(sys.argv, 0)) == 1): 
            print("Welcome to the world of RTSAI!")
    else: return 0

    # 3.2 Handle the environment command : RTSAI env
    if (index_safe(sys.argv, 1) == 'env'):

        ## List all environments
        if (index_safe(sys.argv, 2) == 'list'): 
            if (len(sys.argv) == 3): list_envs()
            else: print(get_manual('env/list')); return

        ## Create a new environment
        if (index_safe(sys.argv, 2) == 'create'): 
            if (len(sys.argv) == 4): create_env(sys.argv[3])
            else: print(get_manual('env/create')); return

        ## Activate an environment
        if (index_safe(sys.argv, 2) == 'activate'): 
            if (len(sys.argv) != 4): print(get_manual('env/activate')); return
            if (os.path.expanduser(f'~/opt/RTSAI/env/{index_safe(sys.argv, 3)}')): 
                global CURRENT_ENV
                CURRENT_ENV = index_safe(sys.argv, 3)
                print (f"RTSAI environment {index_safe(sys.argv, 3)} activated! ")
            else: print (f"{convert_to_red('Error')}: RTSAI environment {index_safe(sys.argv, 3)} does not exist! "); return  

        ## Deactivate an environment
        if (index_safe(sys.argv, 2) == 'deactivate'): 
            if (len(sys.argv) != 3): print(get_manual('env/deactivate')); return
            global CURRENT_ENV
            CURRENT_ENV = 'default'
    
    # 3.3 Handle the chatbot command : RTSAI chat
    elif (index_safe(sys.argv, 1) == 'chat'): 

        ## --context : previous context provided
        ## --graph : specific knowledge graph(s) provided

        ## only one context can be specified
        if ('--context' in sys.argv): 
            pass

        ## one or more graphs can be specified; 
        ## regular expression selector will be supported
        if ('--graph' in sys.argv): 
            pass

    # 3.4 Handle the knowledge graph command : RTSAI graph

    ## basically, each graph is a CSV file, as defined in kgtk
    elif (index_safe(sys.argv, 1) == 'graph'): 

        ## graph query
        if (index_safe(sys.argv, 2) == 'query'): 

            ## can specify a graph to query, with -g option

            ## must specify the query, with -q option, 
            pass

        ## graph visualize
        if (index_safe(sys.argv, 2) == 'visualize'): 

            ## must specify 
            pass

        ## graph load
        if (index_safe(sys.argv, 2) == 'load'): 

            ## specify the graph name, followed by the resource name, in csv
            ## if the name exists, that means overriding
            ## if the name does not exist, that means overriding
            pass

        ## graph merge


        ## graph save

        ## graph delete


    else:
        print(f"{convert_to_red('Error')}: Invalid command! Enter 'man RTSAI' for the manual.")

if __name__ == '__main__':
    main()
