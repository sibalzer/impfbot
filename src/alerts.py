import smtplib
import webbrowser
import logging
from email.message import EmailMessage
from email.utils import formatdate
from telegram.ext import Updater
from telegram.parsemode import ParseMode

from common import APPOINTMENT_URL
import settings

log = logging.getLogger(__name__)


def alert(msg: str) -> None:

    if settings.SEND_EMAIL:
        log.debug("[EMAIL] try to send e-mail")
        try:
            send_mail(msg)
            log.debug("[EMAIL] sending e-mail was successful")
        except Exception as e:
            log.error(f"[EMAIL] Couldn't send mail: {e}")
    else:
        log.debug("[EMAIL] enable is not set to true. Skipping...")

    if settings.SEND_TELEGRAM_MSG:
        log.debug("[TELEGRAM] Try to send telegram message")
        try:
            send_telegram_msg(msg)
            log.debug("[TELEGRAM] Sending telegram message was successful")
        except Exception as e:
            log.error(f"[TELEGRAM] Couldn't send Telegram message: {e}")
    else:
        log.debug(
            "[TELEGRAM] enable is not set to true. Skipping...")

    if settings.OPEN_BROWSER:
        log.debug("[WEBBROWSER] try to open browser")
        try:
            webbrowser.open(APPOINTMENT_URL, new=1, autoraise=True)
            log.debug("[WEBBROWSER] Open browser was successful")
        except Exception as e:
            log.error(f"[WEBBROWSER] Couldn't open browser: {e}")
    else:
        log.debug(
            "[WEBBROWSER] enable is not set to true. Skipping...")


def send_mail(msg: str) -> None:
    mail = EmailMessage()

    mail['From'] = settings.SENDER
    mail['To'] = settings.SENDER
    mail['Bcc'] = settings.EMAIL_RECEIVERS
    mail['Date'] = formatdate(localtime=True)
    mail['subject'] = msg
    mail.set_content(APPOINTMENT_URL)

    with smtplib.SMTP(settings.SERVER, settings.PORT)as smtp:
        smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        smtp.send_message(mail)


def send_telegram_msg(msg: str) -> None:
    update = Updater(settings.TOKEN)
    for chat_id in settings.CHAT_IDS:
        update.bot.send_message(
            chat_id=chat_id,
            text=f"*{msg}*\n{APPOINTMENT_URL}",
            parse_mode=ParseMode.MARKDOWN
        )
