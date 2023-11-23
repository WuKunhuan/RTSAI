import sys
import os

from RTSAI_env import create_env, list_envs
from RTSAI_chat import create_chat, list_chats, list_chat_graphs, chat

from constants import ENV_PATH
from constants import DEFAULT_ENV, CURRENT_ENV
from constants import RED, RESET

from functions import print_error, find_name_regex

# 1. Global Variables and Functions

from functions import get_manual, index_safe, convert_to_red

# 3. The Main function

## The main function handles RTSAI commands
def main():

    global CURRENT_ENV

    # 3.0 Perform installation check

    ## Verify if the binary exists
    ## Verify if the default environment exists
    ## Verify if the graph and 


    # 3.1 Handle the command : RTSAI
    ## This command display a Hello World message
    if (index_safe(sys.argv, 0) == 'RTSAI'): 
        if (len(sys.argv) == 1): 
            print("Welcome to the world of RTSAI!"); 
            return 0; 
    else: return 0



    # 3.2 Handle the environment command : RTSAI env

    ## An environment, is basically one set of contexts + pre-defined graphs
    ## you could think it as one user's chatgpt account
    if (index_safe(sys.argv, 1) == 'env'):

        ## List all environments
        if (index_safe(sys.argv, 2) == 'list'): 
            if (len(sys.argv) == 3): list_envs()
            else: print(get_manual('envs/list')); return

        ## Create a new environment
        if (index_safe(sys.argv, 2) == 'create'): 
            if (len(sys.argv) == 4): create_env(sys.argv[3])
            else: print(get_manual('envs/create')); return

        ## Activate an environment
        if (index_safe(sys.argv, 2) == 'activate'): 
            if (len(sys.argv) != 4): print(get_manual('envs/activate')); return
            if (os.path.expanduser(f'~/opt/RTSAI/envs/{index_safe(sys.argv, 3)}')): 
                CURRENT_ENV = index_safe(sys.argv, 3)
                print (f"RTSAI environment {index_safe(sys.argv, 3)} activated! ")
            else: print (f"{convert_to_red('Error')}: RTSAI environment {index_safe(sys.argv, 3)} does not exist! "); return  

        ## Deactivate an environment
        if (index_safe(sys.argv, 2) == 'deactivate'): 
            if (len(sys.argv) != 3): print(get_manual('envs/deactivate')); return
            CURRENT_ENV = 'default'

        ## Delete a environment
        if (index_safe(sys.argv, 2) == 'delete'): 
            if (len(sys.argv) == 4 and sys.argv[3] != 'default'): create_env(sys.argv[3])
            else: print(get_manual('envs/create')); return
    


    # 3.3 Handle the chatbot command : RTSAI chat

    ## A chat, basically means generating some contexts as another (one or more) knowledge graphs
    ## Context + Prior = the agent's knowledge. 
    ## you could think it as one user's chatgpt chat
    elif (index_safe(sys.argv, 1) == 'chat'): 

        ## List all existing chats
        if (index_safe(sys.argv, 2) == 'list'): 
            if (len(sys.argv) == 3): 
                list_chats()
            elif (len(sys.argv) == 5 and sys.argv[3] == "--graph"): 
                list_chat_graphs(sys.argv[4])
            else: print(get_manual('chats/list')); return

        ## Delete a chat
        elif (index_safe(sys.argv, 2) == 'delete'): 
            if (len(sys.argv) != 4): 
                print(get_manual('chats/delete')); return
            chat_name = sys.argv[3]
            all_chats = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats", "\'*\'")
            if (chat_name not in all_chats): 
                print_error(f"chat name {chat_name} does not exist in the environment {CURRENT_ENV}! all chats: {all_chats}"); return
            confirm = input(f"Confirm to delete chat {chat_name} from all chats: {all_chats}, in the environment {CURRENT_ENV}? (y/n): ")
            if confirm.lower() != 'y':
                print("RTSAI chat deletion ended by the user [confirm: FALSE]. ")
                return False
            print (f"Deleting the chat {chat_name} (password may required) ... ", end = "")
            if (not os.system(f"sudo rm -rf {ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}")): 
                print (f"SUCCESS! ")
            else: print (f"FAILED. ")

        ## Start new chat
        else: 

            ## --context : previous context provided
            ## --graph : specific knowledge graph(s) provided
            ## --learn : whether the agent can modify pernament memory

            chat_name = None
            selected_graphs = []
            study_option = False

            ## only one previous can be specified to load. 
            if ('--load' in sys.argv): 
                chat_index = sys.argv.index('--load')
                if (len(sys.argv) == chat_index + 1): 
                    print(get_manual('chats/default')); return
                chat_name = sys.argv[chat_index + 1]
                # need to ensure the chat is under all chats
                all_chats = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats", "\'*\'")
                if (chat_name not in all_chats): 
                    print_error(f"chat name {chat_name} does not exist in the environment {CURRENT_ENV}! all chats: {all_chats}"); return
                elif (len(sys.argv) > (chat_index + 2)) and sys.argv[chat_index + 2][0] != '-': 
                    print_error(f"only one chat is allowed to be loaded! (here at lest two: {sys.argv[chat_index + 1:chat_index + 3]})"); return
            else: 
                if (len(sys.argv) == 2): # argument: RTSAI chat
                    print(get_manual('chats/default')); return
                else: 
                    chat_name = sys.argv[2]
                    if (not create_chat(chat_name)): return


            ## one or more graphs can be specified; 
            ## regular expression selector will be supported
            if ('--graph' in sys.argv): 
                graph_index = sys.argv.index('--graph')
                for i in range (graph_index, len(sys.argv)): 
                    if (sys.argv[i][0] == '-'): break
                    else: selected_graphs.append(sys.argv[i])
                if (not selected_graphs): 
                    print_error(f"--graph option with no graph selected! "); return
                ## Find all graphs for the environment, and the chat itself
                available_graphs_env = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/graphs", "__graph_*")
                available_graphs_chat = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}", "__graph_*")
                invalid_graphs = []
                for graph in selected_graphs: 
                    if ((graph not in available_graphs_env) and (graph not in available_graphs_chat)): 
                        invalid_graphs.append(graph)
                if (invalid_graphs): 
                    print_error(f"graphs {invalid_graphs} selected not valid! \nall valid graphs for the {CURRENT_ENV} environment (shared): {available_graphs_env}\nall valid graphs for the {chat_name} chat: {available_graphs_chat}"); return


            ## specify this option to let the graphs able to be updated
            ## the change is pernament, deemed to be the knowledge acquired by the agent
            ## learn, may create new graphs, may merge graphs, etc. aiming to improve the topology
            if ('--learn' in sys.argv): 
                study_option = True
            
            chat(chat_name, selected_graphs, study_option)



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
