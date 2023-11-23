
import getpass

# 1. System Settings

## The system user (MAC system)
SYSTEM_USER = getpass.getuser()

## The executable path
EXEC_PATH = "/usr/local/bin/RTSAI"

## The environment path
ENV_PATH = f"/Users/{SYSTEM_USER}/opt/RTSAI"



# 2. RTSAI: Environment Settings

## The default and current user environment
DEFAULT_ENV = "default"
CURRENT_ENV = DEFAULT_ENV

# Others

RED = "\033[91m"
RESET = "\033[0m"
