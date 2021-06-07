"""alert service handler"""

import smtplib
import webbrowser
import logging
from email.message import EmailMessage
from email.utils import formatdate
from telegram.ext import Updater
from telegram.parsemode import ParseMode
from telegram.error import TelegramError

from common import APPOINTMENT_URL
from settings import settings

log = logging.getLogger(__name__)


def alert(msg: str) -> None:
    """Calls alert services with message"""
    if settings.EMAIL_ENABLE:
        log.debug("[EMAIL] try to send _e-mail")
        try:
            send_mail(msg)
            log.debug("[EMAIL] sending _e-mail was successful")
        except smtplib.SMTPException as _e:
            log.error(f"[EMAIL] Couldn't send mail: {_e}")
    else:
        log.debug("[EMAIL] enable is not set to true. Skipping...")

    if settings.TELEGRAM_ENABLE:
        log.debug("[TELEGRAM] Try to send telegram message")
        try:
            send_telegram_msg(msg)
            log.debug("[TELEGRAM] Sending telegram message was successful")
        except TelegramError as _e:
            log.error(f"[TELEGRAM] Couldn't send Telegram message: {_e}")
    else:
        log.debug(
            "[TELEGRAM] enable is not set to true. Skipping...")

    if settings.WEBBROWSER_ENABLE:
        log.debug("[WEBBROWSER] try to open browser")
        try:
            webbrowser.open(APPOINTMENT_URL, new=1, autoraise=True)
            log.debug("[WEBBROWSER] Open browser was successful")
        except webbrowser.Error as _e:
            log.error(f"[WEBBROWSER] Couldn't open browser: {_e}")
    else:
        log.debug(
            "[WEBBROWSER] enable is not set to true. Skipping...")


def send_mail(msg: str) -> None:
    """email alert service"""
    mail = EmailMessage()

    mail['From'] = settings.EMAIL_SENDER
    mail['To'] = settings.EMAIL_SENDER
    mail['Bcc'] = settings.EMAIL_RECEIVERS
    mail['Date'] = formatdate(localtime=True)
    mail['subject'] = msg
    mail.set_content(APPOINTMENT_URL)

    with smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT) as smtp:
        smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        smtp.send_message(mail)


def send_telegram_msg(msg: str) -> None:
    """telegram alert service"""
    update = Updater(settings.TELEGRAM_TOKEN)
    for chat_id in settings.TELEGRAM_CHAT_IDS:
        update.bot.send_message(
            chat_id=chat_id,
            text=f"*{msg}*\n{APPOINTMENT_URL}",
            parse_mode=ParseMode.MARKDOWN
        )
