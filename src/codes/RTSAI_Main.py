import sys
import os

from RTSAI_env import create_env, list_envs

user = os.getenv('USER')

def get_usage(command):
    usage_file = f"/Users/{user}/opt/RTSAI/man/{command}.txt"
    try: 
        with open(usage_file, 'r') as f:
            return f.read()
    except Exception: raise Exception
    return "Usage information not available."

def handle_command(args):
    if args[0] == 'create':
        if len(args) == 2:
            create_env(args[1])
        elif (len(args) != 2 and args[0] == 'create'): # must be true
            print(get_usage('create'))
            return
        else: 
            pass
        
    elif args[0] == 'env':
        if len(args) == 2 and args[1] == 'list':
            list_envs()
        elif (len(args) != 2 and args[1] == 'list'): 
            print(get_usage('env/list'))
            return
        else: 
            pass
    else:
        print("Error: Invalid command! Enter 'man RTSAI' for usage.")

def main():
    # Check if the user entered 'RTSAI' without any additional commands
    if len(sys.argv) == 1:
        print("Welcome to the world of RTSAI!")
        return 0
    else:
        handle_command(sys.argv[1:])

if __name__ == '__main__':
    main()
