"""config parser modul"""
from configparser import RawConfigParser
import re
import logging
from datetime import datetime

from config_skeleton import SKELETON, DEPRACATED_CONFIG_MAP
from common import NOTIFIERS

__log = logging.getLogger(__name__)


class Datastore():
    """data-class for settings"""

    def __str__(self):
        result = ""
        for section in SKELETON:
            result += f"[{section}]\n"
            for option in SKELETON[section]:
                name_builder = option.upper()
                if section not in "ADVANCED":
                    name_builder = f"{section.upper()}_{option.upper()}"
                value = getattr(self, name_builder, "not set")
                if isinstance(value, list):
                    list_str = ""
                    for entry in value:
                        list_str += str(entry)
                    value = list_str
                result += f"   {option}: {value}\n"
        return result

    def clear(self):
        """removes all settings"""
        attributes = list(settings.__dict__)
        for att in attributes:
            delattr(self, att)


settings = Datastore()


class ParseExeption(BaseException):
    """data-class for settings"""


def __set_option(section: str, option: str, value: str, multiplyer: int = 1):
    """sets an option in the data class"""
    regex = SKELETON[section][option]["regex"]

    name_builder = option.upper()
    if section != "ADVANCED":
        name_builder = f"{section.upper()}_" + name_builder

    if re.match(regex, value):
        typ: any = SKELETON[section][option]["type"]

        if issubclass(typ, datetime):
            value = datetime.strptime(value, r'%d.%m.%Y')
        elif typ is float:
            value = typ(value)*multiplyer
        elif typ is bool:
            value = value == "true"
        elif typ is list:
            value = value.split(',')
        else:
            value = typ(value)

        setattr(settings, name_builder, value)


def __parse(config: RawConfigParser):
    for section in config.sections():
        if section in SKELETON:
            __parse_section(config, section)
        else:
            __log.warning(
                f"[{section}] is unknown")


def __parse_section(config: RawConfigParser, section: str):
    """parse a settings section"""
    for option in config.options(section):
        try:
            __parse_option(config, section, option)
        except Exception as ex:
            __log.error(
                f"[{section}] '{option}' error during parsing: {ex}")


def __parse_option(config: RawConfigParser, section: str, option: str):
    """parse a single setting option"""
    if option in SKELETON[section]:
        value = config[section][option]
        __set_option(section, option, value)

    # depracated config
    elif (section, option) in DEPRACATED_CONFIG_MAP:
        new_option = DEPRACATED_CONFIG_MAP[(section, option)]
        value = config[section][option]
        if option[-7:] == "_in_min":
            __set_option(section, new_option, value, 60)
        else:
            __set_option(section, new_option, value)

        __log.warning(
            f"[{section}] '{option}' is depracated please use: '{new_option}'")

    # unknown
    else:
        __log.warning(f"[{section}] '{option}' is unknown.")


def __validate():
    for section in SKELETON:
        __validate_section(section)


def __validate_section(section: str):
    for option in SKELETON[section]:
        __validate_option(section, option)


def __validate_option(section: str, option: str):
    if section == "COMMON":
        option_name = f'COMMON_{option.upper()}'
        if option in ["birthdate", "group_size"]:
            if not hasattr(settings, "COMMON_BIRTHDATE") and not hasattr(settings, "COMMON_GROUP_SIZE"):
                raise ParseExeption(
                    f"[{section}] 'birthdate' or 'group_size' must be in the config.")

            if not hasattr(settings, "COMMON_BIRTHDATE") ^ hasattr(settings, "COMMON_GROUP_SIZE"):
                raise ParseExeption(
                    f"[{section}] only one of 'birthdate' or 'group_size' is allowed in the same config.")
        else:
            if getattr(settings, option_name, None) is None:
                raise ParseExeption(
                    f"[{section}] '{option}' must be in the config.")

    elif section in NOTIFIERS:
        option_name = f"{section.upper()}_{option.upper()}"
        name_enable = f"{section.upper()}_ENABLE"
        if getattr(settings, name_enable, False):
            if getattr(settings, option_name, None) is None:
                if (section == "EMAIL" and option == "user"
                    # depracated special case email user
                        and getattr(settings, "EMAIL_SENDER") is not None):
                    __set_option(section, "user", getattr(
                        settings, "EMAIL_SENDER"))
                    __log.warning(
                        f"[{section}] '{option}' is missing; set sender as user")
                else:
                    __set_option(section, "enable", "False")
                    __log.warning(
                        f"[{section}] '{option}' not valid or missing. Disable [{section}]")
        else:
            __set_option(section, "enable", "False")
            if option == "enable":
                __log.info(
                    f"[{section}] '{option}' is set to 'false'. Disable [{section}]")

    elif section == "ADVANCED":
        name = option.upper()
        if getattr(settings, name, None) is None:
            value = SKELETON[section][option]["default"]
            typ: any = SKELETON[section][option]["type"]
            setattr(settings, option.upper(), typ(value))

            __log.warning(
                f"[{section}] '{option}' not set. Using default: '{value}'")
            return
    else:
        raise ParseExeption(
            f"[{section}] '{option}' is unknown")


def load(path):
    """loads a config file"""
    settings.clear()
    config = RawConfigParser()
    dataset = config.read(path)
    if not dataset:
        raise FileNotFoundError("config.ini not found.")

    __parse(config)
    __validate()
