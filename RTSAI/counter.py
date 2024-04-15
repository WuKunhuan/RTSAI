
ID_counter = 0
def new_ID(): 
    global ID_counter; ID_counter += 1
    return ID_counter

KG_element_ID_counter = 0
def KG_element_ID(): 
    global KG_element_ID_counter; KG_element_ID_counter += 1
    return KG_element_ID_counter