from common import *


SKELETON_DEFAULT = {
    "COMMON": {
        "zip_code": {
            "default-value": None,
            "type": int,
            "regex": ZIP_REGEX
        },
        "birthdate": {
            "default-value": None,
            "type": bool,
            "regex": BIRTHDATE_REGEX
        }
    },
    "EMAIL": {
        "enable": {
            "default-value": False,
            "type": bool,
            "regex": BOOL_REGEX
        },
        "sender": {
            "default-value": None,
            "type": str,
            "regex": NOTIFIER_REGEX["sender"]
        },
        "password": {
            "default-value": None,
            "type": str,
            "regex": NOTIFIER_REGEX["password"],
        },
        "server": {
            "default-value": None,
            "type": str,
            "regex": NOTIFIER_REGEX["server"]
        },
        "port": {
            "default-value": None,
            "type": int,
            "regex": NOTIFIER_REGEX["port"]
        },
        "recievers": {
            "default-value": None,
            "type": list[str],
            "regex": NOTIFIER_REGEX["recievers"]
        }
    },
    "TELEGRAM": {
        "enable": {
            "default-value": False,
            "type": bool,
            "regex": BOOL_REGEX
        },
        "token": {
            "default-value": 30,
            "type": str,
            "regex": NOTIFIER_REGEX["token"]
        },
        "chat_ids": {
            "default-value": 30,
            "type": list[str],
            "regex": NOTIFIER_REGEX["chat_ids"]
        },
    },
    "ADVANCED": {
        "cooldown_between_requests": {
            "default-value": 30,
            "type": float,
            "regex": TIME_REGEX
        },
        "cooldown_between_failed_requests": {
            "default-value": 5,
            "type": float,
            "regex": TIME_REGEX
        },
        "cooldown_after_ip_ban": {
            "default-value": 60*5,
            "type": float,
            "regex": TIME_REGEX
        },
        "cooldown_after_success": {
            "default-value": 30,
            "type": float,
            "regex": TIME_REGEX
        },
        "jitter": {
            "default-value": 30,
            "type": float,
            "regex": TIME_REGEX
        },
        "sleep_at_night": {
            "default-value": True,
            "type": bool,
            "regex": BOOL_REGEX
        },
    }
}

DEPRACATED_CONFIG_MAP = {
    "zip_code": ["postleitzahl"],
    "birthdate": ["geburtstag"],
    "recievers": ["empfaenger"],
    "enable": ["enable_telegram"],
    "chat_ids": ["chat_id"],
    "cooldown_between_requests": ["sleep_between_requests_in_s"],
    "cooldown_between_failed_requests": ["sleep_between_failed_requests_in_s"],
    "cooldown_after_ip_ban": ["sleep_after_ipban_in_min"],
    "cooldown_after_success": ["cooldown_after_found_in_min"],
}
