""" generate a config if none found """
import tkinter as tk

def start_config_generation():
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
    return 0

def run_cli_config():
    return 0