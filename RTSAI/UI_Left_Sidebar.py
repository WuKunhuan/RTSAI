
import tkinter, os
from PIL import ImageTk, Image
import RTSAI.config as config
import RTSAI.UI_config as UI_config
import RTSAI.UI_components as UI_components
from RTSAI.tool_funcs import color_tuple_to_rgb
from RTSAI.UI_Art import draw_chat_icon, draw_crawl_icon

debug = 1

avatars_directory = os.path.join(config.PACKAGE_PATH, "assets", "images", "avatars")

class Left_Sidebar_Icon(tkinter.Canvas):
    '''
    The left sidebar icon objects
    '''
    def __init__(self, hover_color = UI_config.VSCode_highlight_color):
        super().__init__(master = UI_components.left_panel_sidebar, width=UI_config.left_panel_sidebar_width, height=UI_config.left_panel_sidebar_width, 
                            bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness=0)
        self.hovered = False
        self.hover_color = hover_color
        self.items_in_panel = []
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.pack(side = "top")

    def on_enter(self, event): 
        self.hovered = True
        for item in self.items_in_panel: 
            self.itemconfigure(item, fill=color_tuple_to_rgb(self.hover_color))

    def on_leave(self, event):
        self.hovered = False
        for item in self.items_in_panel: 
            self.itemconfigure(item, fill=color_tuple_to_rgb(UI_config.VSCode_font_grey_color))
            
def on_avatar_hover_handler(canvas, item, change_image):
    def on_avatar_hover(event): 
        canvas.itemconfig(item, image = change_image)
    return on_avatar_hover

def on_avatar_leave_handler(canvas, item, original_image):
    def on_avatar_leave(event):
        canvas.itemconfig(item, image=original_image)
    return on_avatar_leave

def on_avatar_change_handler(filename):
    def on_avatar_change(event): 
        if (debug == 1): print (f"Change user avatar to {filename}")
        UI_config.user_avatar = filename
        update_current_avatar_image()
        update_current_avatar_image_user_setting()
    return on_avatar_change

def update_current_avatar_image(): 
    current_avatar_image = Image.open(f"{avatars_directory}/{UI_config.user_avatar}")
    current_avatar_image_resized = current_avatar_image.resize((UI_config.left_panel_sidebar_width - 10, UI_config.left_panel_sidebar_width - 10))
    UI_components.avatar_image = ImageTk.PhotoImage(current_avatar_image_resized)
    UI_components.avatar_image_item = UI_components.left_panel_sidebar_logo.create_image(5, 5, image=UI_components.avatar_image, anchor="nw")
    UI_components.left_panel_sidebar_logo.bind("<Enter>", 
        on_avatar_hover_handler(UI_components.left_panel_sidebar_logo, UI_components.avatar_image_item, UI_components.avatar_image_change))
    UI_components.left_panel_sidebar_logo.bind("<Leave>", 
        on_avatar_leave_handler(UI_components.left_panel_sidebar_logo, UI_components.avatar_image_item, UI_components.avatar_image))

def update_current_avatar_image_user_setting(): 
    current_avatar_image = Image.open(f"{avatars_directory}/{UI_config.user_avatar}")
    current_avatar_image_resized = current_avatar_image.resize((30, 30))
    UI_components.avatar_image_in_setting = ImageTk.PhotoImage(current_avatar_image_resized)
    UI_components.avatar_item_in_setting = UI_components.avatar_canvas_in_setting.create_image(0, 0, image=UI_components.avatar_image_in_setting, anchor='nw')

