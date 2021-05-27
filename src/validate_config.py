import argparse
from log import log
from alerts import alert


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alert', default=False, action='store_true',
                    help='validate alert with a test message. Default=False')
arg = parser.parse_args()

log.info(f"validate config.ini")

import settings

log.info(f"settings validation finished")

result = None
if arg.alert:
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

log.info(f"finished validation script")

if not arg.alert:
    input()
