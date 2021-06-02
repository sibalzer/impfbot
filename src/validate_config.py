import argparse
from log import log
from settings import settings
from alerts import alert

YES = ["yes", "y", "ja", "j"]
NO = ["no", "n", "nein"]

parser = argparse.ArgumentParser()
parser.add_argument('-f', '-c', '--config',
                    dest='configfile',
                    help='Path to config.ini file',
                    required=False,
                    default='config.ini')
parser.add_argument('-a', '--alert',
                    action='store_true',
                    help='validate alert with a test message. Default=False',
                    default=False)
arg = vars(parser.parse_args())

log.info("validate config.ini")

settings.load(arg['configfile'])

log.info("settings validation finished")


while True:
    if not arg['alert']:
        print("Do you want to send a test message? yes/no")
        result = input()

    if result in YES or arg['alert']:
        alert("Test", verbose=True)
        log.info("Finished: Sending test massages")
        break
    elif result in NO:
        break
    else:
        print("Invalid input")

if not arg['alert']:
    while True:
        print("Do you want to see your config? yes/no")
        result = input()
        if result in YES:
            print(settings)
            break
        elif result in NO:
            break
        else:
            print("Invalid input")


if not arg['alert']:
    log.info("Finished validation script. Press [enter] to close")
    input()
