"""Notification bot for the lower saxony vaccination portal"""
import argparse
import sys

from alerts import alert
from api_wrapper import fetch_api, ShadowBanException, ConnectionError
from common import sleep, sleep_until, is_night, datetime2timestamp
from log import log
from settings import load, settings


from common import sleep, sleep_until, is_night, datetime2timestamp


def check_for_slot() -> None:
    """checks if a slot is available"""
    try:
        birthdate_timestamp = datetime2timestamp(settings.COMMON_BIRTHDATE)
        result = fetch_api(
            plz=settings.COMMON_ZIP_CODE,
            birthdate_timestamp=birthdate_timestamp,
            max_retries=10,
            sleep_after_error=settings.COOLDOWN_BETWEEN_FAILED_REQUESTS,
            user_agent=settings.USER_AGENT,
            jitter=settings.JITTER
        )
        if result == []:
            log.error("Result is emtpy. (Invalid ZIP Code (PLZ)?)")
        for elem in result:
            if not elem['outOfStock']:
                free_slots = elem['freeSlotSizeOnline']
                vaccine_name = elem['vaccineName']
                vaccine_type = elem['vaccineType']

                log.info(
                    f"Free slot! ({free_slots}) {vaccine_name}/{vaccine_type}")
                msg = f"Freier Impfslot ({free_slots})! {vaccine_name}/{vaccine_type}"

                alert(msg)
                sleep(settings.COOLDOWN_AFTER_SUCCESS)
            else:
                log.info("No free slot.")
                sleep(settings.COOLDOWN_BETWEEN_REQUESTS, settings.JITTER)

    except ConnectionError as _e:
        log.error(
            f"Couldn't fetch api: ConnectionError (No internet?) {_e}")
        sleep(10)

    except ShadowBanException as _e:
        sleep_after_shadowban_min = settings.COOLDOWN_AFTER_IP_BAN/60
        log.error(
            f"Couldn't fetch api. (Shadowbanned IP?) "
            f"Sleeping for {sleep_after_shadowban_min}min")
        sleep(settings.COOLDOWN_AFTER_IP_BAN)

    except Exception as _e:
        log.error(f"Something went wrong ({_e})")
        sleep(settings.COOLDOWN_BETWEEN_REQUESTS, settings.JITTER)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description='Notification bot for the lower saxony vaccination portal')
        parser.add_argument('-f', '-c', '--config',
                            dest='configfile',
                            help='Path to config.ini file',
                            required=False,
                            default='config.ini')
        arg = vars(parser.parse_args())

        try:
            load(arg['configfile'])
        except (settings.ParseExeption, FileNotFoundError) as e:
            log.error(e)
            print(f"Press [enter] to close.")
            input()
            sys.exit(1)
        except Exception as _e:
            log.warning(_e)

        print(settings)

        while True:
            if is_night() and settings.SLEEP_AT_NIGHT:
                log.info("It's night. Sleeping until 7am")
                sleep_until(hour=7, minute=0)

            check_for_slot()

    except (KeyboardInterrupt, SystemExit):
        print("Bye...")
