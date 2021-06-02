import unittest.mock as mock

from settings import settings, load
import alerts


@mock.patch('alerts.send_mail')
@mock.patch('alerts.send_telegram_msg')
@mock.patch('webbrowser.open', return_value=None)
def test_alert(browser_mock, telegram_mock, email_mock):
    load("tests/configs/test-config.ini")

    msg = 'test'
    alerts.alert(msg)

    email_mock.assert_called_once_with(msg)
    telegram_mock.assert_called_once_with(msg)
    browser_mock.assert_called_once_with(alerts.APPOINTMENT_URL)


@mock.patch('smtplib.SMTP', create=True)
def test_send_email(smtp_mock):
    load("tests/configs/test-config-email.ini")

    msg = 'test'
    alerts.send_mail(msg)

    smtp_mock.assert_called_once()

    smtp_mock_obj = smtp_mock.return_value.__enter__.return_value

    smtp_mock_obj.login.assert_called_once_with(
        settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
    smtp_mock_obj.send_message.assert_called_once()


@mock.patch('telegram.bot.Bot._validate_token', return_value=None)
@mock.patch('telegram.bot.Bot.send_message', return_value=None)
def test_send_telegram_msg(telegram_send_mock, telegram_validate_token_mock):
    load("tests/configs/test-config-telegram.ini")

    msg = 'test'
    alerts.send_telegram_msg(msg)

    for chat_id in settings.TELEGRAM_CHAT_IDS:
        assert telegram_send_mock.call_count == len(settings.TELEGRAM_CHAT_IDS)
        assert telegram_send_mock.call_args[1]["chat_id"] in settings.TELEGRAM_CHAT_IDS


@mock.patch('webbrowser.open', return_value=None)
def test_open_browser(webbrowser_mock):
    load("tests/configs/test-config-browser.ini")

    alerts.alert('')

    webbrowser_mock.assert_called_once_with(alerts.APPOINTMENT_URL)
