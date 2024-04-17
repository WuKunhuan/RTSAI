
import RTSAI.UI_config as UI_config
from RTSAI.tool_funcs import color_tuple_to_rgb

debug = 1

def round_rectangle_points(x1, y1, x2, y2, radius): 
    return([
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
        x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
        x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
        x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
        x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ])

def draw_chat_icon(parent_canvas, canvas_width = None, canvas_height = None, fill = color_tuple_to_rgb(UI_config.VSCode_font_grey_color)): 
    '''
    Draw the chat logo: Left_Sidebar_Icon class
    '''

    if (not canvas_width): canvas_width = parent_canvas.winfo_width()
    if (not canvas_height): canvas_height = parent_canvas.winfo_height()
    parent_canvas.delete("item_1_rectangle")
    parent_canvas.delete("item_2_triangle")
    item_1_rectangle_coords = round_rectangle_points(0.2 * canvas_width, 0.2 * canvas_height, 0.8 * canvas_width, 0.6 * canvas_height, 0.2 * canvas_height)
    item_2_triangle_coords = [
        canvas_width * 0.35, canvas_height * 0.6,
        canvas_width * 0.3, canvas_height * 0.75,
        canvas_width * 0.5, canvas_height * 0.6, 
    ]
    parent_canvas.create_polygon(item_1_rectangle_coords, fill = fill, tags="item_1_rectangle", smooth=True, outline = "")
    parent_canvas.create_polygon(item_2_triangle_coords, fill = fill, tags="item_2_triangle", outline = "")
    parent_canvas.items_in_panel = ["item_1_rectangle", "item_2_triangle"]

def draw_crawl_icon(parent_canvas, canvas_width = None, canvas_height = None, fill = color_tuple_to_rgb(UI_config.VSCode_font_grey_color)): 
    '''
    Draw the web crawl logo: Left_Sidebar_Icon class
    '''

    if (not canvas_width): canvas_width = parent_canvas.winfo_width()
    if (not canvas_height): canvas_height = parent_canvas.winfo_height()

    parent_canvas.delete("item_1_spider_body")
    parent_canvas.delete("item_8_spider_head")
    parent_canvas.delete("item_2_spider_leg_1")
    parent_canvas.delete("item_3_spider_leg_2")
    parent_canvas.delete("item_4_spider_leg_3")
    parent_canvas.delete("item_5_spider_leg_4")
    parent_canvas.delete("item_6_spider_leg_5")
    parent_canvas.delete("item_7_spider_leg_6")

    def spider_leg_points(x, y, x_first_joint, y_first_joint, thickness):
        return [
            x, y - thickness / 2, 
            x, y + thickness / 2, 
            x_first_joint, y_first_joint + thickness / 2, 
            2 * x_first_joint - x, 3 * y_first_joint - 2 * y + thickness / 2, 
            2 * x_first_joint - x, 3 * y_first_joint - 2 * y - thickness / 2, 
            x_first_joint, y_first_joint - thickness / 2, 
        ]
    
    parent_canvas.create_oval(0.3 * canvas_width, 0.3 * canvas_height, 0.7 * canvas_width, 0.7 * canvas_height, fill=fill, tags="item_1_spider_body", outline = "")
    parent_canvas.create_oval(0.4 * canvas_width, 0.2 * canvas_height, 0.6 * canvas_width, 0.4 * canvas_height, fill=fill, tags="item_8_spider_head", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.4 * canvas_height, 0.27 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_2_spider_leg_1", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.5 * canvas_height, 0.27 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=fill, tags="item_3_spider_leg_2", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.35 * canvas_width, 0.6 * canvas_height, 0.27 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_4_spider_leg_3", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.4 * canvas_height, 0.73 * canvas_width, 0.35 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_5_spider_leg_4", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.5 * canvas_height, 0.73 * canvas_width, 0.5 * canvas_height, 0.06 * canvas_height), fill=fill, tags="item_6_spider_leg_5", outline = "")
    parent_canvas.create_polygon(spider_leg_points(0.65 * canvas_width, 0.6 * canvas_height, 0.73 * canvas_width, 0.65 * canvas_height, 0.07 * canvas_height), fill=fill, tags="item_7_spider_leg_6", outline = "")
    parent_canvas.items_in_panel = ["item_1_spider_body", "item_8_spider_head", "item_2_spider_leg_1", "item_3_spider_leg_2", "item_4_spider_leg_3", "item_5_spider_leg_4", "item_6_spider_leg_5", "item_7_spider_leg_6"]

def draw_message_callout(parent_canvas, canvas_width, canvas_height, radius = 0, fill = color_tuple_to_rgb(UI_config.VSCode_font_grey_color)): 
    '''
    Draw the message callout: tkinter.Canvas class
    '''

    if (not canvas_width): canvas_width = parent_canvas.winfo_width()
    if (not canvas_height): canvas_height = parent_canvas.winfo_height()
    if (debug == 1): print (f"Message callout canvas size: ({canvas_width}, {canvas_height})")
    parent_canvas.delete("item_1_message_callout")
    item_1_message_callout_coords = round_rectangle_points(0, 0, canvas_width, canvas_height, radius)
    parent_canvas.create_polygon(item_1_message_callout_coords, fill = fill, tags="item_1_message_callout", smooth=True, outline = "")

