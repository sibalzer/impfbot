""" generate a config if none found """
import re

from common import (
    NOTIFIERS,
    NOTIFIER_REGEX,
    ZIP_REGEX,
    GROUP_SIZE_REGEX,
    BIRTHDATE_REGEX
)
from config_skeleton import SKELETON

try:
    import tkinter as tk
    from tkinter import ttk
    from tkcalendar import DateEntry
    run_gui = True
except ImportError:
    # tk is missing -> run CLI config
    run_gui = False


FIELDS = {
    "EMAIL": {
        "sender": "Absender",
        "user": "User",
        "password": "Passwort",
        "server": "Server",
        "port": "Port",
        "receivers": "Empfänger"
    },
    "TELEGRAM": {
        "token": "Token",
        "chat_ids": "Chat-ID(s)"
    },
    "APPRISE": {
        "service_urls": "Different Service URLs"
    }
}


def init_input(config_dict):
    config_dict["COMMON"] = {}
    for item in NOTIFIERS:
        config_dict[item.upper()] = {}
    config_dict["ADVANCED"] = {}
    config_dict["ADVANCED"]["custom_message_prefix"] = str(
        SKELETON["ADVANCED"]["custom_message_prefix"]["default"])
    config_dict["ADVANCED"]["cooldown_between_requests"] = str(
        SKELETON["ADVANCED"]["cooldown_between_requests"]["default"])
    config_dict["ADVANCED"]["cooldown_between_failed_requests"] = str(
        SKELETON["ADVANCED"]["cooldown_between_failed_requests"]["default"])
    config_dict["ADVANCED"]["cooldown_after_ip_ban"] = str(
        SKELETON["ADVANCED"]["cooldown_after_ip_ban"]["default"])
    config_dict["ADVANCED"]["cooldown_after_success"] = str(
        SKELETON["ADVANCED"]["cooldown_after_success"]["default"])
    config_dict["ADVANCED"]["jitter"] = str(
        SKELETON["ADVANCED"]["jitter"]["default"])
    config_dict["ADVANCED"]["sleep_at_night"] = str(
        SKELETON["ADVANCED"]["sleep_at_night"]["default"])
    config_dict["ADVANCED"]["user_agent"] = str(
        SKELETON["ADVANCED"]["user_agent"]["default"])


