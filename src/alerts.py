import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from telegram.ext import Updater
import webbrowser
import logging

import settings


appointment_url = r"https://www.impfportal-niedersachsen.de/portal/#/appointment/public"


log = logging.getLogger(__name__)


def alert(msg: str) -> None:
    if settings.SEND_EMAIL:
        try:
            send_mail(msg)
        except Exception as e:
            log.error(f"Couldn't send mail: {e}")
    if settings.SEND_TELEGRAM_MSG:
        try:
            send_telegram_msg(msg)
        except:
            log.error(f"Couldn't send Telegram message: {e}")
    if settings.OPEN_BROWSER:
        try:
            webbrowser.open(appointment_url)
        except Exception as e:
            log.error(f"Couldn't open browser: {e}")


def send_mail(msg: str) -> None:
    mail = EmailMessage()

    mail['From'] = settings.SENDER
    mail['To'] = settings.SENDER
    mail['Bcc'] = settings.EMAIL_RECEIVERS
    mail['Date'] = formatdate(localtime=True)
    mail['subject'] = msg
    mail.set_content(appointment_url)

    with smtplib.SMTP_SSL(settings.SERVER, settings.PORT)as smtp:
        smtp.login(settings.SENDER, settings.PASSWORD)
        smtp.send_message(mail)

def send_telegram_msg(msg: str) -> None:
    update = Updater(settings.TOKEN)
    update.bot.send_message(
        chat_id=settings.CHAT_ID,
        text=msg
    )
