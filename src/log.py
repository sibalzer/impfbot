import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("impfbot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

log = logging.getLogger()
