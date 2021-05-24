import random
from datetime import datetime, timedelta
import time
import sys


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
