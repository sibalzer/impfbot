""" generate a config if none found """
import tkinter as tk
import configparser
from tkinter import ttk
from tkcalendar import DateEntry

NOTIFICATORS = ["EMail", "Telegram", "Webbrowser"]
FIELDS = {
    "EMail": {
        "sender": "Absender",
        "password": "Passwort",
        "server": "Server",
        "port": "Port",
        "receivers": "Empfänger"
    },
    "Telegram": {
        "token": "Token",
        "chat_ids": "Chat-IDs"
    }
}
def init_input(config_dict):
    config_dict["COMMON"] = {}
    for item in NOTIFICATORS:
        config_dict[item.upper()] = {}

def start_config_generation(config_dict):
    """ entry point for config generation """
    run_gui = True
    try:
        gui_window = tk.Tk()
    except tk.TclError:
        # most likely no display was found (i. e. running headless)
        run_gui = False

    init_input(config_dict)
    if run_gui:
        run_gui_config(gui_window, config_dict)
    else:
        run_cli_config()

def run_gui_config(tk_window, config_dict):
    """ create a window for data entry """

    def get_input():
        config_dict["COMMON"]["geburtstag"] = birthday.get()
        config_dict["COMMON"]["postleitzahl"] = plz.get()
        for item in NOTIFICATORS:
            config_dict[item.upper()]["enable"] = str(enable[item].get()).lower()
        with open("config.ini", "w") as configfile:
            config_dict.write(configfile)
        return config_dict

    def create_subwindow(event):
        """ when selecting a notificator, show a new window with the required options """
        def close_subwindow():
            for field in FIELDS[notificator]:
                config_dict[notificator.upper()][field] = input_arr[field].get()
            subwindow.destroy()

        notificator = event.widget.cget("text")
        if notificator != "Webbrowser" and not enable[notificator].get():
            enable[notificator].set(not enable[notificator].get())
            input_arr = {}
            subwindow = tk.Toplevel(tk_window)
            row_index = 0
            notificator_fields = FIELDS[notificator]
            for field in notificator_fields:
                tk.Label(subwindow, text=notificator_fields[field]).grid(row=row_index, column=0)
                input_arr[field] = tk.Entry(subwindow)
                input_arr[field].grid(row=row_index, column=1)
                row_index += 1
            
            close = tk.Button(subwindow, text="Fenster schließen", command=close_subwindow)
            close.grid(row=row_index, column=1)

    def close_window():
        get_input()
        tk_window.destroy()

    tk_window.geometry("400x400+250+100")

    row_index = 6
    checkboxes = {}
    enable = {}

    tk.Label(tk_window, text="Geburtsdatum", font="bold").grid(row=1, column=1)
    tk.Label(tk_window, text="PLZ", font="bold").grid(row=3, column=1)

    birthday = DateEntry(tk_window, width=18)
    plz = tk.Entry(tk_window)

    birthday.grid(row=2, column=1)
    plz.grid(row=4, column=1)

    tk.Label(tk_window, text="Benachrichtigung", font="bold").grid(row=5, column=1)
    for item in NOTIFICATORS:
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


def run_cli_config(config_dict):
    def get_mail_credentials():
        config_dict["EMAIL"]["enable"] = "true"
        mail_input = {}
        for field in FIELDS["EMail"]:
            mail_input[field] = input(f'{FIELDS["EMail"][field]}: ')
        return mail_input
    
    def get_telegram_credentials():
        config_dict["TELEGRAM"]["enable"] = "true"
        telegram_input = {}
        for field in FIELDS["EMail"]:
            telegram_input[field] = input(f'{FIELDS["Telegram"][field]}: ')
        return telegram_input

    birthday = input('Bitte den Geburtstag eingeben: ')
    plz = input('Bitte die PLZ eingeben: ')
    enable_mail_input = input('Soll per E-Mail benachrichtigt werden? (j/n): ')
    enable_mail = True if enable_mail_input.lower() == "j" else False
    if enable_mail:
        config_dict["EMAIL"] = get_mail_credentials()
    else:
        config_dict["EMAIL"]["enable"] = "false"
    enable_telegram_input = input('Soll per E-Mail benachrichtigt werden? (j/n): ')
    enable_telegram = True if enable_telegram_input.lower() == "j" else False
    if enable_telegram:
        config_dict["TELEGRAM"] = get_telegram_credentials()
    else:
        config_dict["TELEGRAM"]["enable"] = "false"

    config_dict["COMMON"]["geburtstag"] = birthday
    config_dict["COMMON"]["postleitzahl"] = plz

    return config_dict
