# Makefile for building and installing RTSAI executable

# Compiler settings
PYTHON := python3

# Directories
SRC_DIR := src
BIN_DIR := bin
DATA_DIR := src/data
RTSAI_DIR := /usr/local/RTSAI
RTSAI_DATA_DIR := $(RTSAI_DIR)/data
RTSAI_ENV_DIR := $(RTSAI_DIR)/environments

# Files
PY_FILE := $(SRC_DIR)/codes/RTSAI_Core.py
EXE_FILE := $(BIN_DIR)/RTSAI

# Build and install target
install: $(PY_FILE)
	@echo "Creating executable..."
	@echo "#!/usr/bin/env python3" > $(EXE_FILE)
	@cat $(PY_FILE) >> $(EXE_FILE)
	@chmod +x $(EXE_FILE)
	@echo "Executable created: $(EXE_FILE)"
	@echo "Installing RTSAI ... (password may be required to modify /usr/local)"
	@sudo mkdir -p $(RTSAI_DIR)
	@mkdir -p $(RTSAI_DATA_DIR)
	@cp -r $(DATA_DIR) $(RTSAI_DATA_DIR)
	@mkdir -p $(RTSAI_ENV_DIR)/default
	@echo "RTSAI installed successfully!"

clean:
	rm -rf $(BIN_DIR) $(RTSAI_DIR)

.PHONY: install clean