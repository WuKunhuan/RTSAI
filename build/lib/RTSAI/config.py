
import sys, appdirs, pathlib, pyautogui

PACKAGE_NAME = "package_RTSAI"
PACKAGE_VERSION = '0.1.0'

PACKAGE_PATH = pathlib.Path(__file__).parent.resolve()
EXECUTABLE_PATH = sys.executable[::-1][sys.executable[::-1].index('/')+1:][::-1]
DATA_PATH = appdirs.user_data_dir(PACKAGE_NAME)

COMMAND_NAME = "RTSAI"
WINDOW_NAME = "RTSAI UI"

DESKTOP_SIZE = tuple(pyautogui.size())
