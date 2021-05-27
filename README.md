# Benachrichtigungs-Bot für das niedersächische Impfportal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

Ein kleines Wochenend-Projekt von mir. Der Bot überwacht die REST-API des niedersächsischen Impfportals (https://impfportal-niedersachsen.de) auf freie Impfslots und sendet eine Benachrichtigung via Mail. Ab da gilt leider der Schnellste gewinnt. Bitte missbraucht den Bot nicht und verwendet moderate Intervalle.

> ### ⚠ Hilfe gesucht! (Zeiten und Shadowbans/IP-Bans)
>
> Derzeit fragt der Bot alle 5min die API ab ich würde das gerne etwas optmieren brauche dafür aber Hilfe poste dazu deine Settings [hier](https://github.com/sibalzer/impfbot/issues/6)

## Features
* Automatisches Suchen von kurzfristigen Impfterminen
* Benachrichtigungen über E-Mail und Telegram 
* Öffnet deinen Browser automatisch wenn ein Termin gefunden wurde. Du musst nur noch deine Daten eingeben!

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

Für Fortgeschrittene steht alternativ auch ein Docker-Container zur Verfügung. Siehe dazu [docker](https://github.com/sibalzer/impfbot/tree/main/docker). Das validieren der Config funktioniert über den Befehl `docker exec impfbot python src/validate_config.py -a`.

### Einrichten von Telegram 📣

1. https://t.me/BotFather anschreiben und Bot erstellen. Den Token dann in die `config.ini` kopieren.

Folgende Schritte muss für jeden ausgeführt werden, der Nachrichten empfangen will

2. https://t.me/userinfobot anschreiben und "Id"-Nummer in die `config.ini` kopieren (mit `.` getrennt).
3. Wichtig! Mit dem eigenen Bot muss vorher eine Konversation begonnen werden! (Url steht in der Bothfather Nachricht und dann start drücken)
4. Validieren das auch alles funktioniert: Doppelklick auf `test_telegram.bat`

### config.ini Parameter

> Deine Daten werden lokal gespeichert! Falls du das selber überprüfen willst geht das am einfachsten über die Suche, da bekommst du alle Codezeilen in die bspw. dein Passwort genutzt wird. Bsp.: Passwort https://github.com/sibalzer/impfbot/search?q=password

- **\[COMMON\]**: Allgemeine Einstellungen
  - `geburtstag` - Geburtstag der Abgefragt werden soll. Beispiel: `23.6.1912`
  - `postleitzahl` - Fünfstellige PLZ für die Postleitzahl der Bot Benachrichtigungen schicken soll. Beispiel: `49123`
- **\[EMAIL\]**: E-Mail Einstellungen
  - `enable` - Legt fest ob E-Mails versendet werden sollen. `true` wenn ja, sonst `false`.
  - `sender` - Die E-Mail Adresse von der die Benachrichtigungen versendet werden sollen. Beispiel: `versender@server.tld`
  - `password` - Das Passwort für die Versender E-Mail Adresse. 
  - `server` - Beispiel: `smtp.server.tld`
  - `port` - Der Port für den SMTP-Server. Beispiel: `465`
  - `empfaenger` - Eine Liste der E-Mail Adressen an die eine Nachricht geschickt werden soll. Beispiel: `sender@server.de,foo@server.de,hoo@server.de` oder (nur an sich selber) `sender@server.de`
- **\[TELEGRAM\]**: Email Einstellungen
  - `enable_telegram` - Legt fest ob Telegram Nachrichten versendet werden sollen. `true` wenn ja, sonst `false`.
  - `token` - Der Bot-Token von https://t.me/BotFather
  - `chat_id` - User-ID des Empfängers: nutze dazu https://t.me/userinfobot
- **\[WEBBROWSER\]**: Webbrowser Einstellungen
  - `enable_telegram` - Legt fest ob der Browser automatisch geöffnet werden soll. (Nur auf Desktop-Systemen) `true` wenn ja, sonst `false`.
- **\[ADVANCED\]**: Einstellungen für fortgeschrittene hier wirds experimentell
  - `sleep_between_requests_in_s` - Wartezeit zwischen den Abfragen eine zu kleine Wartezeit führt zu einem IP-Ban (Default: 5min, kann aber empirisch verkleinert werden)
  - `sleep_between_failed_requests_in_s` - Wartezeit zwischen fehlgeschlagenen Versuchen. Bei jedem weiteren wird die Wartezeit nochmal hinzuaddiert, um einen IP Ban zu verhindern. D.h. fünf Fehlschläge = Wartezeit von 5\*30s bis zum nächsen Aufruf
  - `sleep_after_ipban_in_min` - Wenn eine Abfrage 10x fehlschlaegt ist die IP vermutlich gebannt. Standardmaeßig wird dann 3h gewartet.
  - `cooldown_after_found_in_min` - Cooldown nachdem ein Impftermin gefunden wurde. Standardmaeßig wird dann 15min gewartet (in min)
    cooldown_after_found_in_min=15
  - `jitter` - Zufällige Zeitspanne von 0-jtter Sekunden die auf die Wartezeiten addiert wird (Default: `15`)
  - `sleep_at_night` - Legt fest ob der Bot nachts schlafen soll (Default: `true` da eh keine Termine veröffentlicht werden)
  - `user_agent`- Der User Agent im Header übermittel wird (Default: `true`)

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

Eröffne ein Issue unter [issues](https://github.com/sibalzer/impfbot/issues/new/choose)

### Pull Request

Du möchtest mithelfen? Super! Aktuell gibt es nur E-Mail Benachrichtigungen, aber auch Benachrichtigungen via ~~telegram~~ o.ä. wären toll. Gehe dazu wie folgt vor:

1. Füge den Service unter `alerts.py` - `alert(msg)` hinzu
2. Vervollständige benötigte Einstellungen unter `settings.py` und `config.ini.example`
3. Erstelle einen Pull Request & fertig

#### Vielen Dank an:

- [paulypeter](https://github.com/paulypeter) - Telegram Integration

## TODO

- Englische Beschreibung
- Ein ausführliches Tutorial für nicht technikaffine Menschen

## Sponsoring

Dir hat der impfbot geholfen und du möchtest monetär etwas beitragen? Dann spende doch unter [dieser Spendenaktion an Ärzte ohne Grenzen](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz). (Ja, etwas abgekupfert von [vaccipy](https://github.com/iamnotturner/vaccipy). Aber ich fand die Idee gut.)
