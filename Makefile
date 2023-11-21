# Makefile for building and installing RTSAI executable

# Compiler settings
PYTHON := python3

# Directories
SRC_CODE_DIR := src/codes
SRC_MAN_DIR := src/manuals
PY_FILE := $(SRC_CODE_DIR)/RTSAI_Main.py  # define the source python file
BIN_DIR := bin
DATA_DIR := src/data

RTSAI_EXEC_DIR := /usr/local/bin/RTSAI
RTSAI_DIR := /Users/$(USER)/opt/RTSAI
RTSAI_DATA_DIR := $(RTSAI_DIR)/data
RTSAI_ENV_DIR := $(RTSAI_DIR)/env
RTSAI_MAN_DIR := $(RTSAI_DIR)/man

# Build and install target
# one directory mode
RTSAI: $(PY_FILE)
	@pip install pyinstaller
	@clear
	@rm -rf dist
	@echo "Creating standalone executable ..."
	@pyinstaller --onedir $(PY_FILE) --name RTSAI > /dev/null 2>&1
	@echo "Standalone executable created in dist/RTSAI_Main directory."
	@echo "Installing RTSAI ... (password may be required to modify /usr/local)"
	@sudo rm -rf $(RTSAI_EXEC_DIR)
	@sudo mv dist/RTSAI $(RTSAI_EXEC_DIR)
	@export PATH="/usr/local/bin/RTSAI:$PATH"
	@echo "RTSAI binary added to $(RTSAI_EXEC_DIR)!"
	@if [ ! -d $(RTSAI_DIR) ]; then \
		sudo mkdir -p $(RTSAI_DIR); \
		sudo cp -r $(DATA_DIR) $(RTSAI_DATA_DIR); \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default; \
		echo "RTSAI environment created at $(RTSAI_DIR)!"; \
	else \
		sudo chmod +x $(RTSAI_DIR); \
		echo "RTSAI environment already created at $(RTSAI_DIR)!"; \
	fi
	@sudo chmod +x $(RTSAI_EXEC_DIR)
	@sudo chmod +rwx $(RTSAI_DIR); 
	@sudo chmod +rwx $(RTSAI_DATA_DIR); 
	@sudo chmod +rwx $(RTSAI_ENV_DIR); 
	@rm -rf dist
	@rm -rf build
	@rm -f RTSAI_Main.spec
	@sudo cp $(SRC_MAN_DIR)/RTSAI.1 /usr/local/share/man/man1/RTSAI.1
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@sudo mkdir -p $(RTSAI_MAN_DIR)
	@sudo cp -R $(SRC_MAN_DIR)/* $(RTSAI_MAN_DIR)
	@echo "RTSAI manuals added!"

clean:
	@rm -rf dist
	@sudo rm -rf $(RTSAI_EXEC_DIR)
	@sudo rm -rf $(RTSAI_DIR)
	@echo "RTSAI binary deleted successfully from $(RTSAI_EXEC_DIR)!"
	@echo "RTSAI environment deleted successfully from $(RTSAI_DIR)!"
	@sudo rm -f /usr/local/share/man/man1/RTSAI.1
	@sudo rm -rf $(RTSAI_MAN_DIR)
	@echo "RTSAI manuals removed!"

.PHONY: RTSAI clean
