
from configparser import ConfigParser
import re
import logging

from config_skeleton import *


settings = __import__(__name__)

log = logging.getLogger()


class ParseExeption(BaseException):
    pass


def validate_option(config: ConfigParser, section: str, option: str):
    regex = SKELETON_DEFAULT[section][option]["regex"]
    if re.match(regex, config[section][option]):
        return
    else:
        raise ParseExeption(f"[{section}] {option} is not valid.")


def set_option(config: ConfigParser, section: str, option: str):
    value = config[section][option]
    type: any = SKELETON_DEFAULT[section][option]["type"]
    setattr(settings, f"{section.upper()}_{option.upper}", type(value))


def parse_option(config: ConfigParser, section: str, option: str):
    if config.has_section(section) and config.has_option(option):
        validate_option(config, section, option)
        set_option(config, section, option)
        return
    if option in DEPRACATED_CONFIG_MAP.keys:
        new_key_name = DEPRACATED_CONFIG_MAP[option]
        validate_option(config, section, new_key_name)
        set_option(config, section, new_key_name)
        return
    if section in NOTIFIERS:
        value = SKELETON_DEFAULT[section]["enable"]["default"]
        log.warning(f"{section}'{option}' not set. Disable [{section}]")
        return
    if section in "ADVANCED":
        value = SKELETON_DEFAULT[section][option]["default"]
        type: any = SKELETON_DEFAULT[section][option]["type"]
        setattr(settings, f"{section.upper()}_{option.upper}", type(value))
        log.warning(f"{section}'{option}' not set. Using default: '{value}'")
        return
    raise ParseExeption(f"[{section}] {option} must be in the config.")


def load(path):
    config = ConfigParser()
    dataset = config.read(path)
    if not dataset:
        raise FileNotFoundError("Could not find config file. Exit...")

    for section in SKELETON_DEFAULT:
        for option in section:
            parse_option(config, section, option)


def __str__(self):
    for section in SKELETON_DEFAULT.keys:
        print(f"[{section}]")
        for option in section.keys:
            value = getattr(self, option.to_upper())
            print(f"   {option}: {value}")
