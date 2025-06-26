import tkinter as tk
from PIL import Image, ImageTk
widgets = [] #list that stores {"widget object" : (object, {"default_property" : value, ...}), "widget type": "label/button/etc"}
image_cache = {}

def scaling(width, height):
    return width / 800 if width / 800 <= height / 600 else height / 600


def add_to_widgets_list(widget,widget_type, default_width=None, default_height=None, default_font_size=None):
    
    widgets.append({"widget" : widget,
                    "default properties" : {
                             "width" : default_width,
                             "height" : default_height,
                             "font size" : default_font_size

                    },
                    "widget type" : widget_type})
    

def load_radio_images(size):
    selected_img = Image.open("img/radiobuttons/selected.png").resize((size, size))
    unselected_img = Image.open("img/radiobuttons/unselected.png").resize((size, size,))
    
    selected_photo = ImageTk.PhotoImage(selected_img)
    unselected_photo = ImageTk.PhotoImage(unselected_img)
    
    image_cache["selected"] = selected_photo
    image_cache["unselected"] = unselected_photo
    
    return selected_photo, unselected_photo