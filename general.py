import tkinter as tk
from PIL import Image, ImageTk
import time



from variables import widgets, original_images, image_cache, u_scale, last_resize_time, event_calls, multiplier, current_scale, radiobutton_options

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
    

def load_images():
    original_images["selected"] = Image.open("img/radiobuttons/selected.png")
    original_images["unselected"] = Image.open("img/radiobuttons/unselected.png")


def get_scaled_radio_buttons(size):
    
    size = int(size)
    
    cache_key = f"radio_{size}"
    if f"{cache_key}_selected" in image_cache:
       return image_cache[f"{cache_key}_selected"], image_cache[f"{cache_key}_unselected"]
    
    selected_img = original_images["selected"].resize((size, size), Image.Resampling.LANCZOS)
    unselected_img = original_images["unselected"].resize((size, size), Image.Resampling.LANCZOS)
    
    selected_photo = ImageTk.PhotoImage(selected_img)
    unselected_photo = ImageTk.PhotoImage(unselected_img)
    
    image_cache[f"{cache_key}_selected"] = selected_photo
    image_cache[f"{cache_key}_unselected"] = unselected_photo
    
    return selected_photo, unselected_photo


def enforce_int(input, placeholder_text="Rec 5-15"):
    if input == "" or input == placeholder_text:
        return True
    return input.isdigit() 


def strike(text):
    result = ''
    for c in text:
        result += (c if c != ' ' else '\u00a0') + '\u0336'
    return result

def update_u_scale(value, window):
    global u_scale
    u_scale = float(value)
    resizer(window)






def resizer(window, force=False):
    global current_scale
    global last_resize_time
    global event_calls
    global multiplier
    event_calls += 1
    if event_calls == multiplier:
        multiplier += 100
    

    
    current_width = window.winfo_width()
    current_height = window.winfo_height()


    need_resizing = False
    new_width = current_width
    new_height = current_height


    if current_width < 1280:
        new_width = 1280
        need_resizing = True
    if current_height < 720:
        new_height = 720
        need_resizing = True

    if need_resizing:
        window.geometry(f"{new_width}x{new_height}")
        return
    
    current_time = time.time()    
    if current_time - last_resize_time < 0.1:
        return
    
    last_resize_time = current_time
        

    prescaled = scaling(current_width, current_height)
    true_scale = max(1.0,min(2.5, prescaled * u_scale))
    if not force and true_scale == 2.5 and current_scale == 2.5:
            return
    current_scale = true_scale
    selected_img, unselected_img = get_scaled_radio_buttons(12 * true_scale)
    window.tk.call("tk", "scaling", true_scale)
    for widget in widgets:
        defaults = widget["default properties"]
        scaled_font = int(defaults["font size"] * true_scale)
        if widget["widget type"] in ["Button", "Label", "Entry", "Scale", "Radio"]:
            widget["widget"].config(font=("default", scaled_font))
        if widget["widget type"] == "Radiobutton":

            widget["widget"].config(font=("default", scaled_font), image=unselected_img, selectimage=selected_img)




def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    
    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')
    
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

def get_real_value(entry, placeholder_text):
    value = entry.get()
    return "" if value == placeholder_text else value


def page_cleaner(widget_list):
    for widget in widget_list:
        widget["widget"].place_forget()