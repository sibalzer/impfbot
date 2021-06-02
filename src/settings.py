from configparser import ConfigParser
import re
import logging
from datetime import datetime
from tkinter.constants import NO

from config_skeleton import SKELETON, DEPRACATED_CONFIG_MAP
from config_generator import start_config_generation
from common import NOTIFIERS

log = logging.getLogger(__name__)


class Datastore():
    def __str__(self):
        result = ""
        for section in SKELETON:
            result += f"[{section}]\n"
            for option in SKELETON[section]:
                name_builder = option.upper()
                if section not in "ADVANCED":
                    name_builder = f"{section.upper()}_{option.upper()}"
                value = getattr(self, name_builder)
                if type(value) is list:
                    list_str = ""
                    for entry in value:
                        list_str += str(entry)
                    value = list_str
                result += f"   {option}: {value}\n"
        return result


settings = Datastore()


class ParseExeption(BaseException):
    pass


def validate_option(config: ConfigParser, section: str, option: str, alt_name: str = ""):
    regex = SKELETON[section][option]["regex"]

    if alt_name:
        if re.match(regex, config[section][alt_name]):
            return True
    else:
        if re.match(regex, config[section][option]):
            return True

    return False


def set_option(config: ConfigParser, section: str, option: str, alt_name: str = ""):
    if alt_name:
        value = config[section][alt_name]
    else:
        value = config[section][option]
    t: any = SKELETON[section][option]["type"]

    name_builder = option.upper()
    if section != "ADVANCED":
        name_builder = f"{section.upper()}_" + name_builder

    if t is datetime:
        value = datetime.strptime(value, r'%d.%m.%Y')
    elif t is float:
        value = t(value)
        if alt_name[-7:] == "_in_min":
            value *= 60
    elif t is bool:
        value = value == "true"
    elif t is list:
        value = value.split(',')
    else:
        value = t(value)

    setattr(settings, name_builder, value)


def parse_option(config: ConfigParser, section: str, option: str):
    if config.has_option(section, option) and validate_option(config, section, option):
        set_option(config, section, option)
        return

    elif option in DEPRACATED_CONFIG_MAP.values():
        for old_key in DEPRACATED_CONFIG_MAP:
            if DEPRACATED_CONFIG_MAP[old_key] == option:
                new_key = DEPRACATED_CONFIG_MAP[old_key]
                if validate_option(config, section, new_key, alt_name=old_key):
                    set_option(config, section, new_key, alt_name=old_key)
                    return
                else:
                    ParseExeption(f"[{section}] '{option}'' is not valid.")

    elif section in NOTIFIERS:
        value = SKELETON[section]["enable"]["default"]
        type: any = SKELETON[section][option]["type"]
        name_builder = f"{section.upper()}_ENABLE"
        setattr(settings, option, None)
        setattr(settings, name_builder, type(value))

        log.warning(f"[{section}] '{option}' not valid. Disable [{section}]")
        return

    elif section in "ADVANCED":
        value = SKELETON[section][option]["default"]
        type: any = SKELETON[section][option]["type"]
        setattr(settings, option.upper(), type(value))

        log.warning(
            f"[{section}] '{option}' not set. Using default: '{value}'")
        return

    raise ParseExeption(f"[{section}] '{option}'' must be in the config.")


def load(path):
    config = ConfigParser()
    dataset = config.read(path)
    if not dataset:
        start_config_generation()

    for section in SKELETON:
        for option in SKELETON[section]:
            try:
                parse_option(config, section, option)
            except ParseExeption as _e:
                log.warning(_e)
            except Exception as _e:
                log.error(f"[{section}] '{option}' error during parsing: {_e}")
