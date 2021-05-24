import configparser
import datetime

config = configparser.ConfigParser()
config.read("config.ini")

ZIP = config["COMMON"]["postleitzahl"]
BIRTHDATE = datetime.datetime.strptime(
    config["COMMON"]["geburtstag"], r"%d.%m.%Y")

SLEEP_BETWEEN_REQUESTS_IN_S = int(
    config["ADVANCED"]["sleep_between_requests_in_s"])
SLEEP_BETWEEN_FAILED_REQUESTS_IN_S = int(
    config["ADVANCED"]["sleep_between_failed_requests_in_s"])
SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN = int(
    config["ADVANCED"]["sleep_after_ipban_in_min"])

JITTER = int(
    config["ADVANCED"]["jitter"])

SEND_EMAIL = config["EMAIL"]["enable"]

if SEND_EMAIL:
    SENDER = config["EMAIL"]["sender"]
    SERVER = config["EMAIL"]["server"]
    PASSWORD = config["EMAIL"]["password"]
    EMAIL_RECEIVERS = config["EMAIL"]["empfaenger"].split(',')

OPEN_BROWSER = config["WEBBROWSER"]["open_browser"]
