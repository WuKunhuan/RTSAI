
import os, sys, pyautogui

'''
Package information
'''
PACKAGE_NAME = "package_RTSAI"
PACKAGE_VERSION = '0.1.0'

PACKAGE_PATH = os.path.dirname(__file__)
EXECUTABLE_PATH = sys.executable[::-1][sys.executable[::-1].index('/')+1:][::-1]

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

def operating_system(): 
    # print (f"sys.platform: {sys.platform}")
    if (sys.platform.startswith("darwin")): return ("MacOS")
    elif (): return ("Windows")
    else: return ("Windows")

PRE_INSTALLED_KG_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'knowledge_graphs')
PRE_INSTALLED_KG = ["HKU_Intuitive"]

COMMAND_NAME = "RTSAI"
WINDOW_NAME = "RTSAI UI"

DESKTOP_SIZE = tuple(pyautogui.size())

'''
RTSAI UI Components
No Need to Change
'''
window = None
left_panel = None
left_panel_sidebar = None
left_panel_main = None
right_panel = None
right_panel_tabbar = None
right_panel_main = None
left_panel_change_arrow = None
left_panel_sidebar_chat = None
left_panel_sidebar_crawl = None
right_panel_change_arrow = None

toggle_list = None
toggle_list_created = False
toggle_list_states = dict()
toggle_item_on_focus = None # The current selected toggle item
toggle_list_operations = [] # A list of operations done; for reverting purposes (max. 100 operations)
toggle_list_operation_current = 0  # The operation corresponding to the current state

editor_states = [] # Sequential order of opened editors: (editor tab: (type, value, display), status)
editor_item_on_focus = 0 # The current selected editor; id of the editor_states
editor_item_operations = dict() # key: editor_item; value: l[ist of operations done on this item (max. 100 operations); operation_current]

label_width_ratio = 8

'''
RTSAI UI Config
'''
window_width = 800; window_height = 600; 
window_width_min = 600; window_height_min = 450; 
window_width_max = DESKTOP_SIZE[0]; window_height_max = DESKTOP_SIZE[1]; 

left_panel_color = (24, 24, 24)
left_panel_relwidth = 0.3; 
left_panel_width = 240; 
left_panel_width_min = 200; 
left_panel_relwidth_max = 0.4; 
left_panel_sidebar_width = 50

right_panel_color = (31, 31, 31)
right_panel_tabbar_height = 20

size_increase_arrow_width = 25; 
size_increase_arrow_height = 12.5; 
boundary_width = 1; 

boundary_grey_color = (43, 43, 43)
clicked_grey_color = (51, 51, 51)
default_grey_color = (64, 64, 64)

VSCode_highlight_color = (47, 108, 187)
VSCode_new_color = (82, 158, 78)
VSCode_font_grey_color = (204, 204, 204)

standard_font_family = "Consolas"
standard_font_size = 12
toggle_item_padx = 5
toggle_item_pady = 2
toggle_item_height = standard_font_size * 1.5 + 2 * toggle_item_pady
toggle_modify_width = toggle_item_height - 2 * toggle_item_pady
toggle_modify_height = toggle_item_height - 2 * toggle_item_pady

