import configparser
import datetime
import logging
import sys
import os

from common import GOOD_PLZ
from config_generator import start_config_generation

log = logging.getLogger(__name__)

config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    config.read("config.ini")
else:
    start_config_generation(config)

try:
    ZIP = config["COMMON"]["postleitzahl"]
    if len(ZIP) != 5:
        raise Exception('Non 5 digit ZIP-Code')
    if ZIP[0:2] not in GOOD_PLZ:
        log.warning(
            "[EMAIL] Are you sure that you are living in lower saxony? Because your ZIP-Code seem suspicious...")
except KeyError as e:
    log.warning(
        f"[COMMON] '{e}' is missing in Config. Cant run without Zip-Code. Exit.")
    sys.exit(1)
except Exception as e:
    log.warning(f"[COMMON] Invalid ZIP-Code: {e}")

try:
    BIRTHDATE = datetime.datetime.strptime(
        config["COMMON"]["geburtstag"], r"%d.%m.%Y")
except KeyError as e:
    log.warning(
        f"[COMMON] '{e}' is missing in Config. Cant run without birthdate. Exit.")
    sys.exit(1)
except Exception as e:
    log.warning(f"[COMMON] Invalid birthdate: {e}")

try:
    SEND_EMAIL = True if config["EMAIL"]["enable"].lower() == "true" else False
except KeyError:
    log.warning(
        "[EMAIL] 'enable' is missing in Config. Set False")
    SEND_EMAIL = False

try:
    if SEND_EMAIL:
        SENDER = config["EMAIL"]["sender"]
        SERVER = config["EMAIL"]["server"]
        PASSWORD = config["EMAIL"]["password"]
        EMAIL_RECEIVERS = config["EMAIL"]["empfaenger"].split(',')
        PORT = config["EMAIL"]["port"]
except KeyError as e:
    log.warning(f"[EMAIL] '{e}' is missing in Config. Set Email to False")
    SEND_EMAIL = False

try:
    SEND_TELEGRAM_MSG = config["TELEGRAM"]["enable"].lower() == "true"
except KeyError:
    log.warning("[TELEGRAM] 'enable' is missing in Config. Set False")
    SEND_TELEGRAM_MSG = False

try:
    if SEND_TELEGRAM_MSG:
        TOKEN = config["TELEGRAM"]["token"]
        CHAT_IDS = config["TELEGRAM"]["chat_id"].split(',')
except KeyError as e:
    log.warning(
        f"[TELEGRAM] '{e}' is missing in Config. Set Telegram to False")
    SEND_EMAIL = False

try:
    OPEN_BROWSER = config["WEBBROWSER"]["enable"].lower() == "true"
except KeyError:
    log.warning("[WEBBROWSER] 'enable' is missing in Config. Set False")
    OPEN_BROWSER = False

try:
    SLEEP_BETWEEN_REQUESTS_IN_S = int(
        config["ADVANCED"]["sleep_between_requests_in_s"])
except KeyError:
    log.warning(
        "'sleep_between_requests_in_s' is missing in Config. Set 5min")
    SLEEP_BETWEEN_REQUESTS_IN_S = 300

try:
    SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = int(
        config["ADVANCED"]["sleep_between_failed_requests_in_s"])
except KeyError:
    log.warning(
        "'sleep_between_failed_requests_in_s' is missing in Config. Set 30s")
    SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = 30

try:
    SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = int(
        config["ADVANCED"]["sleep_after_ipban_in_min"])*60
except KeyError:
    log.warning("'sleep_after_ipban_in_min' is missing in Config. Set 3h")
    SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = 60*180
try:
    COOLDOWN_AFTER_FOUND_IN_MIN = int(
        config["ADVANCED"]["cooldown_after_found_in_min"])*60
except KeyError:
    log.warning("'cooldown_after_found_in_min' is missing in Config. Set 15min")
    COOLDOWN_AFTER_FOUND_IN_MIN = 60*15

try:
    JITTER = int(
        config["ADVANCED"]["jitter"])
except KeyError:
    log.warning("'jitter' is missing in Config. Set 15")
    JITTER = 15

try:
    SLEEP_AT_NIGHT = True if config["ADVANCED"]["sleep_at_night"].lower(
    ) == "true" else False
except KeyError:
    log.warning("'sleep_at_night' is missing in Config. Set True")
    SLEEP_AT_NIGHT = True

try:
    USER_AGENT = config["ADVANCED"]["user_agent"]
except KeyError:
    log.warning("'user_agent' is missing in config. set impfbot")
    USER_AGENT = 'impfbot'
