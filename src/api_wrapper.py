import logging

from requests.sessions import Session
from common import sleep

log = logging.getLogger(__name__)


headers = {
    'Accept': 'application/json',
    'User-Agent': 'vacBot'
}


def fetch_api(plz: int, birthdate_timestamp: int = None, max_retries: int = 10, sleep_after_error: int = 30, sleep_after_shadowban: int = 300) -> any:
    url = f"https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{plz}"
    if birthdate_timestamp != None:
        url += f"?stiko=&count=1&birthdate={int(birthdate_timestamp)*1000}"
    fail_counter = 0

    while True:
        try:
            session = Session()
            with session.get(url=url, headers=headers, timeout=10) as data:
                return data.json()["resultList"]
        except Exception as e:
            if fail_counter > max_retries:
                log.error(
                    f"Couldn't fetch api. (Shadowbanned IP?) Sleeping for {sleep_after_shadowban}min")
                sleep(sleep_after_shadowban, 30)
                return None
            fail_counter += 1

            sleep_time = sleep_after_error*fail_counter

            sleep(sleep_time, 15)