def create_left_sidebar(): 
    '''
    Fill in the sidebar of the left panel
    binds open editor to create the right panel editor
    create the user logo on the bottom
    '''

    def user_setting(): 
        '''
        User setting UI and interface
        '''

        user_setting_window = tkinter.Toplevel(width = 400, height = 180)
        user_setting_window.title("User Setting")
        user_setting_window.resizable(False, False)
        user_setting_window.pack_propagate(False)

        '''
        Create the 'Current avatar: ' prompt
        Display the current avatar
        '''
        avatar_prompt_frame = tkinter.Frame(user_setting_window)
        UI_components.avatar_canvas_in_setting = tkinter.Canvas(avatar_prompt_frame, width=30, height=30, highlightthickness=0)
        avatar_prompt = tkinter.Label(avatar_prompt_frame, text='Current avatar: ', font=(UI_config.standard_font_family, UI_config.standard_font_size))
        avatar_prompt_2 = tkinter.Label(avatar_prompt_frame, text=', click one below to update: ', font=(UI_config.standard_font_family, UI_config.standard_font_size))
        update_current_avatar_image_user_setting()
        avatar_prompt.pack(side='left')
        UI_components.avatar_canvas_in_setting.pack(side='left', pady = 10)
        avatar_prompt_2.pack(side='left')
        avatar_prompt_frame.pack(side='top')

        '''
        Display all avatars
        '''
        avatars_global_dict = dict()
        avatars_frame_upper = tkinter.Frame(user_setting_window)
        avatars_frame_lower = tkinter.Frame(user_setting_window)
        filenames = sorted(os.listdir(avatars_directory))
        filenames = [name for name in filenames if name.startswith("male_") or name.startswith("female_")]
        if (debug == 0): print (f"All avatars: {filenames}")

        UI_components.avatar_image_change_in_setting = Image.open(f"{avatars_directory}/change_avatar.png")
        UI_components.avatar_image_change_in_setting = ImageTk.PhotoImage(UI_components.avatar_image_change_in_setting.resize((50, 50)))
        for id, filename in enumerate(filenames):
            if (debug == 0): print (f"avatar option: {id}")
            avatars_global_dict[f"avatar_image_others_{id}"] = Image.open(f"{avatars_directory}/{filename}")
            avatars_global_dict[f"avatar_image_others_{id}"] = ImageTk.PhotoImage(avatars_global_dict[f"avatar_image_others_{id}"].resize((50, 50)))
            if id <= 5: 
                avatars_global_dict[f"avatar_image_others_{id}_canvas"] = tkinter.Canvas(avatars_frame_upper, width=50, height=50, highlightthickness=0)
            else: 
                avatars_global_dict[f"avatar_image_others_{id}_canvas"] = tkinter.Canvas(avatars_frame_lower, width=50, height=50, highlightthickness=0)
            avatars_global_dict[f"avatar_image_others_{id}_item"] = avatars_global_dict[f"avatar_image_others_{id}_canvas"]\
                .create_image(0, 0, image=avatars_global_dict[f"avatar_image_others_{id}"], anchor='nw')
            hover_handler = on_avatar_hover_handler(
                avatars_global_dict[f"avatar_image_others_{id}_canvas"],
                avatars_global_dict[f"avatar_image_others_{id}_item"],
                UI_components.avatar_image_change_in_setting
            )
            leave_handler = on_avatar_leave_handler(
                avatars_global_dict[f"avatar_image_others_{id}_canvas"],
                avatars_global_dict[f"avatar_image_others_{id}_item"],
                avatars_global_dict[f"avatar_image_others_{id}"]
            )
            change_handler = on_avatar_change_handler(filename)
            avatars_global_dict[f"avatar_image_others_{id}_canvas"].bind("<Enter>", hover_handler)
            avatars_global_dict[f"avatar_image_others_{id}_canvas"].bind("<Leave>", leave_handler)
            avatars_global_dict[f"avatar_image_others_{id}_canvas"].bind("<Button-1>", change_handler)
            avatars_global_dict[f"avatar_image_others_{id}_canvas"].pack(side='left', padx = 5, pady = 5)

        avatars_frame_upper.pack(side = 'top')
        avatars_frame_lower.pack(side = 'top')
        user_setting_window.mainloop()

    from RTSAI.UI_Left_Sidebar import Left_Sidebar_Icon
    UI_components.left_panel_sidebar_chat = Left_Sidebar_Icon(hover_color = UI_config.chat_icon_color)
    UI_components.left_panel_sidebar_chat.bind("<Configure>", lambda event: draw_chat_icon(UI_components.left_panel_sidebar_chat, UI_config.left_panel_sidebar_width, UI_config.left_panel_sidebar_width))
    UI_components.left_panel_sidebar_crawl = Left_Sidebar_Icon(hover_color = UI_config.crawl_icon_color)
    UI_components.left_panel_sidebar_crawl.bind("<Configure>", lambda event: draw_crawl_icon(UI_components.left_panel_sidebar_crawl, UI_config.left_panel_sidebar_width, UI_config.left_panel_sidebar_width))
    UI_components.left_panel_sidebar_logo = tkinter.Canvas(master = UI_components.left_panel_sidebar, width=UI_config.left_panel_sidebar_width, height=UI_config.left_panel_sidebar_width, 
                bg=color_tuple_to_rgb(UI_config.left_panel_color), highlightthickness=0)
    UI_components.avatar_image_change = Image.open(f"{avatars_directory}/change_avatar.png")
    UI_components.avatar_image_change = ImageTk.PhotoImage(UI_components.avatar_image_change.resize((UI_config.left_panel_sidebar_width - 10, UI_config.left_panel_sidebar_width - 10)))
    update_current_avatar_image()
    UI_components.left_panel_sidebar_logo.pack(side = "bottom")
    UI_components.left_panel_sidebar_logo.bind("<Button-1>", lambda event: user_setting())

