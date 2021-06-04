# Benachrichtigungs-Bot für das niedersächische Impfportal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

English version [here](https://github.com/sibalzer/impfbot#notification-bot-for-the-lower-saxony-vaccination-portal-).

Ein kleines Wochenend-Projekt von mir. Der Bot überwacht die REST-API des niedersächsischen Impfportals (https://impfportal-niedersachsen.de) auf freie Impfslots und sendet eine Benachrichtigung via Mail. Ab da gilt leider der Schnellste gewinnt. Bitte missbraucht den Bot nicht und verwendet moderate Intervalle.

> ### ⚠ Hilfe gesucht! (Zeiten und Shadowbans/IP-Bans)
>
> Derzeit fragt der Bot alle 2.5min die API ab. Ich würde das gerne etwas optmieren, brauche dafür aber Hilfe. Poste dazu deine Settings [hier](https://github.com/sibalzer/impfbot/issues/6)

## Features
* Automatisches Suchen von kurzfristigen Impfterminen
* Benachrichtigungen über E-Mail und Telegram 
* Öffnet deinen Browser automatisch, wenn ein Termin gefunden wurde. Du musst nur noch deine Daten eingeben!

> Was der impfbot nicht macht: Dem Termin für dich reservieren und/oder deine Daten automatisch eingeben.

## 🤖 Setup

### Voraussetzungen

- python 3.x mit py-Launcher via https://www.python.org/downloads/

### 📝 Anleitung

Am Beispiel von Windows:

1. Python von hier laden und installieren: https://www.python.org/downloads/
2. Den Bot runterladen (Rechts oben der grüne Button und da ZIP-Archiv oder [hier](https://github.com/sibalzer/impfbot/archive/refs/heads/main.zip))
3. Das Archiv (Die Zip Datei) entpacken
4. `config.ini.example` nach `config.ini` umbennen und deine Daten eintragen (PLZ, Geburtstag, Email Server Daten
5. Doppelklick auf `windows_validate.bat` um die Einstellungen zu prüfen
6. Doppelklick auf `windows_start.bat`

Für Fortgeschrittene steht alternativ auch ein Docker-Container zur Verfügung. Siehe dazu [docker](https://github.com/sibalzer/impfbot/tree/main/docker). Das Validieren der Config funktioniert über den Befehl `docker exec impfbot python src/validate_config.py -a`.

### Einrichten von Telegram 📣

1. https://t.me/BotFather anschreiben und Bot erstellen. Den Token dann in die `config.ini` kopieren.

Folgende Schritte muss für jeden ausgeführt werden, der Nachrichten empfangen will

2. https://t.me/userinfobot anschreiben und "Id"-Nummer in die `config.ini` kopieren (mit `,` getrennt).
3. ⚠ Mit dem eigenen Bot muss vorher eine Konversation begonnen werden! (Url steht in der Botfather Nachricht und dann start drücken) ⚠
4. Validieren das auch alles funktioniert: Doppelklick auf `test_telegram.bat`

### config.ini Parameter

> Deine Daten werden lokal gespeichert! Falls du das selber überprüfen willst geht das am einfachsten über die Suche, da bekommst du alle Codezeilen in die bspw. dein Passwort genutzt wird. Bsp.: Passwort https://github.com/sibalzer/impfbot/search?q=password

- **\[COMMON\]**: Allgemeine Einstellungen
  - `geburtstag` - Geburtstag der Abgefragt werden soll. Beispiel: `23.06.1912`
  - `postleitzahl` - Fünfstellige PLZ für das Impfzentrum, das der Bot überwachen soll. Beispiel: `49123`
- **\[EMAIL\]**: E-Mail-Einstellungen
  - `enable` - Legt fest ob E-Mails versendet werden sollen. `true` wenn ja, sonst `false`.
  - `sender` - Die E-Mail Adresse von der die Benachrichtigungen versendet werden sollen. Beispiel: `sender@server.tld`
  - `password` - Das Passwort für die Versender E-Mail Adresse. 
  - `server` - Der SMTP-Server. Beispiel: `smtp.server.tld`
  - `port` - Der Port für den SMTP-Server. Beispiel: `465`
  - `empfaenger` - Eine Liste der E-Mail Adressen an die eine Nachricht geschickt werden soll. Beispiel: `sender@server.tld,foo@server.tld,hoo@server.tld` oder (nur an sich selber) `sender@server.tld`
- **\[TELEGRAM\]**: Telegram-Einstellungen
  - `enable_telegram` - Legt fest ob Telegram Nachrichten versendet werden sollen. `true` wenn ja, sonst `false`.
  - `token` - Der Bot-Token von https://t.me/BotFather
  - `chat_id` - User-ID des Empfängers: nutze dazu https://t.me/userinfobot
- **\[WEBBROWSER\]**: Webbrowser-Einstellungen
  - `open_browser` - Legt fest ob der Browser automatisch geöffnet werden soll. (Nur auf Desktop-Systemen) `true` wenn ja, sonst `false`.
- **\[ADVANCED\]**: Einstellungen für Fortgeschrittene, hier wirds experimentell
  - `sleep_between_requests_in_s` - Wartezeit zwischen den Abfragen eine zu kleine Wartezeit führt zu einem IP-Ban (Default: 2.5min, kann aber empirisch verkleinert werden)
  - `sleep_between_failed_requests_in_s` - Wartezeit zwischen fehlgeschlagenen Versuchen. Bei jedem weiteren wird die Wartezeit nochmal hinzuaddiert, um einen IP Ban zu verhindern. D.h. fünf Fehlschläge = Wartezeit von 5*15s bis zum nächsen Aufruf
  - `sleep_after_ipban_in_min` - Wenn eine Abfrage 10x fehlschlaegt ist die IP vermutlich gebannt. Standardmaeßig wird dann 3h gewartet.
  - `cooldown_after_found_in_min` - Cooldown nachdem ein Impftermin gefunden wurde. Standardmaeßig wird dann 15min gewartet (in min)
  - `jitter` - Zufällige Zeitspanne von 0-jtter Sekunden die auf die Wartezeiten addiert wird (Default: `10`)
  - `sleep_at_night` - Legt fest ob der Bot nachts schlafen soll (Default: `true` da eh keine Termine veröffentlicht werden)
  - `user_agent`- Der User Agent im Header übermittel wird (Default: `impfbot`)

Beispiel Config:

```ini
[COMMON]
geburtstag=23.06.1912
postleitzahl=49049

[EMAIL]
enable=true
sender=beispielsender@server.tld
password=xxxxxxxxxx
server=smtp.server.de
port=465
empfaenger=beispielsender@server.tld,beispielsmfaenger@server.tld

[TELEGRAM]
enable_telegram=true
token=xxxxxxxxxx
chat_id=01234586789,9876543210

[WEBBROWSER]
open_browser=true

[ADVANCED]
sleep_between_requests_in_s=123
sleep_between_failed_requests_in_s=12
sleep_after_ipban_in_min=180
cooldown_after_found_in_min=5
jitter=10
sleep_at_night=true
user_agent=impfbot
```

## Support & Contributing

### Feedback & Probleme bei einrichten

Schreib [hier](https://github.com/sibalzer/impfbot/issues/5) oder [twitter](https://twitter.com/datearl) mich an.

### Feature Requests

Eröffne ein [Issue](https://github.com/sibalzer/impfbot/issues/new/choose).

### Pull Request

Du möchtest mithelfen? Super! Aktuell gibt es nur E-Mail Benachrichtigungen, aber auch Benachrichtigungen via ~~telegram~~ o.ä. wären toll. Gehe dazu wie folgt vor:

1. Füge den Service unter `alerts.py` - `alert(msg)` hinzu
2. Vervollständige benötigte Einstellungen unter `settings.py` und `config.ini.example`
3. Erstelle einen Pull Request & fertig

#### Vielen Dank an:

- [paulypeter](https://github.com/paulypeter) - Telegram Integration

## Sponsoring

Dir hat der impfbot geholfen und du möchtest monetär etwas beitragen? Dann spende doch unter [dieser Spendenaktion an Ärzte ohne Grenzen](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz). (Ja, etwas abgekupfert von [vaccipy](https://github.com/iamnotturner/vaccipy). Aber ich fand die Idee gut.)

# Notification bot for the Lower Saxony vaccination portal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

A little weekend project of mine. The bot monitors the REST-API of the lower saxony vaccination portal (https://impfportal-niedersachsen.de) for free vaccination slots and sends a notification via mail. From then on, unfortunately, the fastest wins. Please do not abuse the bot and use moderate intervals.

> ### ⚠ Help wanted! (Times and Shadowbans/IP-Bans)
>
> Currently the bot queries the API every 2.5min. I would like to optimize this a bit but need help. Post your settings [here](https://github.com/sibalzer/impfbot/issues/6)

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

### config.ini parameter

> Your data will be saved locally! If you want to check this yourself, the easiest way is to search for all lines of code where your password is used. Example: password https://github.com/sibalzer/impfbot/search?q=password


- **\[COMMON\]**: General settings
  - `birthday` - birthday to be queried. Example: `23.06.1912`.
  - `postleitzahl` - five-digit zip code for your vaccination center. Example: `49123`
- **\[EMAIL\]**: Email settings
  - `enable` - Specifies whether emails should be sent. `true` if yes, `false` otherwise.
  - `sender` - The email address from which the notifications should be sent. Example: `sender@server.tld`.
  - `password` - The password for the sender email address. 
  - `server` - The SMTP-server. Example: `smtp.server.tld`.
  - `port` - The port for the SMTP server. Example: `465`.
  - `recipient` - A list of e-mail addresses to which a message should be sent. Example: `sender@server.tld,foo@server.tld,hoo@server.tld` or (only to itself) `sender@server.tld`.
- **\[TELEGRAM\]**: Telegram settings
  - `enable_telegram` - Specifies whether Telegram messages should be sent. `true` if yes, otherwise `false`.
  - `token` - The bot token from https://t.me/BotFather
  - `chat_id` - User-ID of the recipient: use https://t.me/userinfobot
- **\[WEBBROWSER\]**: Web browser settings
  - `open_browser` - Determines if the browser should be opened automatically. (Only on desktop systems) `true` if yes, otherwise `false`.
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
password=xxxxxxxx
server=smtp.server.com
port=465
empfaenger=beispielsender@server.tld,beispielsmfaenger@server.tld

[TELEGRAM]
enable_telegram=true
token=xxxxxxxx
chat_id=01234586789,9876543210

[WEBBROWSER]
open_browser=true

[ADVANCED]
sleep_between_requests_in_s=123
sleep_between_failed_requests_in_s=12
sleep_after_ipban_in_min=180
cooldown_after_found_in_min=5
jitter=10
sleep_at_night=true
user_agent=impfbot
```

## Support & Contributing

### Feedback & problems with setup

Write [here](https://github.com/sibalzer/impfbot/issues/5) or use [twitter](https://twitter.com/datearl).

### Feature Requests

Open an [issue](https://github.com/sibalzer/impfbot/issues/new/choose).

### Pull Request

Want to help out? Great! Currently there are only email notifications, but also notifications via ~~telegram~~ or similar would be great. Proceed as follows:

1. add the service under `alerts.py` - `alert(msg)`
2. complete needed settings under `settings.py` and `config.ini.example
3. create a pull request & done

#### Many thanks to:

- [paulypeter](https://github.com/paulypeter) - Telegram Integration

## Sponsorship

The impfbot helped you and you want to contribute monetarily? Then donate at [this fundraiser to Doctors Without Borders](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz). (Yes, somewhat cribbed from [vaccipy](https://github.com/iamnotturner/vaccipy). But I liked the idea.)