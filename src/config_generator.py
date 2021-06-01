""" generate a config if none found """
import tkinter as tk
import configparser
import regex
from tkinter import ttk
from tkcalendar import DateEntry

from common import GOOD_PLZ

NOTIFIERS = ["EMail", "Telegram", "Apprise", "Webbrowser"]
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
    },
    "Apprise": {
        "service_urls": "Different Service URLs"
    }
}
# from emailregex.com, adapted for python syntax
MAIL_REGEX = r"\b(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])\b"
NOTIFIER_REGEX = {
    "sender": MAIL_REGEX,
    "password": r"\b[^ ]+\b",   # match anything not a space
    "server": r"\b[\p{L}\p{N}\-\.]+\b",    # match alphanumeric characters, dash, and dot
    "port": r"\b\d{2,}\b",
    "receivers": r"\b" + MAIL_REGEX + r"(," + MAIL_REGEX + r")*\b",
    "token": r"\b[0-9]{7,}\:[a-zA-Z0-9\-\_]+\b",    # I hope this covers all possible tokens
    "chat_ids": r"\b\d{5,}(,\d{5,})*\b" # matches a list of numbers
    "service_urls": r"\b[^ ]+\b",   # match anything not a space
}

def init_input(config_dict):
    config_dict["COMMON"] = {}
    for item in NOTIFIERS:
        config_dict[item.upper()] = {}
    config_dict["ADVANCED"] = {}
    config_dict["ADVANCED"]["sleep_between_requests_in_s"] = "300"
    config_dict["ADVANCED"]["sleep_between_failed_requests_in_s"] = "30"
    config_dict["ADVANCED"]["sleep_after_ipban_in_min"] = "180"
    config_dict["ADVANCED"]["cooldown_after_found_in_min"] = "15"
    config_dict["ADVANCED"]["jitter"] = "15"
    config_dict["ADVANCED"]["sleep_at_night"] = "true"
    config_dict["ADVANCED"]["user_agent"] = "impfbot"

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
        for item in NOTIFIERS:
            config_dict[item.upper()]["enable"] = str(enable[item].get()).lower()

    def create_subwindow(event):
        """ when selecting a notifier, show a new window with the required options """
        def close_subwindow():
            """ get values and close window """
            if validate_notifier_input():
                for field in FIELDS[notifier]:
                    config_dict[notifier.upper()][field] = input_arr[field].get()
                subwindow.destroy()
            else:
                open_alert_window(msg="Bitte alle Felder ausfüllen.")

        def validate_notifier_input():
            """ check for empty input """
            for item in input_arr:
                match = regex.match(NOTIFIER_REGEX[item], input_arr[item].get())
                if match is None:
                    return False
            return True

        notifier = event.widget.cget("text")
        if notifier != "Webbrowser" and not enable[notifier].get():
            enable[notifier].set(not enable[notifier].get())
            input_arr = {}
            subwindow = tk.Toplevel(tk_window)
            row_index = 0
            notifier_fields = FIELDS[notifier]
            for field in notifier_fields:
                tk.Label(subwindow, text=notifier_fields[field]).grid(row=row_index, column=0)
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

    def check_notifiers_enabled():
        """ check whether any notifier is enabled """
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
        if not check_notifiers_enabled():
            open_alert_window(msg="Bitte eine Art der Benachrichtigung auswählen!")
        elif not validate_input():
            open_alert_window(msg="Bitte korrekte Daten eingeben.")
        else:
            get_input()
            tk_window.destroy()

    def cancel():
        config_dict = {}
        tk_window.destroy()

    def advanced_settings():
        def close_settings_window():
            for field in config_dict["ADVANCED"]:
                config_dict["ADVANCED"][field] = advanced_settings_input[field].get()
            settings_window.destroy()

        settings_window_row_index = 0
        settings_window = tk.Toplevel(tk_window)
        advanced_settings_input = {}
        for field in config_dict["ADVANCED"]:
            tk.Label(
                settings_window,
                text=field
            ).grid(row=settings_window_row_index, column=0)
            advanced_settings_input[field] = tk.Entry(settings_window)
            advanced_settings_input[field].grid(row=settings_window_row_index, column=1)
            advanced_settings_input[field].insert(0, config_dict["ADVANCED"][field])
            settings_window_row_index += 1
        close_advanced = tk.Button(settings_window, text="Fenster schließen", command=close_settings_window)
        close_advanced.grid(row=settings_window_row_index, column=1)

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
    for item in NOTIFIERS:
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

    close = tk.Button(tk_window, text="Speichern und schließen", command=close_window)
    close.grid(row=row_index + 1, column=1)

    advanced = tk.Button(tk_window, text="Weitere Einstellungen", command=advanced_settings)
    advanced.grid(row=row_index + 2, column=1)

    tk_window.mainloop()



def run_cli_config(config_dict):
    def get_notifier_credentials(notifier):
        notifier_input = {}
        notifier_input["enable"] = "true"
        for field in FIELDS[notifier]:
            match = None
            while match is None:
                notifier_input[field] = input(f'{FIELDS[notifier][field]}: ')
                match = regex.match(NOTIFIER_REGEX[field], notifier_input[field])
        return notifier_input

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

    enable_notifier = {}
    for notifier in FIELDS:
        input_res = ""
        while input_res.lower() not in ["j", "n"]:
            input_res = input(
                f'Soll per {notifier} benachrichtigt werden? (j/n): '
            ).lower()
        enable_notifier[notifier] = input_res == "j"
        if enable_notifier[notifier]:
            config_dict[notifier.upper()] = get_notifier_credentials(notifier)
        else:
            config_dict[notifier.upper()]["enable"] = "false"

    enable_browser_input = ""
    while enable_browser_input.lower() not in ["j", "n"]:
        enable_browser_input = input('Soll bei Benachrichtigung ein '
            'Browserfenster geöffnet werden? (j/n): ').lower()
    enable_browser = str(enable_browser_input.lower() == "j").lower()

    config_dict["COMMON"]["geburtstag"] = birthday
    config_dict["COMMON"]["postleitzahl"] = plz
    config_dict["WEBBROWSER"]["enable"] = enable_browser

    return config_dict
