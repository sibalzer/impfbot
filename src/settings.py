import configparser
import datetime
import logging
import sys

log = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("config.ini")

try:
    ZIP = config["COMMON"]["postleitzahl"]
    if len(ZIP) != 5:
        raise Exception('Non 5 digit ZIP-Code')
    if ZIP[0:2] not in ['19', '21', '26', '27', '28', '29', '30', '31', '34', '37', '38', '48', '49']:
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
    SEND_TELEGRAM_MSG = True if config["TELEGRAM"]["enable_telegram"].lower(
    ) == "true" else False
except KeyError:
    log.warning("[TELEGRAM] 'enable_telegram' is missing in Config. Set False")
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
    SEND_XMPP_MSG = True if config["XMPP"]["enable_xmpp"].lower(
    ) == "true" else False
except KeyError:
    log.warning("[XMPP] 'enable_xmpp' is missing in Config. Set False")
    SEND_XMPP_MSG = False

try:
    if SEND_XMPP_MSG:
        XMPPNAME = config["XMPP"]["user"]
        XMPPPASSW = config["XMPP"]["password"]
        XMPPSERVER = config["XMPP"]["server"]
        XMPPRECV = config["XMPP"]["receivers"].split(',')
except KeyError as e:
    log.warning(
        f"[XMPP] '{e}' is missing in Config. Set XMPP to False")
    SEND_XMPP_MSG = False

try:
    OPEN_BROWSER = True if config["WEBBROWSER"]["open_browser"].lower(
    ) == "true" else False
except KeyError:
    log.warning("'open_browser' is missing in Config. Set False")
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
