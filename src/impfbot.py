"""Notification bot for the lower saxony vaccination portal"""
import argparse
from datetime import datetime, timezone, timedelta
import sys

from alerts import alert
from api_wrapper import fetch_api, ShadowBanException, RequestConnectionError
from common import sleep, sleep_until, is_night, datetime2timestamp, YES, NO
from config_generator import start_config_generation
from log import log
from settings import load, settings, ParseExeption


def check_for_slot() -> None:
    """checks if a slot is available"""
    try:
        if hasattr(settings, "COMMON_BIRTHDATE"):
            birthdate_timestamp = datetime2timestamp(settings.COMMON_BIRTHDATE)
            result = fetch_api(
                zip_code=settings.COMMON_ZIP_CODE,
                birthdate_timestamp=birthdate_timestamp,
                with_vector=settings.COMMON_WITH_VECTOR,
                max_retries=10,
                sleep_after_error=settings.COOLDOWN_BETWEEN_FAILED_REQUESTS,
                user_agent=settings.USER_AGENT,
                jitter=settings.JITTER
            )
        else:
            result = fetch_api(
                zip_code=settings.COMMON_ZIP_CODE,
                group_size=settings.COMMON_GROUP_SIZE,
                with_vector=settings.COMMON_WITH_VECTOR,
                max_retries=10,
                sleep_after_error=settings.COOLDOWN_BETWEEN_FAILED_REQUESTS,
                user_agent=settings.USER_AGENT,
                jitter=settings.JITTER
            )
        if result == []:
            log.error("Result is emtpy. (Invalid ZIP Code (PLZ)?)")
        for elem in result:
            if not elem['outOfStock']:
                local_timezone = timezone(timedelta(hours=2))

                free_slots = elem['freeSlotSizeOnline']
                vaccine_name = elem['vaccineName']
                vaccine_type = elem['vaccineType']
                first_appoinment_date = datetime.fromtimestamp(
                    elem['firstAppoinmentDateSorterOnline'] /
                    1000, local_timezone
                ).strftime("%d.%m.%Y")

                log.info(
                    f"Free slot! ({free_slots}) {vaccine_name}/{vaccine_type} Appointment date: {first_appoinment_date}")
                msg = f"[{settings.CUSTOM_MESSAGE_PREFIX}] Freier Impfslot ({free_slots})! {vaccine_name}/{vaccine_type} verfügbar ab dem {first_appoinment_date}"

                alert(msg)
                sleep(settings.COOLDOWN_AFTER_SUCCESS)
            else:
                log.info("No free slot.")
                sleep(settings.COOLDOWN_BETWEEN_REQUESTS, settings.JITTER)

    except RequestConnectionError as ex:
        log.error(
            f"Couldn't fetch api: ConnectionError (No internet?) {ex}")
        sleep(10)

    except ShadowBanException:
        sleep_after_shadowban_min = settings.COOLDOWN_AFTER_IP_BAN/60
        log.error(
            f"Couldn't fetch api. (Shadowbanned IP?) "
            f"Sleeping for {sleep_after_shadowban_min}min")
        sleep(settings.COOLDOWN_AFTER_IP_BAN)

    except Exception as ex:
        log.error(f"Something went wrong ({ex})")
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
        except FileNotFoundError:
            while True:
                log.error("config file not found")
                print("Do you want to use the interface to generate a config? yes/no")
                result = input().lower()
                if result in YES:
                    log.info("Starting config generator")
                    start_config_generation()
                    break
                elif result in NO:
                    sys.exit(1)
                else:
                    print("Invalid input")

        except ParseExeption as ex:
            log.error(ex)
            print("Press [enter] to close.")
            input()
            sys.exit(1)
        except Exception as ex:
            log.warning(ex)

        print(settings)

        while True:
            if is_night() and settings.SLEEP_AT_NIGHT:
                log.info("It's night. Sleeping until 7am")
                sleep_until(hour=7, minute=0)

            check_for_slot()

    except (KeyboardInterrupt, SystemExit):
        print("Bye...")
