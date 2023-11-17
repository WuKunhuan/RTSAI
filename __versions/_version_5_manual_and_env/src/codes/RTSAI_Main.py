
import sys

from RTSAI_Create import create_env

# Define the list of commands and their descriptions
COMMANDS = {
    'create': {
        'description': 'Create a new environment',
        'usage': 'Usage: RTSAI create <env_name>'
    },
    # Add more commands and their descriptions here
}

def handle_command(args):
    if args[0] == 'create':
        if len(args) != 2:
            print(COMMANDS['create']['usage'])
            return
        create_env(args[1])
    else:
        print("Error: Invalid command! Enter 'man RTSAI' for the usage.")

def show_manual():
    print("RTSAI Commands Manual:")
    for command, info in COMMANDS.items():
        print(f"\n{command.capitalize()}:")
        print(f"  Description: {info['description']}")
        print(f"  Usage: {info['usage']}")

def main():
    # Check if the user entered 'RTSAI' without any additional commands
    if len(sys.argv) == 1:
        print("Welcome to the world of RTSAI!")
        return 0

    # Handle the user commands
    if sys.argv[1] == 'man' and len(sys.argv) == 3 and sys.argv[2] == 'RTSAI':
        show_manual()
    else:
        handle_command(sys.argv[1:])

if __name__ == '__main__':
    import sys
    main()
