
import os, sys, pyautogui, random

'''
Package information
'''
PACKAGE_NAME = "RTSAI"
PACKAGE_VERSION = '0.1.8'

def operating_system(): 
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

'''
RTSAI UI Components
No Need to Change
'''
window = None
left_panel = None
left_panel_sidebar = None
left_panel_main = None
left_panel_main_scrollbar = None
left_panel_main_scrollbar_position = None
right_panel = None
right_panel_tabbar = None
right_panel_tabbar_scrollbar = None
right_panel_tabbar_scrollbar_position = None
right_panel_tabbar_scrollbar_created = False
right_panel_main = None
left_panel_change_arrow = None
left_panel_sidebar_chat = None
left_panel_sidebar_crawl = None
right_panel_change_arrow = None

toggle_list = None
toggle_list_created = False
toggle_list_scrollbar_created = False
toggle_list_states = dict()
toggle_item_on_focus = None # The current selected toggle item
toggle_list_operations = [] # A list of operations done; for reverting purposes (max. 100 operations)
toggle_list_operation_current = 0  # The operation corresponding to the current state

# Tabbar components
right_panel_shown = False
tab_total_width = 0

editor_states = [] # Sequential order of opened editors: [type, value, display] ## status can be obtained within the Main
editor_item_operations = dict() # key: editor_item; value: list of operations done on this item (max. 100 operations); operation_current]

# related to label width setting
label_width_ratio = 8
label_width_one_unit_characters = 5

# Main window components
current_editor_id = -1 # The current selected editor; id of the editor_states
current_editor = None # The previous loaded window
main_windows = dict() # Key: Type + Value; Value: Right_Panel_Main_Window object
    # Key Value part of different tabs: 
    # -     Chat: path to environment
    # -     Knowledge Graph: path to knowledge graph
    # -     Web Crawl: crawl/new_ID()
dialog_box_icon_size = 20

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
left_panel_main_scrollbar_width = 10

right_panel_color = (31, 31, 31)
right_panel_tabbar_height = 25
right_panel_tabbar_scrollbar_width = 10

size_increase_arrow_width = 25; 
size_increase_arrow_height = 12.5; 
boundary_width = 1; 

grey_color_43 = (43, 43, 43)
grey_color_51 = (51, 51, 51)
grey_color_64 = (64, 64, 64)

VSCode_highlight_color = (47, 108, 187)
VSCode_new_color = (82, 158, 78)
VSCode_font_grey_color = (204, 204, 204)

standard_font_family = "Consolas"
standard_font_size = 12
h1_font_size = 24
h2_font_size = 20
h3_font_size = 16

toggle_item_padx = 5
toggle_item_pady = 2
toggle_item_height = standard_font_size * 1.5 + 2 * toggle_item_pady
toggle_modify_width = toggle_item_height - 2 * toggle_item_pady
toggle_modify_height = toggle_item_height - 2 * toggle_item_pady

random_color_list = [
    (235, 75, 66), #RED
    (239, 138, 74), #ORANGE
    (250, 227, 131), #YELLOW
    (172, 223, 125), #GREEN
    (109, 213, 184), #TURQUISE
    (107, 173, 248), #BLUE
    (208, 117, 248), #PURPLE
    (238, 124, 185), #PINK
    (187, 154, 110), #BROWN
]
random.shuffle(random_color_list)
chat_icon_color = random_color_list[0]
crawl_icon_color = random_color_list[1]

