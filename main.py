import tkinter as tk
from general import load_images, enforce_int, resizer
from main_page import main_page_loader
from variable_creation import fill_var

window = tk.Tk()
window.geometry("800x600")
window.title("Solver selection")
window.winfo_width()
load_images()
fill_var()
validate_int = window.register(lambda x: enforce_int(x, "Rec 5-15"))
main_page_loader(window, validate_int)


window.bind("<Configure>", lambda event: resizer(window))
window.mainloop()
