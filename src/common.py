import random
from datetime import datetime, timedelta, time as dt
import time
import sys

GOOD_PLZ = ['19', '21', '26', '27', '28', '29', '30', '31', '34', '37', '38', '48', '49']

def sleep(time_in_s: int, jitter: int = 0) -> None:
    time_to_wait = time_in_s + random.random()*jitter
    start = datetime.now()
    end = datetime.now() + timedelta(seconds=time_to_wait)
    while end > datetime.now():
        elapsed_time = datetime.now() - start
        time_str = f"\rSleeping ({int(elapsed_time.total_seconds())}s/{int(time_to_wait)}s)"
        sys.stdout.write(time_str)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()


def is_night() -> bool:
    morning = dt(hour=7, minute=0)
    evening = dt(hour=23, minute=0)
    now = datetime.now().time()
    return not (morning < now and now < evening)


def sleep_until(hour, minute) -> None:
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        future += timedelta(days=1)
    sleep((future-t).total_seconds())
