import tkinter as tk
from general import load_images, resizer
from main_page import main_page_loader
from variable_creation import fill_var
from PIL import Image, ImageTk

window = tk.Tk()
window.geometry("1280x720")

icon_16 = ImageTk.PhotoImage(Image.open("img/icon/icon.png").resize((16, 16)))
icon_32 = ImageTk.PhotoImage(Image.open("img/icon/icon.png").resize((32, 32)))

window.iconphoto(False, icon_32, icon_16)  # Provide multiple sizes


window.title("Solver selection")
window.winfo_width()
load_images()
fill_var()
main_page_loader(window)


window.bind("<Configure>", lambda event: resizer(window))
window.mainloop()
