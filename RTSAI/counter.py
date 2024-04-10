
ID_counter = 0
def new_ID(): 
    global ID_counter; ID_counter += 1
    return ID_counter

resize_window_ID_counter = 0
def new_resize_window_ID(): 
    global resize_window_ID_counter; resize_window_ID_counter += 1
    return resize_window_ID_counter