# Makefile for building and installing RTSAI executable

# 1. Settings

# 1.1 Compiler settings
PYTHON := python3

# 1.2 Directories location settings
SRC_CODE_DIR := src/codes
SRC_PY_FILE := $(SRC_CODE_DIR)/RTSAI_Main.py
SRC_MAN_DIR := src/manuals
GRAPH_DIR := src/graphs

RTSAI_EXEC_DIR := /usr/local/bin/RTSAI
RTSAI_DIR := /Users/$(USER)/opt/RTSAI
RTSAI_ENV_DIR := $(RTSAI_DIR)/envs
RTSAI_GRAPH_DIR := $(RTSAI_DIR)/graphs
RTSAI_MAN_DIR := $(RTSAI_DIR)/manuals

# 2. Build the target

##	Build and install target, one directory mode
RTSAI: $(SRC_PY_FILE)

	@clear

##	2.1 Install libraries
	@echo "Installing necessary packages ... "

##	install pyinstaller
	@echo "installing pyinstaller: \\c"
	@(pip install --quiet pyinstaller 2> error.log; echo "SUCCESSFUL! "; rm error.log) || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
##	install kgtk. The typing library is removed since it is not compatible with pyinstaller
	@echo "installing kgtk: \\c"
	@(pip install --quiet kgtk 2> error.log; pip show typing > /dev/null 2>&1 && pip uninstall -y typing > /dev/null 2>&1 || true; echo "SUCCESSFUL! "; rm error.log) || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
##	install pandas
	@echo "installing pandas: \\c"
	@(pip install --quiet pandas 2> error.log; echo "SUCCESSFUL! "; rm error.log) || (echo "FAILED! "; cat error.log; rm error.log; exit 1)

##	2.2 Compile the executable
	@echo "\nCompiling the executable RTSAI (it may take a while) ... \\c"
	@rm -rf dist build
	@(pyinstaller --onedir $(SRC_PY_FILE) --name RTSAI > /dev/null 2>&1 && echo "SUCCESSFUL! ") || (echo "FAILED! "; exit 1)

##	2.3 Install the executable
	@echo "\nInstalling RTSAI at $(RTSAI_EXEC_DIR) (password may required) ... \\c"
	@sudo rm -rf $(RTSAI_EXEC_DIR)
	@(sudo mv dist/RTSAI $(RTSAI_EXEC_DIR) 2> error.log; echo "SUCCESSFUL! ") || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
##  For Mac system: export the path to ~/.bash_profile
##	export PATH="/usr/local/bin/RTSAI:$${PATH}"
	@grep -qxF 'export PATH="/usr/local/bin/RTSAI:$${PATH}"' ~/.bash_profile || echo '# Setting PATH for RTSAI\nexport PATH="/usr/local/bin/RTSAI:$${PATH}"' >> ~/.bash_profile

##	2.4 Create the environment
## Create default environment in the fresh installation
## Create the chats and graphs folders under the environment
	@echo "\nCreating the RTSAI environment at $(RTSAI_DIR) ... \\c"
	@if [ ! -d $(RTSAI_DIR) ]; then \
		sudo mkdir -p $(RTSAI_DIR); \
		sudo cp -r $(GRAPH_DIR) $(RTSAI_GRAPH_DIR) 2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1); \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default; \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default/chats; \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default/graphs; \
	else \
		sudo chmod +x $(RTSAI_DIR) 2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1); \
	fi
	@sudo chmod +x $(RTSAI_EXEC_DIR) 2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
	@sudo chmod +rwx $(RTSAI_DIR);  2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
	@sudo chmod +rwx $(RTSAI_GRAPH_DIR);  2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
	@sudo chmod +rwx $(RTSAI_ENV_DIR);  2> error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)

##	2.5 Clean up and copy the manual
	@rm -rf dist build
	@rm -f RTSAI.spec
	@sudo cp $(SRC_MAN_DIR)/RTSAI.1 /usr/local/share/man/man1/RTSAI.1 2> error.log && rm error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@sudo mkdir -p $(RTSAI_MAN_DIR)
	@sudo cp -R $(SRC_MAN_DIR)/* $(RTSAI_MAN_DIR) 2> error.log && rm error.log || (echo "FAILED! "; cat error.log; rm error.log; exit 1)
	@echo "SUCCESSFUL! "
	@echo "RTSAI installation SUCCESSFUL! \nEnter \"man RTSAI\" for the usage. \n"

RTSAI_uninstall:
	@rm -rf dist
	@sudo rm -rf $(RTSAI_EXEC_DIR)
	@sudo rm -rf $(RTSAI_DIR)

##  For Mac system: remove the path from ~/.bash_profile
	@if [ `uname` = "Darwin" ]; then \
		sed -i '' '/RTSAI/d' ~/.bash_profile; \
	else \
		sed -i '/RTSAI/d' ~/.bash_profile; \
	fi
	@echo "RTSAI binary deleted from $(RTSAI_EXEC_DIR): SUCCESSFUL! " 
	@sudo rm -f /usr/local/share/man/man1/RTSAI.1
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@echo "RTSAI environment deleted from $(RTSAI_DIR): SUCCESSFUL! "
	@echo "Thanks for using RTSAI! "

# .PHONY: RTSAI clean
