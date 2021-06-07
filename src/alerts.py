"""alert service handler"""

import apprise
import smtplib
import webbrowser
import logging
from email.message import EmailMessage
from email.utils import formatdate
import ssl

from common import APPOINTMENT_URL
from settings import settings

log = logging.getLogger(__name__)


def alert(msg: str) -> None:
    """Calls alert services with message"""
    if settings.EMAIL_ENABLE:
        log.debug("[EMAIL] try to send e-mail")
        try:
            send_mail(msg)
            log.info("[EMAIL] sending e-mail was successful")
        except smtplib.SMTPException as ex:
            log.error(f"[EMAIL] Couldn't send mail: {ex}")
    else:
        log.debug("[EMAIL] enable is not set to true. Skipping...")

    if settings.TELEGRAM_ENABLE:
        log.debug("[TELEGRAM] Try to send telegram message")
        try:
            send_telegram(msg)
        except Exception as ex:
            log.error(f"[TELEGRAM] Couldn't send Telegram message: {ex}")
    else:
        log.debug(
            "[TELEGRAM] enable is not set to true. Skipping...")

    if settings.WEBBROWSER_ENABLE:
        log.debug("[WEBBROWSER] try to open browser")
        try:
            webbrowser.open(APPOINTMENT_URL, new=1, autoraise=True)
            log.info("[WEBBROWSER] Open browser was successful")
        except webbrowser.Error as ex:
            log.error(f"[WEBBROWSER] Couldn't open browser: {ex}")
    else:
        log.debug(
            "[WEBBROWSER] enable is not set to true. Skipping...")

    if settings.APPRISE_ENABLE:
        log.debug(f"[APPRISE] try to send Apprise Notification")
        try:
            send_apprise(msg)
        except Exception as ex:
            log.error(f"Couldn't send Apprise Notification: {ex}")
    else:
        log.debug(f"[APPRISE] send_apprise is not set to true skipping")


def send_mail(msg: str) -> None:
    """email alert service"""
    mail = EmailMessage()

    mail['From'] = settings.EMAIL_SENDER
    mail['To'] = settings.EMAIL_SENDER
    mail['Bcc'] = settings.EMAIL_RECEIVERS
    mail['Date'] = formatdate(localtime=True)
    mail['subject'] = msg
    mail.set_content(APPOINTMENT_URL)

    if settings.EMAIL_PORT == 465:
        with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT)as smtp:
            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            smtp.send_message(mail)
    elif settings.EMAIL_PORT == 587:
        with smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            smtp.send_message(mail)
    else:
        with smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)as smtp:
            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            smtp.send_message(mail)


def send_telegram(msg: str) -> None:
    """telegram alert service"""
    appobj = apprise.Apprise()

    url = f"tgram://{settings.TELEGRAM_TOKEN}"
    for chat_id in settings.TELEGRAM_CHAT_IDS:
        url += f"/{chat_id}"
    url += "?format=markdown"

    appobj.add(url)

    appobj.notify(
        body=f"{APPOINTMENT_URL}",
        title=f"**{msg}**",
    )


def send_apprise(msg: str) -> None:
    """apprise alert service"""
    appobj = apprise.Apprise()

    for url in settings.APPRISE_SERVICE_URIS:
        appobj.add(url)

    appobj.notify(
        body=f"{APPOINTMENT_URL}",
        title=f"{msg}",
    )
