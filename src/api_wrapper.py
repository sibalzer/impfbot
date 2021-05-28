import logging

from requests.sessions import Session
from requests.exceptions import ConnectTimeout
from common import sleep
import settings

log = logging.getLogger(__name__)


headers = {
    'Accept': 'application/json',
    'User-Agent': settings.USER_AGENT
}


def fetch_api(plz: int, birthdate_timestamp: int = None, max_retries: int = 10, sleep_after_error: int = 30, sleep_after_shadowban: int = 300, jitter: int = 15) -> any:
    url = f"https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{plz}"
    if birthdate_timestamp is not None:
        url += f"?stiko=&count=1&birthdate={int(birthdate_timestamp)*1000}"
    fail_counter = 0

    while True:
        try:
            session = Session()
            with session.get(url=url, headers=headers, timeout=10) as data:
                return data.json()["resultList"]
        except ConnectionError as _e:
            log.error(
                f"Couldn't fetch api: ConnectionError (No internet?) {_e}")
            sleep(10, 0)
        except Exception:
            if fail_counter > max_retries:
                log.error(
                    f"Couldn't fetch api. (Shadowbanned IP?) Sleeping for {sleep_after_shadowban/60}min")
                sleep(sleep_after_shadowban, 30)
                return None
            fail_counter += 1

            sleep_time = sleep_after_error*fail_counter

            sleep(sleep_time, jitter)
