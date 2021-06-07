"""tests for settings.py"""
from datetime import datetime
from unittest import mock
import pytest
from freezegun import freeze_time

from settings import settings, load, ParseExeption


@freeze_time("2021-01-01 03:21:34")
@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_valid(log_info_mock,
               log_warning_mock,
               log_error_mock):
    """test for vaccine in stock"""
    load("tests/configs/test-config-valid.ini")

    # Check output
    log_info_mock.assert_not_called()
    log_warning_mock.assert_not_called()
    log_error_mock.assert_not_called()

    # COMMON
    assert settings.COMMON_ZIP_CODE == 30042
    assert settings.COMMON_BIRTHDATE == datetime(1912, 6, 23)

    # EMAIL
    assert settings.EMAIL_ENABLE is True
    assert settings.EMAIL_USER == "username"
    assert settings.EMAIL_PASSWORD == "secret"
    assert settings.EMAIL_SERVER == "mail.server.de"
    assert settings.EMAIL_PORT == 465
    assert settings.EMAIL_SENDER == "sender@server.de"
    assert settings.EMAIL_RECEIVERS == [
        "sender@server.de", "guenni@server.de", "frida@server.de"]

    # TELEGRAM
    assert settings.TELEGRAM_ENABLE is True
    assert settings.TELEGRAM_TOKEN == "secre0815:TOKEN"
    assert settings.TELEGRAM_CHAT_IDS == ["123456789", "987654321"]

    # WEBBROWSER
    assert settings.WEBBROWSER_ENABLE is True

    # ADVANCED
    assert settings.COOLDOWN_BETWEEN_REQUESTS == 60
    assert settings.COOLDOWN_BETWEEN_FAILED_REQUESTS == 10
    assert settings.COOLDOWN_AFTER_IP_BAN == 10800
    assert settings.COOLDOWN_AFTER_SUCCESS == 900
    assert settings.JITTER == 5
    assert settings.SLEEP_AT_NIGHT is False
    assert settings.USER_AGENT == "impfbot_v3"


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_invalid_zip_code(log_info_mock,
                          log_warning_mock,
                          log_error_mock):
    with pytest.raises(ParseExeption):
        load("tests/configs/test-config-invalid-zip-code.ini")


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_invalid_birthdate(log_info_mock,
                           log_warning_mock,
                           log_error_mock):

    with pytest.raises(ParseExeption):
        load("tests/configs/test-config-invalid-birthdate.ini")


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_invalid_email(log_info_mock,
                       log_warning_mock,
                       log_error_mock):
    load("tests/configs/test-config-invalid-email.ini")

    # Check output
    log_info_mock.assert_not_called()
    log_warning_mock.call_count = 6
    log_error_mock.assert_not_called()

    # EMAIL
    assert settings.EMAIL_ENABLE is False


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_invalid_telegram(log_info_mock,
                          log_warning_mock,
                          log_error_mock):
    load("tests/configs/test-config-invalid-telegram.ini")

    # Check output
    log_info_mock.assert_not_called()
    log_warning_mock.call_count = 3
    log_error_mock.assert_not_called()

    # TELEGRAM
    assert settings.TELEGRAM_ENABLE is False


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_invalid_advanced(log_info_mock,
                          log_warning_mock,
                          log_error_mock):
    load("tests/configs/test-config-invalid-advanced.ini")

    # Check output
    log_info_mock.assert_not_called()
    log_warning_mock.call_count = 7 - 1
    log_error_mock.assert_not_called()

    # ADVANCED
    assert settings.COOLDOWN_BETWEEN_REQUESTS == 30
    assert settings.COOLDOWN_BETWEEN_FAILED_REQUESTS == 5
    assert settings.COOLDOWN_AFTER_IP_BAN == 10800
    assert settings.COOLDOWN_AFTER_SUCCESS == 900
    assert settings.JITTER == 10
    assert settings.SLEEP_AT_NIGHT is True
    assert settings.USER_AGENT == "impfbot"


@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_old(log_info_mock,
             log_warning_mock,
             log_error_mock):
    load("tests/configs/test-config-old.ini")

    # Check output
    log_info_mock.assert_not_called()
    assert log_warning_mock.call_count == 11
    for msg in log_warning_mock.call_args_list:
        assert (" is depracated please use: " in msg.args[0]
                or "[EMAIL] 'user' setting sender as user" in msg.args[0])
    log_error_mock.assert_not_called()

    # COMMON
    assert settings.COMMON_ZIP_CODE == 19042
    assert settings.COMMON_BIRTHDATE == datetime(1912, 6, 23)

    # EMAIL
    assert settings.EMAIL_ENABLE is True
    assert settings.EMAIL_USER == "sender@server.de"
    assert settings.EMAIL_PASSWORD == "xxxx"
    assert settings.EMAIL_SERVER == "mail.server.de"
    assert settings.EMAIL_PORT == 465
    assert settings.EMAIL_SENDER == "sender@server.de"
    assert settings.EMAIL_RECEIVERS == [
        "sender@server.de", "guenni@server.de", "frida@server.de"]

    # TELEGRAM
    assert settings.TELEGRAM_ENABLE is True
    assert settings.TELEGRAM_TOKEN == "TOKEN"
    assert settings.TELEGRAM_CHAT_IDS == ["123456789", "987654321"]

    # WEBBROWSER
    assert settings.WEBBROWSER_ENABLE is True

    # ADVANCED
    assert settings.COOLDOWN_BETWEEN_REQUESTS == 1
    assert settings.COOLDOWN_BETWEEN_FAILED_REQUESTS == 2
    assert settings.COOLDOWN_AFTER_IP_BAN == 3*60
    assert settings.COOLDOWN_AFTER_SUCCESS == 4*60
    assert settings.JITTER == 5
    assert settings.SLEEP_AT_NIGHT is False
    assert settings.USER_AGENT == "impfbot"


@ mock.patch('logging.Logger.error')
@ mock.patch('logging.Logger.warning')
@ mock.patch('logging.Logger.info')
def test_missing_optional(log_info_mock,
                          log_warning_mock,
                          log_error_mock):
    load("tests/configs/test-config-optional-missing.ini")

    # Check output
    log_info_mock.assert_not_called()
    assert log_warning_mock.call_count == 10
    log_error_mock.assert_not_called()

    # EMAIL
    assert settings.EMAIL_ENABLE is False
    # TELEGRAM
    assert settings.TELEGRAM_ENABLE is False
    # WEBBROWSER
    assert settings.WEBBROWSER_ENABLE is False
    # ADVANCED
    assert settings.COOLDOWN_BETWEEN_REQUESTS == 30
    assert settings.COOLDOWN_BETWEEN_FAILED_REQUESTS == 5
    assert settings.COOLDOWN_AFTER_IP_BAN == 3*60*60
    assert settings.COOLDOWN_AFTER_SUCCESS == 15*60
    assert settings.JITTER == 10
    assert settings.SLEEP_AT_NIGHT is True
    assert settings.USER_AGENT == "impfbot"


@ mock.patch('logging.Logger.error')
@ mock.patch('logging.Logger.warning')
@ mock.patch('logging.Logger.info')
def test_missing_all(log_info_mock,
                     log_warning_mock,
                     log_error_mock):
    with pytest.raises(ParseExeption):
        load("tests/configs/test-invalid-file.ini")


@ mock.patch('logging.Logger.error')
@ mock.patch('logging.Logger.warning')
@ mock.patch('logging.Logger.info')
def test_invalid_file(log_info_mock,
                      log_warning_mock,
                      log_error_mock):
    with pytest.raises(FileNotFoundError):
        load("no file 4 u")
