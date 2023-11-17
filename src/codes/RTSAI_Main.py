
import sys

from RTSAI_env import create_env, list_envs

# Define the list of commands and their descriptions
COMMANDS = {
    'create': {
        'description': 'Create a new environment',
        'usage': 'Usage: RTSAI create <env_name>'
    },
    'list': {
        'description': 'List all environments',
        'usage': 'Usage: RTSAI env list'
    }
    # Add more commands and their descriptions here
}
    
def main():
    # Check if the user entered 'RTSAI' without any additional commands
    if len(sys.argv) == 1:
        print("Welcome to the world of RTSAI!")
        return 0
    elif sys.argv[1] == 'create':
        if len(sys.argv) != 3:
            print(COMMANDS['create']['usage'])
            return
        create_env(sys.argv[2])
    elif sys.argv[1] == 'env':
        if len(sys.argv) != 3 or sys.argv[2] != 'list':
            print(COMMANDS['list']['usage'])
            return
        list_envs()
    else:
        print("Error: Invalid command! Enter 'man RTSAI' for usage.")


if __name__ == '__main__':
    main()