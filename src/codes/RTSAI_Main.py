import sys
import os
from RTSAI_env import create_env, list_envs

from constants import DEFAULT_ENVIRONMENT
from constants import RED, RESET

# 1. Global Variables

CURRENT_ENV = DEFAULT_ENVIRONMENT



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


    # 3.0 Perform installation check

    ## Verify if the binary exists
    ## Verify if the default environment exists
    ## Verify if the graph and 


    # 3.1 Handle the command : RTSAI
    ## This command display a Hello World message
    if (index_safe(sys.argv, 0) == 'RTSAI'): 
        if (len(index_safe(sys.argv, 0)) == 1): 
            print("Welcome to the world of RTSAI!")
    else: return 0



    # 3.2 Handle the environment command : RTSAI env

    ## An environment, is basically one set of contexts + pre-defined graphs
    ## you could think it as one user's chatgpt account
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

        ## Delete a environment
        if (index_safe(sys.argv, 2) == 'delete'): 
            if (len(sys.argv) == 4 and sys.argv[3] != 'default'): create_env(sys.argv[3])
            else: print(get_manual('env/create')); return
    


    # 3.3 Handle the chatbot command : RTSAI chat

    ## A chat, basically means generating some contexts as another (one or more) knowledge graphs
    ## Context + Prior = the agent's knowledge. 
    ## you could think it as one user's chatgpt chat
    elif (index_safe(sys.argv, 1) == 'chat'): 

        ## List all existing chats
        if (index_safe(sys.argv, 2) == 'list'): 
            pass

        ## Delete a chat
        elif (index_safe(sys.argv, 2) == 'delete'): 
            pass


        else: 

            ## --context : previous context provided
            ## --graph : specific knowledge graph(s) provided

            ## A name must be provided for the chat, cannot contain special characters, 
            ## it will be modified by the 

            ## only one context can be specified. 
            ## taken from the previous stored chat. 
            if ('--context' in sys.argv): 
                pass

            ## one or more graphs can be specified; 
            ## regular expression selector will be supported
            if ('--graph' in sys.argv): 
                pass

            ## specify this option to let the graphs able to be updated
            ## the change is pernament, deemed to be the knowledge acquired by the agent
            ## learn, may create new graphs, may merge graphs, etc. aiming to improve the topology
            if ('--learn' in sys.argv): 
                pass

    # 3.4 Handle the knowledge graph command : RTSAI graph

    ## basically, each graph is a CSV file, as defined in kgtk
    elif (index_safe(sys.argv, 1) == 'graph'): 

        ## graph query
        if (index_safe(sys.argv, 2) == 'query'): 

            ## can specify a graph to query, with -g option

            ## must specify the query, with -q option
            pass

        ## graph load
        if (index_safe(sys.argv, 2) == 'load'): 

            ## specify the graph name, followed by the resource name, in csv. 
            ## if the name exists, that means overriding
            ## if the name does not exist, that means overriding
            pass

        ## graph combine
        if (index_safe(sys.argv, 2) == 'combine'): 
            ## combine several graphs together into a folder (instead of merge them)
            pass

        ## graph divide
        if (index_safe(sys.argv, 2) == 'divide'): 
            ## divide a graph (must be in folder form; merged before) into its parts
            pass

        ## graph merge
        if (index_safe(sys.argv, 2) == 'merge'): 
            ## merge several CSV files, as specified. 
            ## -  Done by the agent. Conflict detection and management will be conducted. 
            ## -  an replacing flag "--replace" can be provided, to remove all previous graphs. 
            pass

        ## graph split
        if (index_safe(sys.argv, 2) == 'split'): 
            ## split a graph, automatically done by the agent. 
            ## this graph must be created by merge, which allows it to be splitted accordingly
            pass

        ## graph feed
        if (index_safe(sys.argv, 2) == 'feed'): 
            ## feed a graph and extend it according to the natural language input
            ## source of the feeding must be provided
            pass

        ## graph extract
        if (index_safe(sys.argv, 2) == 'extract'): 
            ## extract some knowlege to create a subgraph
            ## A description, stored in a .txt file, must be provided
            pass

        ## graph delete
        if (index_safe(sys.argv, 2) == 'delete'): 
            ## extract some knowlege to create a subgraph
            ## A description, stored in a .txt file, must be provided
            pass

        ## graph visualize
        if (index_safe(sys.argv, 2) == 'visualize'): 

            ## must specify a graph to visualize
            ## this function will be implemented via tkinter, if time allows
            pass


    else:
        print(f"{convert_to_red('Error')}: Invalid command! Enter 'man RTSAI' for the manual.")

if __name__ == '__main__':
    main()
