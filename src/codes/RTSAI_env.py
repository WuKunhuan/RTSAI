
import os, re

from constants import ENV_PATH
from functions import convert_to_red
from RTSAI_Main import CURRENT_ENV

## This function creates an RTSAI environment
def create_env(env_name):

    ## Validate the environment name
    if not re.match(r'^[a-zA-Z0-9_]+$', env_name):
        print(f"{convert_to_red('Error')}: Invalid RTSAI environment name. Please use only letters, numbers, and underscores.")
        return

    ## Set the environment directory path
    env_dir = f'{ENV_PATH}/envs/{env_name}'

    ## Check if the environment already exists
    if os.path.exists(env_dir):
        overwrite = input(f"The RTSAI environment '{env_name}' already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("RTSAI environment creation ended by the user [overwrite: FALSE]. ")
            return

    # Create the environment directory with elevated privileges
    print (f"\nCreating RTSAI environment {env_name} at {env_dir} (password may required) ... ")
    os.system(f"sudo mkdir -p {env_dir}")
    os.system(f"sudo chmod -R 755 {env_dir}")
    os.system(f"sudo mkdir -p {env_dir}/chats")
    os.system(f"sudo mkdir -p {env_dir}/graphs")
    print(f"SUCCESSFUL! ")

## This function lists all RTSAI environments
def list_envs():

    ## Verify the environment exists
    env_dir = f"{ENV_PATH}/envs"
    if not os.path.exists(env_dir):
        print(f"{convert_to_red('Error')}: The folder {env_dir} (for RTSAI environments) does not exist! ")
        return

    ## Display all environments
    print(f"\nRTSAI environments: ")
    envs = [name for name in os.listdir(env_dir) if os.path.isdir(os.path.join(env_dir, name))]
    if not envs: print("(None)"); return
    for env in envs: 
        if (env == CURRENT_ENV): print(f"-   {env} (*)")
        else: print(f"-   {env}")
    print()

