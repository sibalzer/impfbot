import unittest.mock as mock

from settings import settings, load
import alerts


@mock.patch('alerts.send_mail')
@mock.patch('alerts.send_telegram')
@mock.patch('webbrowser.open', return_value=None)
def test_alert(browser_mock, telegram_mock, email_mock):
    load("tests/configs/test-config.ini")

    msg = 'test'
    alerts.alert(msg)

    email_mock.assert_called_once_with(msg)
    telegram_mock.assert_called_once_with(msg)
    browser_mock.assert_called_once_with(
        alerts.APPOINTMENT_URL, new=1, autoraise=True)


@mock.patch('smtplib.SMTP', create=True)
def test_send_email(smtp_mock):
    load("tests/configs/test-config-email.ini")

    msg = 'test'
    alerts.send_mail(msg)

    smtp_mock.assert_called_once()

    smtp_mock_obj = smtp_mock.return_value.__enter__.return_value

    smtp_mock_obj.login.assert_called_once_with(
        settings.EMAIL_USER, settings.EMAIL_PASSWORD)
    smtp_mock_obj.send_message.assert_called_once()


@mock.patch('apprise.Apprise.notify', return_value=None)
def test_send_telegram_msg(apprise_notify_mock):
    load("tests/configs/test-config-telegram.ini")

    msg = 'test'
    alerts.send_telegram(msg)

    assert apprise_notify_mock.called_once()


@mock.patch('webbrowser.open', return_value=None)
def test_open_browser(webbrowser_mock):
    load("tests/configs/test-config-browser.ini")

    alerts.alert('')

    webbrowser_mock.assert_called_once_with(
        alerts.APPOINTMENT_URL, new=1, autoraise=True)


@mock.patch('apprise.Apprise.notify', return_value=None)
def test_send_apprise(apprise_notify_mock):
    load("tests/configs/test-config-apprise.ini")

    msg = 'test'
    alerts.send_apprise(msg)

    assert apprise_notify_mock.called_once()
