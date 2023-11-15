# Makefile for building and installing RTSAI executable

# Compiler settings
PYTHON := python3

# Directories
SRC_DIR := src/codes
BIN_DIR := bin
DATA_DIR := src/data
RTSAI_DIR := /Users/$(USER)/opt/RTSAI
RTSAI_DATA_DIR := $(RTSAI_DIR)/data
RTSAI_ENV_DIR := $(RTSAI_DIR)/env

# Files
PY_FILE := $(SRC_DIR)/RTSAI_Main.py
EXE_FILE := $(BIN_DIR)/RTSAI

# Build and install target
install: $(PY_FILE)

	@echo "Creating executable..."

	echo "#!/usr/bin/env python3" > $(EXE_FILE); \
	cat $(PY_FILE) >> $(EXE_FILE); \
	chmod +x $(EXE_FILE); \

	@echo "Executable created: $(EXE_FILE)"; \

	@echo "Installing RTSAI... (password may be required to modify /usr/local)"

	sudo rm -rf /usr/local/bin/$(EXE_FILE); \
	sudo cp $(EXE_FILE) /usr/local/bin/; \
	echo "RTSAI binary added to /usr/local/bin"; 

	@if [ ! -d $(RTSAI_DIR) ]; then \
		sudo mkdir -p $(RTSAI_DIR); \
		sudo cp -r $(DATA_DIR) $(RTSAI_DATA_DIR); \
		sudo mkdir -p $(RTSAI_ENV_DIR)/default; \
		echo "RTSAI installed successfully at $(RTSAI_DIR)!"; \
	else \
		echo "RTSAI already installed at $(RTSAI_DIR)!"; \
	fi

clean:
	rm -rf $(BIN_DIR)

.PHONY: install clean

