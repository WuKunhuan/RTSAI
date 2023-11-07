
# 1. Check system requirements

## 1.1 Check CMake version

cmake_minimum_required(VERSION 3.12)
project(YourProjectName)



## 1.2 Check Python version >= 3.12

find_package(Python 3.12 REQUIRED)
if (Python_FOUND)
    message(STATUS "Found Python: ${Python_EXECUTABLE}")
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import sys; exit(0) if sys.version_info >= (3, 12) else exit(1)"
        RESULT_VARIABLE PYTHON_VERSION_CHECK
    )
    if (PYTHON_VERSION_CHECK EQUAL 0)
        message(STATUS "Requirement: Python version >= 3.12 : SATISFIED. ")
    else()
        message(FATAL_ERROR "Requirement: Python version >= 3.12 : NOT SATISFIED. ")
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
set_target_properties(RTSAI PROPERTIES LINKER_LANGUAGE Python)