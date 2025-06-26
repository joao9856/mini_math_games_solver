import tkinter as tk
from widget_interaction import button_click_me
from configs import scaling, add_to_widgets_list, widgets, load_radio_images
window = tk.Tk()
window.geometry("800x600")
window.title("Solver selection")
#widgets = [] #list that stores {"widget object" : (object, {"default_property" : value, ...}), "widget type": "label/button/etc"}
u_scale = 1.0
def resizer(event=None):
    print(f"Resizer called - Event: {event}")
    
    current_width = window.winfo_width()
    current_height = window.winfo_height()


    need_resizing = False
    new_width = current_width
    new_height = current_height


    if current_width < 800:
        new_width = 800
        need_resizing = True
    if current_height < 600:
        new_height = 600
        need_resizing = True

    if need_resizing:
        window.geometry(f"{new_width}x{new_height}")
        return
        


    prescaled = scaling(current_width, current_height)
    true_scale = prescaled * u_scale if prescaled * u_scale >= 1.0 else 1.0
    
    window.tk.call("tk", "scaling", true_scale)
    for widget in widgets:
        defaults = widget["default properties"]
        print(defaults, true_scale)
        if widget["widget type"] == "Button":
            scaled_width = int(defaults["width"] * true_scale)
            scaled_height = int(defaults["height"] * true_scale)
            scaled_font = int(defaults["font size"] * true_scale)

            widget["widget"].config(font=("default", scaled_font))
            widget["widget"].place(width=scaled_width, height=scaled_height)
        if widget["widget type"] == "Radiobutton":
            print(widget["widget"])
            scaled_font = int(defaults["font size"] * true_scale)

            selected_img, unselected_img = load_radio_images(20 * true_scale)

            widget["widget"].config(font=("default", scaled_font), image=unselected_img, selectimage=selected_img)
    print(button.winfo_width(), button.winfo_height())
    #widget_rescaler()
    
   



button = tk.Button(window, text="Click me", command=lambda : button_click_me((window.winfo_width(), window.winfo_height())), font=("default", 12))
button.place(relx= 0.7, rely= 0.05, anchor=tk.CENTER, width=100, height=50)
add_to_widgets_list(button, "Button", 100, 50, 12)

print(widgets, button.winfo_width(), button.winfo_height())

solver_choice = tk.StringVar(value="numbersums")

solvers = [("Number Sums Solver", "numbersums"),
           ("Nonogram Solver", "nonogram"),
           ("Math Crosswords Solver", "mathcross")]

selected_img, unselected_img = load_radio_images(20)
for text, value in solvers:
    radio = tk.Radiobutton(window, text=text, variable=solver_choice, value=value, font=("default", 12), image=unselected_img, selectimage=selected_img, indicatoron=False, compound="left")
    radio.place(relx=0.1, rely=0.2 + solvers.index((text, value)) * 0.1)
    add_to_widgets_list(radio, "Radiobutton", None, None, 12)

window.bind("<Configure>", resizer)
window.mainloop()
