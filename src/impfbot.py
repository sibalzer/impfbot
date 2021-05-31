import argparse
from datetime import datetime
import sys

from alerts import alert
from api_wrapper import fetch_api, ShadowBanException
from common import sleep, sleep_until, is_night
from log import log
import settings


def check_for_slot() -> None:
    try:
        result = fetch_api(
            plz=settings.ZIP,
            birthdate_timestamp=int(
                datetime.now().timestamp() -
                (datetime.now() - settings.BIRTHDATE).total_seconds()),
            max_retries=10,
            sleep_after_error=settings.SLEEP_BETWEEN_FAILED_REQUESTS_IN_S,
            user_agent=settings.USER_AGENT
            jitter=settings.JITTER
        )
        if result == []:
            log.error("Result is emtpy. (Invalid ZIP Code (PLZ)?)")
        for elem in result:
            if not elem['outOfStock']:
                log.info(
                    f"Free slot! ({elem['freeSlotSizeOnline']}) {elem['vaccineName']}/{elem['vaccineType']}")

                msg = f"Freier Impfslot ({elem['freeSlotSizeOnline']})! {elem['vaccineName']}/{elem['vaccineType']}"

                alert(msg)

                sleep(settings.COOLDOWN_AFTER_FOUND_IN_MIN)
            else:
                log.info("No free slot.")
                sleep(settings.SLEEP_BETWEEN_REQUESTS_IN_S, settings.JITTER)

    except ShadowBanException as e:
        sleep_after_shadowban = settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN
        log.error(
            f"Couldn't fetch api. (Shadowbanned IP?) Sleeping for {settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN/60}min")
        sleep(settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN)

    except Exception as e:
        log.error(f"Something went wrong ({e})")
        sleep(settings.SLEEP_BETWEEN_REQUESTS_IN_S, settings.JITTER)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description='Notification bot for the lower saxony vaccination portal ')
        parser.add_argument('-f', '-c', '--config', dest='configfile',
                            help='Path to config.ini file', required=False, default='config.ini')
        arg = vars(parser.parse_args())

        try:
            settings.load(arg['configfile'])
        except (settings.ParseExeption, FileNotFoundError) as e:
            log.error(e)
            print(f"Press [enter] to close.")
            input()
            sys.exit(1)
        except Exception as e:
            log.warning(e)

        while True:
            if is_night() and settings.SLEEP_AT_NIGHT:
                log.info("It's night. Sleeping until 7am")
                sleep_until(hour=7, minute=0)

            check_for_slot()

    except (KeyboardInterrupt, SystemExit):
        print("Bye...")
