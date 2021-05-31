from logging import FATAL
from unittest import mock
from freezegun import freeze_time
from datetime import datetime
import time
import common


@freeze_time("2012-01-14 03:21:34")
def test_is_night_night():
    assert common.is_night()


@freeze_time("2012-01-14 14:21:34")
def test_is_night_day():
    assert not common.is_night()


@freeze_time("2012-01-14 13:59:10", tick=True)
def test_sleep():
    start = time.time()
    common.sleep(2)
    end = time.time()
    delta = (end - start)
    assert 1.9 < delta < 2.1


@freeze_time("2012-01-14 13:59:58", tick=True)
def test_sleep_until():
    common.sleep_until(14, 0)
    end = time.gmtime()
    assert end.tm_hour == 14
    assert end.tm_min == 0
    assert end.tm_sec == 0
