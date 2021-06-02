
"""api wrapper for the lower saxony vaccination portal"""
import logging

from requests.sessions import Session
from requests.exceptions import ConnectionError
from common import sleep

log = logging.getLogger(__name__)


class ShadowBanException(Exception):
    """Exception for ip ban detection"""
    pass


def fetch_api(plz: int,
              birthdate_timestamp: int = None,
              max_retries: int = 10,
              sleep_after_error: int = 30,
              jitter: int = 10,
              user_agent: str = 'python') -> any:
    """fetches the api with ip ban avoidance"""
    url = f"https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{plz}"
    headers = {
        'Accept': 'application/json',
        'User-Agent': user_agent
    }
    if birthdate_timestamp is not None:
        url += f"?stiko=&count=1&birthdate={int(birthdate_timestamp)*1000}"

    for fail_counter in range(0, max_retries+1):
        try:
            session = Session()
            with session.get(url=url, headers=headers, timeout=10) as data:
                return data.json()["resultList"]
        except ConnectionError as _e:
            raise _e
        except Exception as e:
            sleep_time = sleep_after_error*fail_counter
            sleep(sleep_time, jitter)
    raise ShadowBanException
