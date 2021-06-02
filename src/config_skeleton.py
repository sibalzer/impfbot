"""skelton data for the settings"""

from datetime import datetime
from common import BIRTHDATE_REGEX, BOOL_REGEX, NOTIFIER_REGEX, NUMBER_REGEX, USER_AGENT_REGEX, ZIP_REGEX


SKELETON = {
    "COMMON": {
        "zip_code": {
            "default": None,
            "type": int,
            "regex": ZIP_REGEX
        },
        "birthdate": {
            "default": None,
            "type": datetime,
            "regex": BIRTHDATE_REGEX
        }
    },
    "EMAIL": {
        "enable": {
            "default": False,
            "type": bool,
            "regex": BOOL_REGEX
        },
        "sender": {
            "default": None,
            "type": str,
            "regex": NOTIFIER_REGEX["sender"]
        },
        "user": {
            "default": None,
            "type": str,
            "regex": NOTIFIER_REGEX["user"]
        },
        "password": {
            "default": None,
            "type": str,
            "regex": NOTIFIER_REGEX["password"],
        },
        "server": {
            "default": None,
            "type": str,
            "regex": NOTIFIER_REGEX["server"]
        },
        "port": {
            "default": None,
            "type": int,
            "regex": NOTIFIER_REGEX["port"]
        },
        "receivers": {
            "default": None,
            "type": list,
            "regex": NOTIFIER_REGEX["receivers"]
        }
    },
    "TELEGRAM": {
        "enable": {
            "default": False,
            "type": bool,
            "regex": BOOL_REGEX
        },
        "token": {
            "default": 30,
            "type": str,
            "regex": NOTIFIER_REGEX["token"]
        },
        "chat_ids": {
            "default": 30,
            "type": list,
            "regex": NOTIFIER_REGEX["chat_ids"]
        },
    },
    "WEBBROWSER": {
        "enable": {
            "default": False,
            "type": bool,
            "regex": BOOL_REGEX
        },
    },
    "ADVANCED": {
        "cooldown_between_requests": {
            "default": 30,
            "type": float,
            "regex": NUMBER_REGEX
        },
        "cooldown_between_failed_requests": {
            "default": 5,
            "type": float,
            "regex": NUMBER_REGEX
        },
        "cooldown_after_ip_ban": {
            "default": 60*5,
            "type": float,
            "regex": NUMBER_REGEX
        },
        "cooldown_after_success": {
            "default": 30,
            "type": float,
            "regex": NUMBER_REGEX
        },
        "jitter": {
            "default": 30,
            "type": float,
            "regex": NUMBER_REGEX
        },
        "sleep_at_night": {
            "default": True,
            "type": bool,
            "regex": BOOL_REGEX
        },
        "user_agent": {
            "default": "impfbot",
            "type": str,
            "regex": USER_AGENT_REGEX
        },
    }
}

DEPRACATED_CONFIG_MAP = {
    "postleitzahl": "zip_code",
    "geburtstag": "birthdate",
    "empfaenger": "receivers",
    "enable_telegram": "enable",
    "chat_id": "chat_ids",
    "sleep_between_requests_in_s": "cooldown_between_requests",
    "sleep_between_failed_requests_in_s": "cooldown_between_failed_requests",
    "sleep_after_ipban_in_min": "cooldown_after_ip_ban",
    "cooldown_after_found_in_min": "cooldown_after_success",
}
