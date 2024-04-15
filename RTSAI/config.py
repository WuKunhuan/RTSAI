
import os, sys, pyautogui, random

'''
Package information
'''
PACKAGE_NAME = "RTSAI"
PACKAGE_VERSION = '0.1.8'

def operating_system(): 
    print (f"Operating system: {sys.platform}")
    if (sys.platform.startswith("darwin")): return ("MacOS")
    elif (): return ("Windows")
    else: return ("Windows")

PACKAGE_PATH = os.path.dirname(__file__)
if (operating_system() == "MacOS"):
    EXECUTABLE_PATH = sys.executable[::-1][sys.executable[::-1].index('/')+1:][::-1]
else: EXECUTABLE_PATH = sys.executable[::-1]

ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

environment_names = os.listdir(os.path.join(DATA_PATH, "environments"))
if (not environment_names): 
    os.makedirs(os.path.join(DATA_PATH, "environments", "default"))
    environment_names = os.listdir(os.path.join(DATA_PATH, "environments"))
    CURRENT_ENV = "default"
else: 
    environment_names.sort (key = lambda name: name.lower())
    CURRENT_ENV = environment_names[0]

PRE_INSTALLED_KG_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'knowledge_graphs')
PRE_INSTALLED_KG = ["HKU_Intuitive"]

COMMAND_NAME = "RTSAI"
WINDOW_NAME = "RTSAI UI"
DESKTOP_SIZE = tuple(pyautogui.size())
