
import os, re

from constants import ENV_PATH
from functions import convert_to_red, find_name_regex, print_error
from constants import CURRENT_ENV

## This function creates an RTSAI chat for the current environment
def create_chat(chat_name): 

    ## This function creates a RTSAI chat under the current environment

        ## Validate the environment name
        if (not re.match(r'^[a-zA-Z0-9_]+$', chat_name)):
            print(f"{convert_to_red('Error')}: Invalid RTSAI chat name. Please use only letters, numbers, and underscores.")
            return False

        ## Set the environment directory path
        chat_dir = f'{ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}'

        ## Check if the environment already exists
        if os.path.exists(chat_dir):
            overwrite = input(f"The RTSAI chat '{chat_name}' already exists for the {CURRENT_ENV} environment. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("RTSAI chat creation ended by the user [overwrite: FALSE]. ")
                return False

        # Create the environment directory with elevated privileges
        print (f"\nCreating RTSAI chat {chat_name} for the {CURRENT_ENV} environment, at {chat_dir} (password may required) ... ")
        os.system(f"sudo mkdir -p {chat_dir}")
        os.system(f"sudo chmod -R 755 {chat_dir}")
        print(f"SUCCESSFUL! ")
        return True

## This function lists all RTSAI chats under the current environment
def list_chats(): 

    ## Display all chats under the current environment
    print(f"\nChats for the {CURRENT_ENV} environment: ")
    chats = [name for name in os.listdir(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats") if os.path.isdir(os.path.join(f"{ENV_PATH}/envs/{CURRENT_ENV}", name))]
    if not chats: print("(None)\n"); 
    for chat in chats: 
        print(f"-   {chat}")
    print()

## This function lists all RTSAI chats under the current environment
def list_chat_graphs(chat_name): 

    ## Verify that the chat exists
    all_chats = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats", "\'*\'")
    if (chat_name not in all_chats): 
        print_error(f"chat name {chat_name} does not exist in the environment {CURRENT_ENV}! all chats: {all_chats}"); return
                
    ## Display all knowledge graphs of the chat
    print(f"\nKnowledge Graphs for the chat {chat_name} in the environment {CURRENT_ENV}: ")
    all_chat_graphs_env = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}", "\'*\'")
    print(f"\nShared within the {CURRENT_ENV} environment: ")
    if not all_chat_graphs_env: print("(None)\n"); 
    for graph in all_chat_graphs_env: 
        print(f"-   {graph}")
    print()
    all_chat_graphs_chat = find_name_regex(f"{ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}", "\'*\'")
    print(f"\nOnly for the {chat_name} chat: ")
    if not all_chat_graphs_chat: print("(None)\n"); 
    for graph in all_chat_graphs_chat: 
        print(f"-   {graph}")
    print()

## This function initializes a chat window
def chat(chat_name, selected_graphs, study_option): 
    print ("chat started ...")
    print ("chat ended ...")
    pass