def start_config_generation(config_dict: dict = dict()):
    """ entry point for config generation """
    global run_gui
    if run_gui:
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

    def toggle_group_request(event):
        """ toggle input for group appointment search """
        if not search_group_appointments.get():
            birthday.grid_remove()
            birthday_label.grid_remove()
            group_size_label.grid(row=2, column=1)
            group_size.grid(row=3, column=1)
        else:
            birthday.grid(row=3, column=1)
            birthday_label.grid(row=2, column=1)
            group_size.grid_remove()
            group_size_label.grid_remove()

    def get_input():
        """ read config from form """
        if search_group_appointments.get():
            config_dict["COMMON"]["group_size"] = group_size.get()
        else:
            config_dict["COMMON"]["birthdate"] = birthday.get_date().strftime(
                "%d.%m.%Y")
        config_dict["COMMON"]["zip_code"] = plz.get()
        for item in NOTIFIERS:
            config_dict[item.upper()]["enable"] = str(
                enable[item].get()).lower()

    def create_subwindow(event):
        """ when selecting a notifier, show a new window with the required options """
        def close_subwindow():
            """ get values and close window """
            if validate_notifier_input():
                for field in FIELDS[notifier]:
                    config_dict[notifier.upper(
                    )][field] = input_arr[field].get()
                subwindow.destroy()
            else:
                open_alert_window(msg="Bitte alle Felder ausfüllen.")

        def validate_notifier_input():
            """ check for empty input """
            for item in input_arr:
                match = re.match(
                    NOTIFIER_REGEX[item], input_arr[item].get())
                if match is None:
                    return False
            return True

        notifier = event.widget.cget("text")
        if notifier != "WEBBROWSER" and not enable[notifier].get():
            enable[notifier].set(not enable[notifier].get())
            input_arr = {}
            subwindow = tk.Toplevel(tk_window)
            row_index = 0
            notifier_fields = FIELDS[notifier]
            for field in notifier_fields:
                tk.Label(subwindow, text=notifier_fields[field]).grid(
                    row=row_index, column=0)
                input_arr[field] = tk.Entry(subwindow)
                input_arr[field].grid(row=row_index, column=1)
                row_index += 1
            close = tk.Button(
                subwindow, text="Fenster schließen", command=close_subwindow)
            close.grid(row=row_index, column=1)
        return 0

    def open_alert_window(msg):
        """ create an alert window """
        def close_alert_window():
            alert_window.destroy()

        alert_window = tk.Toplevel(tk_window)
        tk.Label(alert_window, text=msg).grid(row=0, column=0)
        close_alert = tk.Button(alert_window, text="OK",
                                command=close_alert_window)
        close_alert.grid(row=1, column=0)

    def check_notifiers_enabled():
        """ check whether any notifier is enabled """
        for item in enable:
            if enable[item].get():
                return True
        return False

    def validate_input():
        """ validate user input """
        if search_group_appointments.get():
            entered_group_size = group_size.get()
            match_group_size = re.match(GROUP_SIZE_REGEX, entered_group_size)
            if match_group_size is None:
                return False
        entered_plz = plz.get()
        return bool(re.match(ZIP_REGEX, entered_plz))

    def close_window():
        """ close the window """
        if not check_notifiers_enabled():
            open_alert_window(
                msg="Bitte eine Art der Benachrichtigung auswählen!")
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
            advanced_settings_input[field].grid(
                row=settings_window_row_index, column=1)
            advanced_settings_input[field].insert(
                0, config_dict["ADVANCED"][field])
            settings_window_row_index += 1
        close_advanced = tk.Button(
            settings_window, text="Fenster schließen", command=close_settings_window)
        close_advanced.grid(row=settings_window_row_index, column=1)

    tk_window.geometry("400x400+250+100")

    row_index = 7
    checkboxes = {}
    enable = {}

    search_group_appointments = tk.BooleanVar()
    search_group_appointments.set(False)
    group_request = ttk.Checkbutton(
        tk_window,
        text="Gruppentermin",
        variable=search_group_appointments,
        onvalue=True
    )
    group_request.bind('<Button-1>', toggle_group_request)
    group_request.grid(row=1, column=1)

    birthday_label = tk.Label(tk_window, text="Geburtsdatum", font="bold")
    birthday_label.grid(row=2, column=1)
    tk.Label(tk_window, text="PLZ", font="bold").grid(row=4, column=1)

    group_size_label = tk.Label(tk_window, text="Gruppengröße", font="bold")
    group_size_label.grid_remove()

    birthday = DateEntry(tk_window, width=18)
    group_size = tk.Entry(tk_window)
    plz = tk.Entry(tk_window)

    birthday.grid(row=3, column=1)
    plz.grid(row=5, column=1)
    group_size.grid_remove()

    tk.Label(tk_window, text="Benachrichtigung",
             font="bold").grid(row=6, column=1)
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

    close = tk.Button(
        tk_window, text="Speichern und schließen", command=close_window)
    close.grid(row=row_index + 1, column=1)

    advanced = tk.Button(
        tk_window, text="Weitere Einstellungen", command=advanced_settings)
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
                match = re.match(
                    NOTIFIER_REGEX[field], notifier_input[field])
        return notifier_input

    birthday = ""
    plz = ""
    match = None
    config_for_group_input = ""
    while config_for_group_input.lower() not in ["j", "n"]:
        config_for_group_input = input(
            'Soll nach Gruppenterminen gesucht werden? (j/n): ')
    config_for_group = config_for_group_input.lower() == "j"
    while match is None and not config_for_group:
        birthday = input('Bitte den Geburtstag eingeben: ')
        match = re.match(BIRTHDATE_REGEX, birthday)
    match = None
    while match is None and config_for_group:
        group_size = input('Bitte die Gruppengröße eingeben: ')
        match = re.match(GROUP_SIZE_REGEX, group_size)
    while match is None or bool(re.match(ZIP_REGEX, plz)):
        plz = input('Bitte die PLZ eingeben: ')
        match = re.match(ZIP_REGEX, plz)

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

    if config_for_group:
        config_dict["COMMON"]["group_size"] = group_size
    else:
        config_dict["COMMON"]["birthday"] = birthday
    config_dict["COMMON"]["zip_cpde"] = plz
    config_dict["WEBBROWSER"]["enable"] = enable_browser

    return config_dict


if __name__ == "__main__":

    start_config_generation()
