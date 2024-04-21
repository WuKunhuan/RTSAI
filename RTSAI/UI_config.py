
import random
from RTSAI.config import DESKTOP_SIZE

window_width = 800; window_height = 600; 
window_width_min = 600; window_height_min = 450; 
window_width_max = DESKTOP_SIZE[0]; window_height_max = DESKTOP_SIZE[1]; 

user_avatar = "male_avatar_1.png"

left_panel_color = (24, 24, 24)
left_panel_relwidth = 0.3; 
left_panel_width = 240; 
left_panel_width_min = 200; 
left_panel_relwidth_max = 0.4; 
left_panel_sidebar_width = 50
left_panel_main_scrollbar_width = 10

right_panel_width = window_width - left_panel_width
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
standard_row_height_constant = 15
h1_font_size = 24
h2_font_size = 20
h3_font_size = 16
dialog_box_font_size = 16
message_callout_radius = 20

label_width_ratio = 8
label_width_ratio_wrap = 6

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

avatar_message_box_color_list = {
    "female_avatar_1.png": (255, 208, 200), 
    "female_avatar_2.png": (220, 246, 249), 
    "female_avatar_3.png": (225, 215, 213), 
    "female_avatar_4.png": (247, 247, 187), 
    "female_avatar_5.png": (246, 226, 217), 
    "female_avatar_6.png": (235, 219, 222), 
    "male_avatar_1.png": (249, 229, 192), 
    "male_avatar_2.png": (255, 218, 210), 
    "male_avatar_3.png": (247, 231, 196), 
    "male_avatar_4.png": (230, 247, 233), 
    "male_avatar_5.png": (248, 214, 206), 
    "male_avatar_6.png": (199, 241, 255), 
    "RTSAI_avatar.png": (197, 249, 255), 
}

dialog_box_icon_size = 20
message_sender_icon_size = 36
message_pady = 5
