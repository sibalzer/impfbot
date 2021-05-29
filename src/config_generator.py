""" generate a config if none found """
import tkinter as tk
import configparser
import regex
from tkinter import ttk
from tkcalendar import DateEntry

from common import GOOD_PLZ

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
        "chat_ids": "Chat-ID(s)"
    }
}

def init_input(config_dict):
    config_dict["COMMON"] = {}
    for item in NOTIFICATORS:
        config_dict[item.upper()] = {}
    config_dict["ADVANCED"] = {}
    config["ADVANCED"]["sleep_between_requests_in_s"] = "300"
    config["ADVANCED"]["sleep_between_failed_requests_in_s"] = "30"
    config["ADVANCED"]["sleep_after_ipban_in_min"] = "180"
    config["ADVANCED"]["cooldown_after_found_in_min"] = "15"
    config["ADVANCED"]["jitter"] = "15"
    config["ADVANCED"]["sleep_at_night"] = "true"
    config["ADVANCED"]["user_agent"] = "impfbot"

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
        config_dict = run_cli_config(config_dict)

    if config_dict != {}:
        with open("config.ini", "w") as configfile:
            config_dict.write(configfile)

def run_gui_config(tk_window, config_dict):
    """ create a window for data entry """

    def get_input():
        """ read config from form """
        config_dict["COMMON"]["geburtstag"] = birthday.get_date().strftime("%d.%m.%Y")
        config_dict["COMMON"]["postleitzahl"] = plz.get()
        for item in NOTIFICATORS:
            config_dict[item.upper()]["enable"] = str(enable[item].get()).lower()

    def create_subwindow(event):
        """ when selecting a notificator, show a new window with the required options """
        def close_subwindow():
            """ get values and close window """
            if validate_notificator_input():
                for field in FIELDS[notificator]:
                    config_dict[notificator.upper()][field] = input_arr[field].get()
                subwindow.destroy()
            else:
                open_alert_window(msg="Bitte alle Felder ausfüllen.")

        def validate_notificator_input():
            """ check for empty input """
            for item in input_arr:
                if input_arr[item].get() == "":
                    return False
            return True

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
        return 0

    def open_alert_window(msg):
        """ create an alert window """
        def close_alert_window():
            alert_window.destroy()

        alert_window = tk.Toplevel(tk_window)
        tk.Label(alert_window, text=msg).grid(row=0, column=0)
        close_alert = tk.Button(alert_window, text="OK", command=close_alert_window)
        close_alert.grid(row=1, column=0)

    def check_notificators_enabled():
        """ check whether any notificator is enabled """
        for item in enable:
            if enable[item].get():
                return True
        return False

    def validate_input():
        """ validate user input """
        entered_plz = plz.get()
        match = regex.match(r"\b\d{5}\b", entered_plz)
        return match is not None and entered_plz[:2] in GOOD_PLZ

    def close_window():
        """ close the window """
        if not check_notificators_enabled():
            open_alert_window(msg="Bitte eine Art der Benachrichtigung auswählen!")
        elif not validate_input():
            open_alert_window(msg="Bitte korrekte Daten eingeben.")
        else:
            get_input()
            tk_window.destroy()

    def cancel():
        config_dict = {}
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
            onvalue=True
        )
        checkboxes[item].bind('<Button-1>', create_subwindow)
        checkboxes[item].grid(row=row_index, column=1)
        row_index += 1

    tk_window.columnconfigure(0, weight=1)
    tk_window.columnconfigure(2, weight=1)

    confirm = tk.Button(tk_window, text="Abbrechen", command=cancel)
    confirm.grid(row=row_index, column=1)

    close = tk.Button(tk_window, text="Fenster schließen", command=close_window)
    close.grid(row=row_index + 1, column=1)

    tk_window.mainloop()

    return config_dict


def run_cli_config(config_dict):
    def get_notificator_credentials(notificator):
        config_dict[notificator.upper()]["enable"] = "true"
        notificator_input = {}
        for field in FIELDS[notificator]:
            notificator_input[field] = ""
            while notificator_input[field] == "":
                notificator_input[field] = input(f'{FIELDS[notificator][field]}: ')
        return notificator_input

    birthday = ""
    plz = ""
    match = None
    while match is None:
        birthday = input('Bitte den Geburtstag eingeben: ')
        match = regex.match(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", birthday)
    match = None
    while match is None or plz[:2] not in GOOD_PLZ:
        plz = input('Bitte die PLZ eingeben: ')
        match = regex.match(r"\b\d{5}\b", plz)

    enable_notificator = {}
    for notificator in FIELDS:
        input_res = ""
        while input_res.lower() not in ["j", "n"]:
            input_res = input(
                f'Soll per {notificator} benachrichtigt werden? (j/n): '
            ).lower()
        enable_notificator[notificator] = input_res == "j"
        if enable_notificator[notificator]:
            config_dict[notificator.upper()] = get_notificator_credentials(notificator)
        else:
            config_dict[notificator.upper()]["enable"] = "false"

    enable_browser_input = ""
    while enable_browser_input.lower() not in ["j", "n"]:
        enable_browser_input = input('Soll bei Benachrichtigung ein'
            'Browserfenster geöffnet werden? (j/n): ').lower()
    enable_browser = str(enable_browser_input.lower() == "j").lower()

    config_dict["COMMON"]["geburtstag"] = birthday
    config_dict["COMMON"]["postleitzahl"] = plz
    config_dict["WEBBROWSER"]["open_browser"] = enable_browser

    return config_dict
