import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from telegram.ext import Updater
from telegram.parsemode import ParseMode
import webbrowser
import logging

import settings


appointment_url = r"https://www.impfportal-niedersachsen.de/portal/#/appointment/public"


log = logging.getLogger(__name__)

verbose_print = False


def verbose_info(msg: str) -> None:
    if verbose_print:
        log.info(msg)


def alert(msg: str, verbose: bool = False) -> None:
    global verbose_print
    verbose_print = verbose

    if settings.SEND_EMAIL:
        verbose_info(f"[EMAIL] try to send e-mail")
        try:
            send_mail(msg)
            verbose_info(f"[EMAIL] sending e-mail was successful")
        except Exception as e:
            log.error(f"Couldn't send mail: {e}")
    else:
        verbose_info(f"[EMAIL] send_mail is not set to true skipping")

    if settings.SEND_TELEGRAM_MSG:
        verbose_info(f"[TELEGRAM] try to send telegram message")
        try:
            send_telegram_msg(msg)
            verbose_info(f"[TELEGRAM] sending telegram message was successful")
        except Exception as e:
            log.error(f"Couldn't send Telegram message: {e}")
    else:
        verbose_info(
            f"[TELEGRAM] send_telegram_msg is not set to true skipping")

    if settings.OPEN_BROWSER:
        verbose_info(f"[WEBBROWSER] try to open browser")
        try:
            webbrowser.open(appointment_url)
            verbose_info(f"[WEBBROWSER] open browser was successful")
        except Exception as e:
            log.error(f"Couldn't open browser: {e}")
    else:
        verbose_info(f"[WEBBROWSER] open_browser is not set to true skipping")


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
    for chat_id in settings.CHAT_IDS:
        update.bot.send_message(
            chat_id=chat_id,
            text=f"*{msg}*\n{appointment_url}",
            parse_mode=ParseMode.MARKDOWN
        )
