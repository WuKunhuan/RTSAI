
# 1. Check system requirements

## 1.1 Check CMake version and define the project

cmake_minimum_required(VERSION 3.20)
project(RTSAI)

# Remove previous cache
file(GLOB_RECURSE REMOVED_FILES ${CMAKE_BINARY_DIR}/CMakeFiles)
file(GLOB_RECURSE REMOVED_FILES ${CMAKE_BINARY_DIR}/cmake_install.cmake)
file(GLOB_RECURSE REMOVED_FILES ${CMAKE_BINARY_DIR}/CMakeCache.txt)
file (REMOVE ${REMOVED_FILES})
file(REMOVE_RECURSE ${CMAKE_BINARY_DIR}/Makefile)
message(STATUS "Cleaning cmake build files")

## 1.2 Check Python version >= 3.12

find_package(Python3 REQUIRED)

# Find Python
if (Python3_FOUND)

    message(STATUS "Found Python: ${Python3_EXECUTABLE}")

    # Find Python Version
    message(STATUS "Current Python version: ${Python3_VERSION}")

    if (Python3_VERSION_MAJOR GREATER_EQUAL 3 AND Python3_VERSION_MINOR GREATER_EQUAL 12)
        message(STATUS "Requirement: Python version >= 3.12 : SATISFIED.")
        set(LINK_EXECUTABLE ${PYTHON3_EXECUTABLE})
    else()
        message(FATAL_ERROR "Requirement: Python version >= 3.12 : NOT SATISFIED. Please install Python 3.12 or a higher version.")
    endif()

else()

    message(FATAL_ERROR "Requirement: Python : NOT SATISFIED. Please install Python.")

endif()

# Source Files
set(SOURCES
    src/RTSAI_Core.py
)

# Executable Target
add_executable(RTSAI ${SOURCES})

# Set the appropriate Python interpreter as the target
set_target_properties(RTSAI PROPERTIES LINKER_LANGUAGE Python3)

