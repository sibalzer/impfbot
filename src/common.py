
from datetime import datetime, timedelta, time as dt
import random
import sys
import time
import re

APPOINTMENT_URL = r"https://www.impfportal-niedersachsen.de/portal/#/appointment/public"

MAIL_REGEX = r"\b(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])\b"
ZIP_REGEX = r"(19|21|26|27|28|29|30|31|34|37|38|48|49)([0-9]{3})"
BIRTHDATE_REGEX = r"^[0-3]?[0-9]\.[0-3]?[0-9]\.(?:[0-9]{2})?[0-9]{2}$"
TIME_REGEX = r"[0-9]*(?:\.[0-9])?$"

BOOL_REGEX = r"(?i)(?:true)|(?:false)"

NOTIFIERS = ["EMAIL", "TELEGRAM", "WEBBROWSER"]
NOTIFIER_REGEX = {
    "sender": MAIL_REGEX,
    "password": r"\b[^ ]+\b",   # match anything not a space
    # match alphanumeric characters, dash, and dot
    "server": r"\b[\p{L}\p{N}\-\.]+\b",
    "port": r"\b\d{2,}\b",
    "receivers": r"\b" + MAIL_REGEX + r"(," + MAIL_REGEX + r")*\b",
    # I hope this covers all possible tokens
    "token": r"\b[a-zA-Z0-9\:\-]+\b",
    "chat_ids": r"\b\d{5,}(,\d{5,})*\b"  # matches a list of numbers
}


def datetime2timestamp(date: datetime):
    now = datetime.now()
    s_since_date = (now - date).total_seconds()
    return int(now.timestamp() - s_since_date)


def is_night() -> bool:
    morning = dt(hour=7, minute=0)
    evening = dt(hour=23, minute=0)
    now = datetime.now().time()
    return not (morning < now and now < evening)

GOOD_PLZ = ['19', '21', '26', '27', '28', '29', '30', '31', '34', '37', '38', '48', '49']

def sleep(time_in_s: int, jitter: int = 0) -> None:
    time_to_wait = time_in_s + random.random()*jitter
    start = datetime.now()
    end = datetime.now() + timedelta(seconds=time_to_wait)
    while end > datetime.now():
        elapsed_time_s: int = (datetime.now() - start).total_seconds()
        time_to_wait_s: int = time_to_wait

        time_str = f"\rSleeping ({elapsed_time_s}s/{time_to_wait_s}s)"
        sys.stdout.write(time_str)
        sys.stdout.flush()

        if elapsed_time_delta < 1:
            time.sleep(elapsed_time_delta)
        else:
            time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()


def sleep_until(hour, minute) -> None:
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        future += timedelta(days=1)
    sleep((future-t).total_seconds())
