from datetime import datetime
from log import log
import settings
import api_wrapper
import alerts

from common import sleep, sleep_until, is_night


def check_for_slot() -> None:
    try:
        result = api_wrapper.fetch_api(
            plz=settings.ZIP,
            birthdate_timestamp=int(
                datetime.now().timestamp() -
                (datetime.now() - settings.BIRTHDATE).total_seconds()),
            max_retries=10,
            sleep_after_error=settings.SLEEP_BETWEEN_FAILED_REQUESTS_IN_S,
            sleep_after_shadowban=settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN,
            user_agent=settings.USER_AGENT,
            jitter=settings.JITTER
        )
        if not result:
            log.error("Result is emtpy. (Invalid ZIP Code (PLZ))")
        for elem in result:
            if not elem['outOfStock']:
                log.info(
                    f"Free slot! ({elem['freeSlotSizeOnline']}) {elem['vaccineName']}/{elem['vaccineType']}")

                msg = f"Freier Impfslot ({elem['freeSlotSizeOnline']})! {elem['vaccineName']}/{elem['vaccineType']}"
                alerts.alert(msg)

                sleep(settings.COOLDOWN_AFTER_FOUND_IN_MIN, 0)
            else:
                log.info("No free slot.")
    except Exception as e:
        log.error(f"Something went wrong ({e})")


if __name__ == "__main__":
    try:
        while True:
            if is_night() and settings.SLEEP_AT_NIGHT:
                log.info("It's night. Sleeping until 7am")
                sleep_until(hour=7, minute=0)

            check_for_slot()
            sleep(settings.SLEEP_BETWEEN_REQUESTS_IN_S, settings.JITTER)

    except (KeyboardInterrupt, SystemExit):
        print("Bye...")
