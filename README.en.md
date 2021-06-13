# Notification bot for the Lower Saxony vaccination portal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![codecov](https://codecov.io/gh/sibalzer/impfbot/branch/main/graph/badge.svg?token=XXI3N5A9X1)](https://codecov.io/gh/sibalzer/impfbot)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

_Zur deutschen Version geht's [hier](https://github.com/sibalzer/impfbot/blob/main/README.md)._

A little weekend project of mine. The bot monitors the REST-API of the lower saxony vaccination portal (https://impfportal-niedersachsen.de) for free vaccination slots and sends a notification via mail. From then on, unfortunately, the fastest wins. Please do not abuse the bot and use moderate intervals.

## 🤖 Features

- Automatic search for short term vaccination dates
- Notifications via email and telegram & many more
- Opens your browser automatically when an appointment is found. All you have to do is enter your details!
- Simple setup with GUI

> What the impfbot doesn't do: Book the appointment for you and/or enter your data automatically.

### ⚠️ Disclaimer

Using this bot does __not__ guarantee to get you a vaccination appointment. Please also use the waiting list of your local vaccination centre and your family physician!

## ⚙️ Setup

### Requirements

- python 3.x via https://www.python.org/downloads/

### 📝 Instructions

Using Windows as an example:

1. download and install python from here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. download the bot (Releases on the right side or [here](https://github.com/sibalzer/impfbot/releases/latest))
3. unpack the archive (the zip file)
4. rename `config.example.ini` to `config.ini` and fill in your data (zip code, birthday, email server data)
5. double-click on `windows_validate.bat` to check the config file
6. double-click on `windows_start.bat`

For advanced users, a docker container is also available as an alternative. See [docker](https://github.com/sibalzer/impfbot/tree/main/docker) for more information. Validating the config works via the command `docker exec impfbot python src/validate_config.py -a`.

### 📣 Setting up Telegram

1. write to https://t.me/BotFather and create bot. Then copy the token to `config.ini`.

The following steps must be performed for everyone who wants to receive messages.

2. write to https://t.me/userinfobot and copy "Id"-number into `config.ini` (separated with `,`)
3. ⚠ You have to start a conversation with your own bot before! (URL is in the Botfather message, press /start there). ⚠
4. validate that everything works: Double click on `test_telegram.bat`

### 🛠️ config.ini parameters

- **\[COMMON\]**: General settings
  - `birthday` - Birthday to be queried. Example: `23.06.1912`.
  - `group_size` - Size of the group for which an appointment is requested (2 to 15). Example: `5`
  - `zip_code` - Five-digit zip code for your vaccination center. Example: `49123`
- **\[EMAIL\]**: Email settings
  - `enable` - Specifies whether emails should be sent. `true` if yes, `false` otherwise.
  - `sender` - The email address from which the notifications should be sent. Example: `sender@server.tld`.
  - `user` - Login name for the SMTP server (in most cases identical with the sender address)
  - `password` - The password for the SMTP server.
  - `server` - The SMTP server. Example: `smtp.server.tld`.
  - `port` - The port for the SMTP server. Example: `465`.
  - `receivers` - A list of e-mail addresses to which a message should be sent. Example: `sender@server.tld,foo@server.tld,hoo@server.tld` or (only to itself) `sender@server.tld`.
- **\[TELEGRAM\]**: Telegram settings
  - `enable` - Specifies whether Telegram messages should be sent. `true` if yes, otherwise `false`.
  - `token` - The bot token from https://t.me/BotFather
  - `chat_ids` - User-ID of the recipient: use https://t.me/userinfobot
- **\[WEBBROWSER\]**: Web browser settings
  - `enable` - Determines if the browser should be opened automatically. (Only on desktop systems) `true` if yes, otherwise `false`.
- **\[APPRISE\]**: Various notification services (Pretty much anything you can think of).
  - `enable` - `true` if Apprise should be used, otherwise `false`'.
  - `service_uris` - Service-URIs. For more information please visit: [Apprise Documentation](https://github.com/caronc/apprise)
- **\[ADVANCED\]**: Settings for advanced users. It's gettting experimental 🤓
  - `cooldown_between_requests` - wait time between requests. A too small wait time leads to an IP ban (default: 1min, but can be decreased empirically)
  - `cooldown_between_failed_requests` - waiting time between failed attempts. For each additional one, the waiting time is added again to prevent an IP ban. I.e. five failures = waiting time of 5\*10s until the next request.
  - `cooldown_after_ip_ban` - If a query fails 10 times the IP is probably banned. By default it will wait for 3h.
  - `cooldown_after_success` - Cooldown after an vaccination slot was found. By default it will wait 15min.
  - `jitter` - random time span from 0-jtter seconds which is added to the wait times (default: `5`)
  - `sleep_at_night` - Specifies if the bot should sleep at night (default: `true` since no events are published anyway)
  - `user_agent`- The user agent is passed in the header (default: `impfbot`)

##### Example Config:

```ini
[COMMON]
zip_code=42042
birthdate=23.06.1912

[EMAIL]
enable=true
sender=sender@server.de
user=username
password=xxxxxx
server=smtp.server.de
port=465
receivers=sender@server.de,guenni@server.de,frida@server.de

[TELEGRAM]
enable=true
token=TOKEN
chat_ids=123456789,987654321

[WEBBROWSER]
enable=true

[APPRISE]
enable=false
service_uris=discord://webhook_id/webhook_token,matrix://hostname

[ADVANCED]
cooldown_between_requests=60
cooldown_between_failed_requests=10
cooldown_after_ip_ban=10800
cooldown_after_success=900
jitter=5
sleep_at_night=true
user_agent=impfbot
```
## Miscellaneous

### 🙋 Feedback & problems setting up.

Write [here](https://github.com/sibalzer/impfbot/issues/5) or [twitter](https://twitter.com/datearl) me.

### ⭐ Sponsorship

The impfbot helped you and you want to contribute monetarily? Then donate at [this fundraiser to Doctors Without Borders](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz). (Yes, somewhat cribbed from [vaccipy](https://github.com/iamnotturner/vaccipy). But I liked the idea.)

### 🙏 Many thanks to:

- [paulypeter](https://github.com/paulypeter) - Telegram Integration, Config-GUI & more
