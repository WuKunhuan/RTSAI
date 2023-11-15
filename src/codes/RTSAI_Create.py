import os
import re

def create_env(env_name):
    # Validate the environment name
    if not re.match(r'^[a-zA-Z0-9_]+$', env_name):
        print("Invalid RTSAI environment name. Please use only letters, numbers, and underscores.")
        return

    # Set the environment directory path
    env_dir = os.path.expanduser(f'~/opt/RTSAI/env/{env_name}')

    # Check if the environment already exists
    if os.path.exists(env_dir):
        overwrite = input(f"The RTSAI environment '{env_name}' already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Environment creation ended by the user [overwrite: FALSE].")
            return

    # Create the environment directory
    os.makedirs(env_dir, exist_ok=True)
    print(f"The RTSAI environment '{env_name}' created successfully at {env_dir}")
