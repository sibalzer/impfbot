import configparser
import datetime
import logging

log = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("config.ini")

try:
    ZIP = config["COMMON"]["postleitzahl"]
    BIRTHDATE = datetime.datetime.strptime(
        config["COMMON"]["geburtstag"], r"%d.%m.%Y")
except KeyError as e:
    log.warning(
        f"[COMMON] '{e}' is missing in Config. Set Email to False")
    SEND_EMAIL = False

try:
    SEND_EMAIL = True if config["EMAIL"]["enable"].lower() == "true" else False
except KeyError as e:
    log.warning(
        f"[EMAIL] 'enable' is missing in Config. Set False")
    SEND_EMAIL = False

try:
    if SEND_EMAIL:
        SENDER = config["EMAIL"]["sender"]
        SERVER = config["EMAIL"]["server"]
        PASSWORD = config["EMAIL"]["password"]
        EMAIL_RECEIVERS = config["EMAIL"]["empfaenger"].split(',')
        PORT = config["EMAIL"]["port"]
except KeyError as e:
    log.warning(
        f"[EMAIL] '{e}' is missing in Config. Set Email to False")
    SEND_EMAIL = False


try:
    OPEN_BROWSER = True if config["WEBBROWSER"]["open_browser"].lower(
    ) == "true" else False
except KeyError as e:
    log.warning(
        f"'open_browser' is missing in Config. Set False")
    OPEN_BROWSER = False

try:
    SLEEP_BETWEEN_REQUESTS_IN_S = int(
        config["ADVANCED"]["sleep_between_requests_in_s"])
except KeyError as e:
    log.warning(
        f"'sleep_between_requests_in_s' is missing in Config. Set 5min")
    SLEEP_BETWEEN_REQUESTS_IN_S = 300

try:
    SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = int(
        config["ADVANCED"]["sleep_between_failed_requests_in_s"])
except KeyError as e:
    log.warning(
        f"'sleep_between_failed_requests_in_s' is missing in Config. Set 30s")
    SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = 30

try:
    SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = int(
        config["ADVANCED"]["sleep_after_ipban_in_min"])*60
except KeyError as e:
    log.warning(f"'sleep_after_ipban_in_min' is missing in Config. Set 3h")
    SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = 60*180

try:
    JITTER = int(
        config["ADVANCED"]["jitter"])
except KeyError as e:
    log.warning(f"'jitter' is missing in Config. Set 15")
    JITTER = 15

try:
    SLEEP_AT_NIGHT = True if config["ADVANCED"]["sleep_at_night"].lower(
    ) == "true" else False
except KeyError as e:
    log.warning(f"'sleep_at_night' is missing in Config. Set True")
    SLEEP_AT_NIGHT = True

try:
    USER_AGENT = config["ADVANCED"]["user_agent"]
except KeyError as e:
    log.warning(f"'user_agent' is missing in config. set impfbot")
    USER_AGENT = 'impfbot'
