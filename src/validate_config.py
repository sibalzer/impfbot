import argparse
from log import log
import settings
from alerts import alert


parser = argparse.ArgumentParser()
parser.add_argument('-f', '-c', '--config', dest='configfile',
                    help='Path to config.ini file', required=False, default='config.ini')
parser.add_argument('-a', '--alert', default=False, action='store_true',
                    help='validate alert with a test message. Default=False')
arg = vars(parser.parse_args())

log.info(f"validate config.ini")

settings.load(arg['configfile'])

log.info(f"settings validation finished")

result = None
if arg['alert']:
    result = "yes"
else:
    print("Do you want to send a test message? yes/no")
    result = input()
while True:
    if result in ["yes", "y", "ja", "j"]:
        alert("Test", verbose=True)
        log.info(f"Finished: Sending test massages")
        break
    elif result in ["no", "n", "nein"]:
        break
    else:
        print("Invalid input")
        print("Do you want to send a test message? yes/no")
        result = input()

if not arg['alert']:
    while True:
        print("Do you want to see your config? yes/no")
        result = input()
        if result in ["yes", "y", "ja", "j"]:
            print(
                f"Loaded Config:\n\
                [COMMON]\n\
                    geburtstag={settings.BIRTHDATE:%d.%m.%Y}\n\
                    postleitzahl={settings.ZIP}\n\
                [EMAIL]\n\
                    enable={settings.SEND_EMAIL}\n\
                    sender={settings.SENDER}\n\
                password={settings.PASSWORD}\n\
                    server={settings.SERVER}\n\
                    port={settings.PORT}\n\
                    empfaenger={settings.EMAIL_RECEIVERS}\n\
                [TELEGRAM]\n\
                    enable_telegram={settings.SEND_TELEGRAM_MSG}\n\
                    token={settings.TOKEN}\n\
                    chat_id={settings.CHAT_IDS}\n\
                [WEBBROWSER]\n\
                    open_browser={settings.OPEN_BROWSER}\n\
                [ADVANCED]\n\
                    sleep_between_requests_in_s=settings.{settings.SLEEP_BETWEEN_REQUESTS_IN_S}\n\
                    sleep_between_failed_requests_in_s={settings.SLEEP_BETWEEN_FAILED_REQUESTS_IN_S}\n\
                    sleep_after_ipban_in_min={settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN}\n\
                    cooldown_after_found_in_min={settings.COOLDOWN_AFTER_FOUND_IN_MIN}\n\
                    jitter={settings.JITTER}\n\
                    sleep_at_night={settings.SLEEP_AT_NIGHT}\n\
                    user_agent={settings.USER_AGENT}")
            break
        elif result in ["no", "n", "nein"]:
            break
        else:
            print("Invalid input")


if not arg['alert']:
    log.info(f"Finished validation script. Press [enter] to close")
    input()
