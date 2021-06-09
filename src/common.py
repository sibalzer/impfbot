"""common methods and constants"""
from datetime import datetime, timedelta, time as dt
import random
import sys
import time

APPOINTMENT_URL = r"https://www.impfportal-niedersachsen.de/portal/#/appointment/public"

ZIP_REGEX = r"^(19|21|26|27|28|29|30|31|34|37|38|48|49)([0-9]{3})$"
BIRTHDATE_REGEX = r"^[0-3]?[0-9]\.[0-3]?[0-9]\.(?:[0-9]{2})?[0-9]{2}$"
NUMBER_REGEX = r"^[0-9]*(?:\.[0-9])?$"
BOOL_REGEX = r"(?i)^(?:true)|(?:false)$"
USER_AGENT_REGEX = r"^[^ ]*$"


MAIL_REGEX = r"\b(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])\b"
NOTIFIERS = ["EMAIL", "TELEGRAM", "WEBBROWSER", "APPRISE"]
NOTIFIER_REGEX = {
    "sender": MAIL_REGEX,
    "user": r"^[^ ]*$",   # match anything execpt space
    "password": r"^[^ ]*$",   # match anything execpt space
    # match alphanumeric characters, dash, and dot
    "server": r"^[a-zA-Z0-9-\.]+$",
    "port": r"^\d{2,}$",
    "receivers": r"^" + MAIL_REGEX + r"(," + MAIL_REGEX + r")*$",
    # I hope this covers all possible tokens
    "token": r"^[0-9]+:[a-zA-Z0-9\-_]+$",
    "chat_ids": r"^\-?\d{5,}(,\-?\d{5,})*$",  # matches a list of numbers with possible leading dash
    "service_uris": r"^[^ ]+$",   # match anything not a space
}


YES = ["yes", "y", "ja", "j"]
NO = ["no", "n", "nein"]


def datetime2timestamp(date: datetime) -> int:
    """transforms a datetime in a timestamp (datetime.datetime.timestamp() fails pre epoch)"""
    now = datetime.now()
    s_since_date = (now - date).total_seconds()
    return int(now.timestamp() - s_since_date)


def is_night() -> bool:
    """test if it is night"""
    morning = dt(hour=7, minute=0)
    evening = dt(hour=23, minute=0)
    now = datetime.now().time()
    return not (morning < now < evening)


GOOD_PLZ = ['19', '21', '26', '27', '28', '29',
            '30', '31', '34', '37', '38', '48', '49']


def sleep(time_in_s: int, jitter: int = 0) -> None:
    """sleeps for time and random jitter; prints output"""
    time_to_wait = time_in_s + random.random()*jitter
    start = datetime.now()
    end = datetime.now() + timedelta(seconds=time_to_wait)
    while end > datetime.now():
        elapsed_time_s = (datetime.now() - start).total_seconds()
        time_to_wait_s = time_to_wait
        elapsed_time_delta = time_to_wait_s - elapsed_time_s

        time_str = f"\rSleeping ({int(elapsed_time_s)}s/{int(time_to_wait_s)}s)"
        sys.stdout.write(time_str)
        sys.stdout.flush()

        if elapsed_time_delta < 1:
            time.sleep(elapsed_time_delta)
        else:
            time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()


def sleep_until(hour, minute) -> None:
    """sleep until certain time"""
    today = datetime.today()
    future = datetime(today.year, today.month, today.day, hour, minute)
    if today.timestamp() > future.timestamp():
        future += timedelta(days=1)
    sleep((future-today).total_seconds())
