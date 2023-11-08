# Makefile for building and installing RTSAI executable

# Compiler settings
PYTHON := python3

# Directories
SRC_DIR := src
BIN_DIR := bin

# Files
PY_FILE := $(SRC_DIR)/RTSAI_Core.py
EXE_FILE := $(BIN_DIR)/RTSAI

# Build and install target
install: $(PY_FILE)
	@echo "Creating executable..."
	@echo "#!/usr/bin/env python3" > $(EXE_FILE)
	@cat $(PY_FILE) >> $(EXE_FILE)
	@chmod +x $(EXE_FILE)
	@echo "Executable created: $(EXE_FILE)"
	@echo "Installing RTSAI..."
	@cp $(EXE_FILE) /usr/local/bin/RTSAI
	@echo "RTSAI installed successfully!"

clean:
	rm -rf $(BIN_DIR)