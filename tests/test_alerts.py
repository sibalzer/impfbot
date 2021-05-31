import settings
import alerts
import unittest.mock as mock


@mock.patch('alerts.send_mail')
@mock.patch('alerts.send_telegram_msg')
@mock.patch('webbrowser.open')
def test_alert(browser_mock, telegram_mock, email_mock):
    settings.load("tests/configs/test-config.ini")

    msg = 'test'
    alerts.alert(msg)

    email_mock.assert_called_once_with(msg)
    telegram_mock.assert_called_once_with(msg)
    browser_mock.assert_called_once_with(alerts.appointment_url)


@mock.patch('smtplib.SMTP')
def atest_send_email(smtp_mock):
    settings.load("tests/configs/test-config-email.ini")

    msg = 'test'
    alerts.send_mail(msg)

    smtp_mock.assert_called_once()
    smtp_mock.login.assert_called_once_with(
        settings.SERVER, settings.PORT)
    smtp_mock.send_message.assert_called_once()


@mock.patch('smtplib.SMTP_SSL')
def atest_send_email_ssl(smtp_mock):
    settings.load("tests/configs/test-config-email-ssl.ini")

    msg = 'test'
    alerts.send_mail(msg)

    smtp_mock.assert_called_once()
    smtp_mock.assert_called_once_with(
        settings.SERVER, settings.PORT)
    smtp_mock.send_message.assert_called_once()


@mock.patch('telegram.bot.Bot._validate_token', return_value=None)
@mock.patch('telegram.bot.Bot.send_message', return_value=None)
def test_send_telegram_msg(telegram_send_mock, telegram_validate_token_mock):
    settings.load("tests/configs/test-config-telegram.ini")

    msg = 'test'
    alerts.send_telegram_msg(msg)

    for chat_id in settings.CHAT_IDS:
        assert telegram_send_mock.call_count == len(settings.CHAT_IDS)
        assert telegram_send_mock.call_args[1]["chat_id"] in settings.CHAT_IDS


@mock.patch('webbrowser.open')
def test_open_browser(webbrowser_mock):
    settings.load("tests/configs/test-config-browser.ini")

    alerts.alert('')

    webbrowser_mock.assert_called_once_with(alerts.appointment_url)
