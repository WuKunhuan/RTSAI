# RTSAI

RTSAI Introduction

## 1. Pre-requisites

### 1.1 Python (version 3.12)

To install Python 3.12, you can visit the [Python Downloads](https://www.python.org/downloads/) page and follow the instructions for your operating system.

If you have an earlier version of Python installed and want to use Python 3.12, you can use `pyenv` (for Unix-like systems) or `pyenv-win` (for Windows) to manage multiple Python versions on your system.

------

#### Using pyenv (Unix-like systems)

1. Install `pyenv` by following the instructions provided in the [pyenv GitHub repository](https://github.com/pyenv/pyenv#installation).

2. Once `pyenv` is installed, you can install Python 3.12 by running the following command in your terminal: 

```pyenv install 3.12.0```

3. Set Python 3.12 as the global version by running the following in the terminal:

```pyenv global 3.12.0```

------

#### Using pyenv-win (Windows)

1. Install pyenv-win by following the instructions provided in the pyenv-win GitHub repository.

2. After installing pyenv-win, open a new command prompt and install Python 3.12 by running the following command in your Powershell:

```pyenv install 3.12.0```

3. Set Python 3.12 as the global version by running the following in the Powershell:

```pyenv global 3.12.0```

------

After following the instructions to install Python 3.12 using pyenv or pyenv-win, you can open a new command prompt or terminal and run the following command: 

```python --version```

This should  display Python 3.12.0 as the output. 

To address the prerequisite of installing CMake for users, you can add the following information to the README.md file:

------

### 1.2 CMake

CMake is a cross-platform build system that is required to compile and build the project. If you don't have CMake installed, follow the instructions below to install it:

- **Windows**: Download the latest CMake installer from the [CMake website](https://cmake.org/download/) and run the installer. Make sure to add CMake to your system's PATH during the installation process.

- **macOS**: Install CMake using Homebrew by running the following command in the terminal:
  ```shell
  brew install cmake
  ```

- **Linux**: Use your distribution's package manager to install CMake. For example, on Ubuntu or Debian, you can run the following command:
  ````shell
  sudo apt-get install cmake
  ```

After installing CMake, you should be able to use the `cmake` command in your command prompt or terminal.

```
