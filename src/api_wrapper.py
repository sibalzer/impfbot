import logging

from requests.sessions import Session
from common import sleep
import settings

log = logging.getLogger(__name__)


headers = {
    'Accept': 'application/json',
    'User-Agent': settings.USER_AGENT
}


def fetch_api(
        plz: int,
        birthdate_timestamp: int = None,
        group_size: int = None,
        max_retries: int = 10,
        sleep_after_error: int = 30,
        sleep_after_shadowban: int = 300
    ) -> any:
    url = f"https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{plz}?stiko="
    if birthdate_timestamp:
        url += f"&count=1&birthdate={int(birthdate_timestamp)*1000}"
    elif group_size:
        url += f"&count={group_size}"
    fail_counter = 0

    while True:
        try:
            session = Session()
            with session.get(url=url, headers=headers, timeout=10) as data:
                return data.json()["resultList"]
        except Exception:
            if fail_counter > max_retries:
                log.error(
                    f"Couldn't fetch api. (Shadowbanned IP?) Sleeping for {sleep_after_shadowban}min")
                sleep(sleep_after_shadowban, 30)
                return None
            fail_counter += 1

            sleep_time = sleep_after_error*fail_counter

            sleep(sleep_time, 15)
