
import math
from tkinter.font import Font

def show_popup_message(message, title = "Message", parent_item = None):
    import tkinter
    tkinter.messagebox.showinfo(title, message, parent = parent_item)

def wrap_label_text(parent_label, expected_row_width, label_text_original = None): 
    '''
    Rendering the label_text, by adding necessary newline characters
    '''

    # Calculate the expected row width
    font = Font(font=parent_label.cget("font"))
    if (not label_text_original): 
        label_text_original = parent_label.cget("text")
    remaining_text = label_text_original
    rendered_text = ""

    while remaining_text: 

        remaining_width = font.measure(remaining_text)
        remaining_density = remaining_width / len(remaining_text)
        total_characters = min(len(remaining_text), math.floor(expected_row_width / remaining_width * len(remaining_text)))
        cropped_text = remaining_text[0:total_characters]

        if (total_characters != len(remaining_text)): 
            # diff_char_nums can either be positive (need more characters) or negative
            diff_char_nums = math.floor((expected_row_width - font.measure(cropped_text)) / remaining_density)
            while (abs(diff_char_nums) > 3): # let us fix the error threshold to be 3
                print (diff_char_nums)
                total_characters += diff_char_nums
                cropped_text = remaining_text[0:total_characters]
                remaining_density = remaining_width / len(remaining_text)
                diff_char_nums = math.floor((expected_row_width - font.measure(cropped_text)) / remaining_density)

        # Check if the next character is not a space to avoid breaking words
        if total_characters < len(remaining_text) and remaining_text[total_characters] != ' ':
            last_space_index = cropped_text.rfind(' ')
            if last_space_index != -1:
                cropped_text = cropped_text[:last_space_index + 1]
                total_characters = last_space_index + 1

        # Add the cropped text to the rendered text with a newline character
        # Skip multiple new line characters
        if (not (rendered_text.endswith('\n\n') and cropped_text == '\n')): 
            rendered_text += cropped_text + '\n'
        remaining_text = remaining_text[total_characters:]

    '''
    Finalize the label text
    '''
    parent_label.configure(text=rendered_text.rstrip())
    parent_label.configure(width=expected_row_width)
