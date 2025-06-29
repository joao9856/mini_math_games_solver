from variables import radiobutton_options
from nums_sums import load_num_sums_page

def fill_var():
    radiobutton_options["numbersums"] = load_num_sums_page
    radiobutton_options["nonogram"] = "coming soon"
    radiobutton_options["mathcross"] = "coming soon"