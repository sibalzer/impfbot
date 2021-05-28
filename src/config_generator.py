""" generate a config if none found """
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def start_config_generation():
    """ entry point for config generation """
    run_gui = True
    try:
        gui_window = tk.Tk()
    except tk.TclError:
        # most likely no display was found (i. e. running headless)
        run_gui = False

    if run_gui:
        run_gui_config(gui_window)
    else:
        run_cli_config()

def run_gui_config(tk_window):
    """ create a window for data entry """
    tk_window.geometry("400x400+250+100")

    row_index = 6
    notificators = ["Mail", "Telegram", "Browser"]
    checkboxes = {}
    enable = {}

    tk.Label(tk_window, text="Geburtsdatum", font="bold").grid(row=1, column=1)
    tk.Label(tk_window, text="PLZ", font="bold").grid(row=3, column=1)

    birthday = DateEntry(tk_window, width=18)
    plz = tk.Entry(tk_window)

    birthday.grid(row=2, column=1)
    plz.grid(row=4, column=1)

    tk.Label(tk_window, text="Benachrichtigung", font="bold").grid(row=5, column=1)
    for item in notificators:
        enable[item] = tk.BooleanVar()
        checkboxes[item] = ttk.Checkbutton(tk_window, text=item, variable=enable[item], onvalue=True)
        checkboxes[item].grid(row=row_index, column=1)
        row_index += 1

    tk_window.columnconfigure(0, weight=1)
    tk_window.columnconfigure(2, weight=1)
    tk_window.mainloop()

def run_cli_config():
    return 0