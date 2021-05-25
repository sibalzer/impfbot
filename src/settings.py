import configparser
import datetime

config = configparser.ConfigParser()
config.read("config.ini")

ZIP = config["COMMON"]["postleitzahl"]
BIRTHDATE = datetime.datetime.strptime(
    config["COMMON"]["geburtstag"], r"%d.%m.%Y")

SEND_EMAIL = True if config["EMAIL"]["enable"].lower() == "true" else False

if SEND_EMAIL:
    SENDER = config["EMAIL"]["sender"]
    SERVER = config["EMAIL"]["server"]
    PASSWORD = config["EMAIL"]["password"]
    EMAIL_RECEIVERS = config["EMAIL"]["empfaenger"].split(',')

OPEN_BROWSER = True if config["WEBBROWSER"]["open_browser"].lower(
) == "true" else False

SLEEP_BETWEEN_REQUESTS_IN_S = int(
    config["ADVANCED"]["sleep_between_requests_in_s"])
SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = int(
    config["ADVANCED"]["sleep_between_failed_requests_in_s"])
SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = int(
    config["ADVANCED"]["sleep_after_ipban_in_min"])*60
JITTER = int(
    config["ADVANCED"]["jitter"])
SLEEP_AT_NIGHT = True if config["ADVANCED"]["sleep_at_night"].lower(
) == "true" else False
USER_AGENT = config["ADVANCED"]["user_agent"]
