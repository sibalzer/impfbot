""" generate a config if none found """
import tkinter as tk
import configparser
from tkinter import ttk
from tkcalendar import DateEntry

def start_config_generation(config_dict):
    """ entry point for config generation """
    run_gui = True
    try:
        gui_window = tk.Tk()
    except tk.TclError:
        # most likely no display was found (i. e. running headless)
        run_gui = False

    if run_gui:
        run_gui_config(gui_window, config_dict)
    else:
        run_cli_config()



def run_gui_config(tk_window, config_dict):
    """ create a window for data entry """
    def get_input():
        config_dict["COMMON"] = {}
        config_dict["COMMON"]["geburtstag"] = birthday.get()
        config_dict["COMMON"]["postleitzahl"] = plz.get()
        for item in notificators:
            config_dict[item.upper()] = {}
            config_dict[item.upper()]["enable"] = str(enable[item].get()).lower()
        with open("test.ini", "w") as configfile:
            config_dict.write(configfile)

    def create_subwindow(event):
        def close_subwindow():
            subwindow.destroy()
        notificator = event.widget.cget("text")
        if notificator != "Webbrowser" and not enable[notificator].get():
            enable[notificator].set(not enable[notificator].get())
            fields = {
                "EMail": {"sender": "Empfänger",
                    "password": "Passwort",
                    "server": "Server",
                    "port": "Port",
                    "receivers": "Empfänger"
                },
                "Telegram": {"token": "Token",
                    "chat_ids": "Chat-IDs"
                }
            }
            input_arr = {}
            subwindow = tk.Toplevel(tk_window)
            row_index = 0
            notificator_fields = fields[notificator]
            for field in notificator_fields:
                tk.Label(subwindow, text=notificator_fields[field]).grid(row=row_index, column=0)
                input_arr[field] = tk.Entry(subwindow)
                input_arr[field].grid(row=row_index, column=1)
                row_index += 1
            
            close = tk.Button(subwindow, text="Fenster schließen", command=close_subwindow)
            close.grid(row=row_index, column=1)

    def close_window():
        tk_window.destroy()

    tk_window.geometry("400x400+250+100")

    row_index = 6
    notificators = ["EMail", "Telegram", "Webbrowser"]
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
        enable[item].set(False)
        checkboxes[item] = ttk.Checkbutton(
            tk_window,
            text=item,
            variable=enable[item],
            command=create_subwindow,
            onvalue=True
        )
        checkboxes[item].bind('<Button-1>', create_subwindow)
        checkboxes[item].grid(row=row_index, column=1)
        row_index += 1

    tk_window.columnconfigure(0, weight=1)
    tk_window.columnconfigure(2, weight=1)

    confirm = tk.Button(tk_window, text="Eintragen", command=get_input)
    confirm.grid(row=row_index, column=1)

    close = tk.Button(tk_window, text="Fenster schließen", command=close_window)
    close.grid(row=row_index + 1, column=1)

    tk_window.mainloop()

def run_cli_config():
    return 0