import configparser
import datetime
import logging
import sys
import os

from common import GOOD_PLZ
from config_generator import start_config_generation

log = logging.getLogger(__name__)

class ParseExeption(BaseException):
    pass


def load(path: str):
    config = configparser.ConfigParser()
    dataset = config.read(path)
    if not dataset:
        raise FileNotFoundError(f"Could not find config file. Exit...")

    try:
        global ZIP
        ZIP = config["COMMON"]["postleitzahl"]
        if len(ZIP) != 5:
            raise Exception('Non 5 digit ZIP-Code')
        if ZIP[0:2] not in GOOD_PLZ:
            ParseExeption(
                "[EMAIL] Are you sure that you are living in lower saxony? Because your ZIP-Code seem suspicious...")
    except KeyError as e:
        raise ParseExeption(
            f"[COMMON] '{e}' is missing in config. Cant run without Zip-Code.")
    except Exception as e:
        raise ParseExeption(f"[COMMON] Invalid ZIP-Code: {e}")

    try:
        global BIRTHDATE
        BIRTHDATE = datetime.datetime.strptime(
            config["COMMON"]["geburtstag"], r"%d.%m.%Y")
    except KeyError as e:
        raise ParseExeption(
            f"[COMMON] '{e}' is missing in config. Cant run without birthdate. Exit.")
    except Exception as e:
        raise ParseExeption(f"[COMMON] Invalid birthdate: {e}")

    try:
        global SEND_EMAIL
        SEND_EMAIL = True if config["EMAIL"]["enable"].lower(
        ) == "true" else False
    except KeyError:
        log.warning(
            "[EMAIL] 'enable' is missing in config. Set to False")
        SEND_EMAIL = False

    try:
        global SENDER, SERVER, PASSWORD, EMAIL_RECEIVERS, PORT
        if SEND_EMAIL:
            SENDER = config["EMAIL"]["sender"]
            SERVER = config["EMAIL"]["server"]
            PASSWORD = config["EMAIL"]["password"]
            EMAIL_RECEIVERS = config["EMAIL"]["empfaenger"].split(',')
            PORT = config["EMAIL"]["port"]
    except KeyError as e:
        log.warning(
            f"[EMAIL] '{e}' is missing in config. Set Send Email to False")
        SEND_EMAIL = False

    try:
        global SEND_TELEGRAM_MSG
		SEND_TELEGRAM_MSG = config["TELEGRAM"]["enable"].lower() == "true"
    except KeyError:
        log.warning("[TELEGRAM] 'enable' is missing in config. Set to False")
        SEND_TELEGRAM_MSG = False

    try:
        if SEND_TELEGRAM_MSG:
            global TOKEN, CHAT_IDS
            TOKEN = config["TELEGRAM"]["token"]
            CHAT_IDS = config["TELEGRAM"]["chat_id"].split(',')
    except KeyError as e:
        log.warning(
            f"[TELEGRAM] '{e}' is missing in config. Set Telegram to False")
        SEND_EMAIL = False

    try:
        global OPEN_BROWSER
		OPEN_BROWSER = config["WEBBROWSER"]["enable"].lower() == "true"
    except KeyError:
        log.warning(
            "'enable' is missing in config. Set to False")
        OPEN_BROWSER = False

    try:
        global SLEEP_BETWEEN_REQUESTS_IN_S
        SLEEP_BETWEEN_REQUESTS_IN_S = int(
            config["ADVANCED"]["sleep_between_requests_in_s"])
    except KeyError:
        log.warning(
            "'sleep_between_requests_in_s' is missing in config. Set to 5min")
        SLEEP_BETWEEN_REQUESTS_IN_S = 300
    except ValueError:
        log.warning(
            "'sleep_between_requests_in_s' is not a number. Set to 5min")
        SLEEP_BETWEEN_REQUESTS_IN_S = 300

    try:
        global SLEEP_BETWEEN_FAILED_REQUESTS_IN_S
        SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = int(
            config["ADVANCED"]["sleep_between_failed_requests_in_s"])
    except KeyError:
        log.warning(
            "'sleep_between_failed_requests_in_s' is missing in config. Set to 30s")
        SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = 30
    except ValueError:
        log.warning(
            "'sleep_between_failed_requests_in_s' is not a number. Set to 30s")
        SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = 300

    try:
        global SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN
        SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = float(
            config["ADVANCED"]["sleep_after_ipban_in_min"])*60
    except KeyError:
        log.warning(
            "'sleep_after_ipban_in_min' is missing in config. Set to 3h")
        SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = 60*180
    except ValueError:
        log.warning(
            "'sleep_after_ipban_in_min' is not a number. Set to 3h")
        SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = 300

    try:
        global COOLDOWN_AFTER_FOUND_IN_MIN
        COOLDOWN_AFTER_FOUND_IN_MIN = float(
            config["ADVANCED"]["cooldown_after_found_in_min"])*60
    except KeyError:
        log.warning(
            "'cooldown_after_found_in_min' is missing in config. Set to 15min")
        COOLDOWN_AFTER_FOUND_IN_MIN = 60*15
    except ValueError:
        log.warning(
            "'cooldown_after_found_in_min' is not a number. Set to 15min")
        COOLDOWN_AFTER_FOUND_IN_MIN = 300

    try:
        global JITTER
        JITTER = int(
            config["ADVANCED"]["jitter"])
    except KeyError:
        log.warning("'jitter' is missing in config. Set to 15s")
        JITTER = 15
    except ValueError:
        log.warning(
            "'jitter' is not a number. Set to 15s")
        JITTER = 300

    try:
        global SLEEP_AT_NIGHT
        SLEEP_AT_NIGHT = True if config["ADVANCED"]["sleep_at_night"].lower(
        ) == "true" else False
    except KeyError:
        log.warning(
            "'sleep_at_night' is missing in config. Set to True")
        SLEEP_AT_NIGHT = True

    try:
        global USER_AGENT
        USER_AGENT = config["ADVANCED"]["user_agent"]
    except KeyError:
        log.warning(
            "'user_agent' is missing in config. Set to 'impfbot'")
        USER_AGENT = 'impfbot'
