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
RTSAI_ENV_DIR := $(RTSAI_DIR)/env
RTSAI_GRAPH_DIR := $(RTSAI_DIR)/graphs
RTSAI_MAN_DIR := $(RTSAI_DIR)/man

# 2. Build the target

##	Build and install target, one directory mode
RTSAI: $(SRC_PY_FILE)
	@pip install pyinstaller
	@clear
	@rm -rf dist
	@echo "Compiling the executable RTSAI ... (it make take a while)"
	@pyinstaller --onedir $(SRC_PY_FILE) --name RTSAI > /dev/null 2>&1
	@echo "Standalone executable created in dist/RTSAI_Main directory."
	@echo "Installing RTSAI ... (password may be required to modify /usr/local)"
	@sudo rm -rf $(RTSAI_EXEC_DIR)
	@sudo mv dist/RTSAI $(RTSAI_EXEC_DIR)

##  For Mac system: export the path to ~/.bash_profile
##	export PATH="/usr/local/bin/RTSAI:$${PATH}"
	@grep -qxF 'export PATH="/usr/local/bin/RTSAI:$${PATH}"' ~/.bash_profile || echo '#Setting PATH for RTSAI\nexport PATH="/usr/local/bin/RTSAI:$${PATH}"' >> ~/.bash_profile
	@echo "RTSAI binary added to $(RTSAI_EXEC_DIR)!"

## Create default environment in the fresh installation
## Create the chats and graphs folders under the environment
	@if [ ! -d $(RTSAI_DIR) ]; then \
		sudo mkdir -p $(RTSAI_DIR); \
		sudo cp -r $(GRAPH_DIR) $(RTSAI_GRAPH_DIR); \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default; \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default/chats; \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default/graphs; \
		echo "RTSAI environment created at $(RTSAI_DIR)!"; \
	else \
		sudo chmod +x $(RTSAI_DIR); \
		echo "RTSAI environment already created at $(RTSAI_DIR)!"; \
	fi
	@sudo chmod +x $(RTSAI_EXEC_DIR)
	@sudo chmod +rwx $(RTSAI_DIR); 
	@sudo chmod +rwx $(RTSAI_GRAPH_DIR); 
	@sudo chmod +rwx $(RTSAI_ENV_DIR); 
	@rm -rf dist
	@rm -rf build
	@rm -f RTSAI.spec
	@sudo cp $(SRC_MAN_DIR)/RTSAI.1 /usr/local/share/man/man1/RTSAI.1
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@sudo mkdir -p $(RTSAI_MAN_DIR)
	@sudo cp -R $(SRC_MAN_DIR)/* $(RTSAI_MAN_DIR)
	@echo "RTSAI manuals added!"

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

	@echo "RTSAI binary deleted successfully from $(RTSAI_EXEC_DIR)!"
	@echo "RTSAI environment deleted successfully from $(RTSAI_DIR)!"
	@sudo rm -f /usr/local/share/man/man1/RTSAI.1
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@echo "RTSAI manuals removed!"

# .PHONY: RTSAI clean
