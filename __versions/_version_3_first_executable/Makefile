# Makefile for building RTSAI executable

# Compiler settings
PYTHON := python3

# Directories
SRC_DIR := src
BIN_DIR := bin

# Files
PY_FILE := $(SRC_DIR)/RTSAI_Core.py
EXE_FILE := $(BIN_DIR)/RTSAI

# Build target
all: $(BIN_DIR) $(EXE_FILE)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(EXE_FILE): $(PY_FILE)
	@echo "Creating executable..."
	@echo "#!/usr/bin/env python3" > $(EXE_FILE)
	@cat $(PY_FILE) >> $(EXE_FILE)
	@chmod +x $(EXE_FILE)
	@echo "Executable created: $(EXE_FILE)"

clean:
	rm -rf $(BIN_DIR)