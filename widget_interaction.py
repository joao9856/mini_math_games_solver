from general import page_cleaner
from variables import widgets, radiobutton_options


def button_click_me(choice, window, size):
    if size.isdigit() == False:
        return
    size = int(size)
    page_cleaner(widgets)
    game = radiobutton_options[choice]
    game(window, size)