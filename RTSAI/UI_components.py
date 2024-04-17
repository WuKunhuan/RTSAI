
# Window, left and right panels
window = None
left_panel = None
left_panel_sidebar = None
left_panel_main = None
left_panel_main_scrollbar = None
left_panel_main_scrollbar_position = None
left_panel_change_arrow = None
left_panel_sidebar_chat = None
left_panel_sidebar_crawl = None
left_panel_sidebar_logo = None
right_panel = None
right_panel_tabbar = None
right_panel_tabbar_scrollbar = None
right_panel_tabbar_scrollbar_position = None
right_panel_tabbar_scrollbar_created = False
right_panel_main = None
right_panel_change_arrow = None

avatar_image = None
avatar_image_item = None
avatar_image_change = None
avatar_image_in_setting = None
avatar_item_in_setting = None
avatar_canvas_in_setting = None
avatar_image_change_in_setting = None

# Toggle list components
toggle_list = None
toggle_list_created = False
toggle_list_scrollbar_created = False
toggle_list_states = dict()
toggle_item_on_focus = None # The current selected toggle item
toggle_list_operations = [] # A list of operations done; for reverting purposes (max. 100 operations)
toggle_list_operation_current = 0  # The operation corresponding to the current state

# Tabbar components
tabbar_shown = False
tab_total_width = 0
editor_states = [] # Sequential order of opened editors: [type, value, display] ## status can be obtained within the Main
editor_item_operations = dict() # key: editor_item; value: list of operations done on this item (max. 100 operations); operation_current]

# Editor window components
current_editor_id = -1 # The current selected editor; id of the editor_states
current_editor = None # The previous loaded window
editor_windows = dict() # Key: Type + Value; Value: [Right_Panel_Main_Window object, all elements to render]
editor_updated = False
    # Key Value part of different tabs: 
    # -     Chat: path to environment
    # -     Knowledge Graph: path to knowledge graph
    # -     Web Crawl: crawl/new_ID()
