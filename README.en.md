# Notification bot for the Lower Saxony vaccination portal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

A little weekend project of mine. The bot monitors the REST-API of the lower saxony vaccination portal (https://impfportal-niedersachsen.de) for free vaccination slots and sends a notification via mail. From then on, unfortunately, the fastest wins. Please do not abuse the bot and use moderate intervals.

> ### ⚠ Help wanted! (Times and Shadowbans/IP-Bans)
>
> Currently the bot queries the API every 2.5min I would like to optimize this a bit but need help post your settings [here](https://github.com/sibalzer/impfbot/issues/6)

## Features
* Automatic search for short term vaccination dates
* Notifications via email and telegram 
* Opens your browser automatically when an appointment is found. All you have to do is enter your details!

> What the impfbot doesn't do: Book the appointment for you and/or enter your data automatically.

## 🤖 Setup

### Requirements

- python 3.x with py launcher via https://www.python.org/downloads/

### 📝 Instructions

Using Windows as an example:

1. download and install python from here: https://www.python.org/downloads/
2. download the bot (top right green button and there ZIP archive or [here](https://github.com/sibalzer/impfbot/archive/refs/heads/main.zip))
3. unpack the archive (the zip file)
4. rename `config.ini.example` to `config.ini` and fill in your data (zip code, birthday, email server data)
5. double-click on `windows_validate.bat` to check the config file
6. double-click on `windows_start.bat`

For advanced users, a docker container is also available as an alternative. See [docker](https://github.com/sibalzer/impfbot/tree/main/docker) for more information. Validating the config works via the command `docker exec impfbot python src/validate_config.py -a`.

### Setting up Telegram 📣

1. write to https://t.me/BotFather and create bot. Then copy the token to `config.ini`.

The following steps must be performed for everyone who wants to receive messages.

2. write to https://t.me/userinfobot and copy "Id"-number into `config.ini` (separated with `,`)
3. ⚠ You have to start a conversation with your own bot before! (Url is in the bothfather message and then press start). ⚠
4. validate that everything works: Double click on `test_telegram.bat`

### config.ini parameters

> Your data will be saved locally! If you want to check this yourself, the easiest way is to search for all lines of code where your password is used. Example: password https://github.com/sibalzer/impfbot/search?q=password


- **\[COMMON\]**: General settings
  - `birthday` - birthday to be queried. Example: `23.06.1912`.
  - `gruppengroesse` - Size of the group for which an appointment is requested. Example: `5`
  - `postleitzahl` - five-digit zip code for your vaccination center. Example: `49123`
- **\[EMAIL\]**: Email settings
  - `enable` - Specifies whether emails should be sent. `true` if yes, `false` otherwise.
  - `sender` - The email address from which the notifications should be sent. Example: `sender@server.tld`.
  - `user` - The user name for the sender email address. 
  - `password` - The password for the sender email address. 
  - `server` - The SMTP server. Example: `smtp.server.tld`.
  - `port` - The port for the SMTP server. Example: `465`.
  - `recipient` - A list of e-mail addresses to which a message should be sent. Example: `sender@server.tld,foo@server.tld,hoo@server.tld` or (only to itself) `sender@server.tld`.
- **\[TELEGRAM\]**: Telegram settings
  - `enable` - Specifies whether Telegram messages should be sent. `true` if yes, otherwise `false`.
  - `token` - The bot token from https://t.me/BotFather
  - `chat_id` - User-ID of the recipient: use https://t.me/userinfobot
- **\[TELEGRAM\]**: Web browser settings
  - `enable` - Determines if the browser should be opened automatically. (Only on desktop systems) `true` if yes, otherwise `false`.
- **\[ADVANCED\]**: Settings for advanced users. it's gettting experimental 🤓
  - `sleep_between_requests_in_s` - wait time between requests. A too small wait time leads to an IP ban (default: 2.5min, but can be decreased empirically)
  - `sleep_between_failed_requests_in_s` - waiting time between failed attempts. For each additional one, the waiting time is added again to prevent an IP ban. I.e. five failures = waiting time of 5*15s until the next call.
  - `sleep_after_ipban_in_min` - If a query fails 10 times the IP is probably banned. By default it will wait for 3h.
  - `cooldown_after_found_in_min` - Cooldown after an vaccination slot was found. By default it will wait 15min (in min).
  - `jitter` - random time span from 0-jtter seconds which is added to the wait times (default: `10`)
  - `sleep_at_night` - Specifies if the bot should sleep at night (default: `true` since no events are published anyway)
  - `user_agent`- The user agent is passed in the header (default: `impfbot`)

Example Config:

```ini
[COMMON]
geburtstag=23.06.1912
postleitzahl=49049

[EMAIL]
enable=true
sender=beispielsender@server.tld
user=xxxxxxxx
password=xxxxxxxx
server=smtp.server.com
port=465
empfaenger=beispielsender@server.tld,beispielsmfaenger@server.tld

[TELEGRAM]
enable=true
token=xxxxxxxx
chat_id=01234586789,9876543210

[WEBBROWSER]
open=true

[ADVANCED]
sleep_between_requests_in_s=123
sleep_between_failed_requests_in_s=12
sleep_after_ipban_in_min=180
cooldown_after_found_in_min=5
jitter=10
sleep_at_night=true
user_agent=impfbot
```

