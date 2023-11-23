
import os

from constants import ENV_PATH
from functions import convert_to_red
from constants import CURRENT_ENV

## This function creates an RTSAI chat for the current environment
def create_chat(chat_name): 

    ## This function creates a RTSAI chat under the current environment

        ## Validate the environment name
        if not re.match(r'^[a-zA-Z0-9_]+$', chat_name):
            print(f"{convert_to_red('Error')}: Invalid RTSAI chat name. Please use only letters, numbers, and underscores.")
            return

        ## Set the environment directory path
        chat_dir = f'{ENV_PATH}/envs/{CURRENT_ENV}/chats/{chat_name}'

        ## Check if the environment already exists
        if os.path.exists(chat_dir):
            overwrite = input(f"The RTSAI chat '{chat_name}' already exists for the {CURRENT_ENV} environment. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("RTSAI chat creation ended by the user [overwrite: FALSE]. ")
                return

        # Create the environment directory with elevated privileges
        print (f"\nCreating RTSAI chat {chat_name} for the {CURRENT_ENV} environment, at {chat_dir} (password may required) ... ")
        os.system(f"sudo mkdir -p {chat_dir}")
        os.system(f"sudo chmod -R 755 {chat_dir}")
        print(f"SUCCESSFUL! ")

## This function lists all RTSAI chats under the current environment
def list_chats(): 

    ## Verify the current environment exists
    env_dir = f"{ENV_PATH}/envs/{CURRENT_ENV}"
    if not os.path.exists(env_dir):
        print(f"{convert_to_red('Error')}: The folder {env_dir} (for RTSAI environments) does not exist! ")
        return

    ## Display all chats under the current environment
    print(f"\nRTSAI chats for the {CURRENT_ENV} environment: ")
    chats = [name for name in os.listdir(f"{env_dir}/chats") if os.path.isdir(os.path.join(env_dir, name))]
    if not chats: print("(None)\n"); return
    for chat in chats: 
        print(f"-   {chat}")
    print()

