
# clear the screen
if(UNIX) 
    execute_process(COMMAND clear)
elseif(WIN32)
    execute_process(COMMAND cmd /c cls)
endif()

# 1. Check system requirements

## 1.1 Check CMake version and define the project

cmake_minimum_required(VERSION 3.20)
project(RTSAI)

## 1.2 Check Python version >= 3.12

set(CMAKE_FIND_FRAMEWORK NEVER)

find_package(Python3 3.12 REQUIRED COMPONENTS Interpreter Development)

# Find Python
if (Python3_FOUND)

    message(STATUS "Found Python: ${Python3_EXECUTABLE}")

    # Find Python Version
    message(STATUS "Current Python version: ${Python3_VERSION}")

    if (Python3_VERSION_MAJOR GREATER_EQUAL 3 AND Python3_VERSION_MINOR GREATER_EQUAL 12)
        message(STATUS "Requirement: Python version >= 3.12 : SATISFIED.")
        set(CMAKE_Python3_LINK_EXECUTABLE "${CMAKE_Python3_LINK_EXECUTABLE}")
    else()
        message(FATAL_ERROR "Requirement: Python version >= 3.12 : NOT SATISFIED. Please install Python 3.12 or a higher version.")
    endif()

else()

    message(FATAL_ERROR "Requirement: Python : NOT SATISFIED. Please install Python.")

endif()

set (SRC_FOLDER "src")

## 1.3 Set output directory location

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)



## X. Build target RTSAI

file(GLOB_RECURSE RTSAI_SOURCES
    ${SRC_FOLDER}/RTSAI_Core.py
)
add_executable(RTSAI ${RTSAI_SOURCES})
set_target_properties(RTSAI PROPERTIES LINKER_LANGUAGE Python3)



