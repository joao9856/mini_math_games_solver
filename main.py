import tkinter as tk
from widget_interaction import button_click_me
from configs import add_to_widgets_list, get_scaled_radio_buttons, load_images, enforce_int, strike, update_u_scale, resizer, add_placeholder, get_real_value
from variables import widgets

window = tk.Tk()
window.geometry("800x600")
window.title("Solver selection")

load_images()
validate_int = window.register(lambda x: enforce_int(x, "Rec 5-25"))




button = tk.Button(window, text="Create Board", command=lambda : button_click_me((window.winfo_width(), window.winfo_height())), font=("default", 12), width=13)
button.place(relx= 0.5, rely= 0.4)
add_to_widgets_list(button, "Button", default_font_size=12)

print(widgets, button.winfo_width(), button.winfo_height())

solver_choice = tk.StringVar(value="numbersums")

solvers = [("Number Sums Solver", "numbersums"),
           (strike("Nonogram Solver"), "nonogram"),
           (strike("Math Crosswords Solver"), "mathcross")]

selected_img, unselected_img = get_scaled_radio_buttons(12)
for text, value in solvers:
    radio = tk.Radiobutton(window, text=text, variable=solver_choice, value=value, font=("default", 12), image=unselected_img, selectimage=selected_img, indicatoron=False, compound="left")
    radio.place(relx=0.1, rely=0.2 + solvers.index((text, value)) * 0.1)
    add_to_widgets_list(radio, "Radiobutton", None, None, 12)

label = tk.Label(window, text="Board width", font=("default", 12), width=13)
label.place(relx=0.5, rely=0.2)
add_to_widgets_list(label, "Label", default_font_size=12)

board_size_input = tk.Entry(window, font=("default", 12), validate="key", validatecommand=(validate_int, "%P"), width=13)
board_size_input.place(relx=0.5, rely=0.3)
add_placeholder(board_size_input, "Rec 5-25")
add_to_widgets_list(board_size_input, "Entry", default_font_size=12)

slider = tk.Scale(window, from_=0.5, to=1.0, orient="horizontal", label="Scale", font=("default", 12), resolution=0.1, command=lambda value:update_u_scale(value, window), length=250)
slider.set(1.0)
slider.place(relx=0.9, rely=0.9, anchor="se")
add_to_widgets_list(slider, "Scale", default_font_size=12)









window.bind("<Configure>", lambda event: resizer(window))
window.mainloop()
