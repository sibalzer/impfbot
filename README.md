# Benachrichtigungs-Bot für das niedersächische Impfportal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![codecov](https://codecov.io/gh/sibalzer/impfbot/branch/main/graph/badge.svg?token=XXI3N5A9X1)](https://codecov.io/gh/sibalzer/impfbot)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

_English version [here](https://github.com/sibalzer/impfbot/blob/main/README.en.md)._

Ein kleines Wochenend-Projekt von mir. Der Bot überwacht die REST-API des niedersächsischen Impfportals (https://impfportal-niedersachsen.de) auf freie Impfslots und sendet eine Benachrichtigung mit deinem bevorzugtem Service. Ab da gilt leider: der Schnellste gewinnt. Bitte missbraucht den Bot nicht und verwendet moderate Intervalle.

## 🤖 Features

- Automatisches Suchen von kurzfristigen Impfterminen
- Benachrichtigungen über E-Mail, Telegram und vielen anderen Services
- Öffnet deinen Browser automatisch wenn ein Termin gefunden wurde. Du musst nur noch deine Daten eingeben!
- Einfaches Einrichten mit


> Was der impfbot nicht macht: Dem Termin für dich reservieren und/oder deine Daten automatisch eingeben.

## ⚙️ Setup

### Voraussetzungen

- Python 3.x von hier [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 📝 Anleitung - Schritt für Schritt

Am Beispiel von Windows:

1. Python von hier runderladen und installieren: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Den Bot runterladen (Rechts bei den Releases oder [hier](https://github.com/sibalzer/impfbot/releases/latest))
3. Das Archiv (Die Zip-Datei) entpacken
4. `config.example.ini` nach `config.ini` umbennen und deine Daten eintragen (PLZ, Geburtstag, Email-Server-Daten
5. Doppelklick auf `windows_validate.bat`, um die Einstellungen zu prüfen
6. Doppelklick auf `windows_start.bat`

Für Fortgeschrittene steht alternativ auch ein Docker-Container zur Verfügung. Siehe dazu [docker](https://github.com/sibalzer/impfbot/tree/main/docker). Das Validieren der Config funktioniert über den Befehl `docker exec impfbot python src/validate_config.py -a`.

### 📣 Einrichten von Telegram

1. https://t.me/BotFather anschreiben und Bot erstellen. Den Token dann in die `config.ini` kopieren.

Folgende Schritte muss für jeden ausgeführt werden, der Nachrichten empfangen will

2. https://t.me/userinfobot anschreiben und "Id"-Nummer in die `config.ini` kopieren (mehrere Nummern mit `,` getrennt).
3. ⚠ Mit dem eigenen Bot muss vorher eine Konversation begonnen werden! (URL steht in der Botfather-Nachricht, dort /start drücken) ⚠
4. Validieren, dass auch alles funktioniert: Doppelklick auf `test_telegram.bat`


### 🛠️ config.ini Parameter

> Deine Daten werden nur lokal gespeichert!

- **\[COMMON\]**: Allgemeine Einstellungen
  - `birthdate` - Dein Geburtstag - Da die Verteilung vom Alter abhängig ist, ist dieser zwingend notwendig. Beispiel: `23.06.1912`
  - `group_size` - Gruppengröße - Wenn du lieber einen Gruppentermin suchen möchtest musst du birthdate auskommentieren und eine Gruppengröße angeben (zwischen 2 und 15). Es darf nur eins von beiden in der Config sein! Beispiel: `5`
  - `zip_code` - Fünfstellige PLZ für das Impfzentrum, das der Bot überwachen soll. Beispiel: `49123`
- **\[EMAIL\]**: E-Mail-Einstellungen
  - `enable` - Legt fest, ob E-Mails versendet werden sollen. `true` wenn ja, sonst `false`.
  - `sender` - Die E-Mail-Adresse, von der die Benachrichtigungen versendet werden sollen. Beispiel: `sender@server.tld`
  - `user` - Login Name für den SMTP-Server (in den meisten Fällen identisch mit der Absender Adresse)
  - `password` - Das Passwort für die Absender-E-Mail-Adresse.
  - `server` - Der SMTP-Server. Beispiel: `smtp.server.tld`
  - `port` - Der Port für den SMTP-Server. Beispiel: `465`
  - `receivers` - E-Mail Empfänger Liste - Trag hier auch deine Absender-Adresse ein, wenn du selber Mails empfangen möchtest (Mit Kommata getrennt). Beispiel: `sender@server.tld,foo@server.tld,hoo@server.tld` oder (nur an sich selbst) `sender@server.tld`
- **\[TELEGRAM\]**:Telegram-Einstellungen
  - `enable` - Legt fest, ob Telegram-Nachrichten versendet werden sollen. `true` wenn ja, sonst `false`.
  - `token` - Bot-Token - Dieser zunächst beim BotFather generiert werden: [https://t.me/BotFather](https://t.me/BotFather)
  - `chat_ids` - User-IDs der Empfänger - Die bekommst du am einfachsten wenn du den User-Info-Bot anschreibst https://t.me/userinfobot. Da bekommst du eine Id, die hier eingetragen werden muss. Mehrere Id's durch Kommata trennen.
- **\[WEBBROWSER\]**: Webbrowser-Einstellungen
  - `enable` - Legt fest, ob der Browser automatisch geöffnet werden soll. (Nur auf Desktop-Systemen) `true` wenn ja, sonst `false`.
- **\[APPRISE\]** Verschiedene Benachrichtigungsservices (So ziemlich alles was man sich vorstellen kann).
  - `enable` - 'true' wenn Apprise verwendet werden soll, sonst 'false'
  - `service_uris` - Service URIs. Für mehr Informationen: [Apprise Documentation](https://github.com/caronc/apprise) (Mehrere URIs durch Kommata trennen)
- **\[ADVANCED\]**: Einstellungen für Fortgeschrittene, hier wird's experimentell
  - `cooldown_between_requests` - Wartezeit zwischen den Abfragen; Eine zu kleine Wartezeit führt zu einem IP-Ban (Default: 1 min, kann aber empirisch verkleinert werden)
  - `cooldown_between_failed_requests` - Wartezeit zwischen fehlgeschlagenen Versuchen. Bei jedem weiteren wird die Wartezeit nochmal hinzuaddiert, um einen IP Ban zu verhindern. D.h. fünf Fehlschläge = Wartezeit von 5\*15s bis zum nächsen Aufruf
  - `cooldown_after_ip_ban` - Wenn eine Abfrage 10x fehlschlaegt, ist die IP vermutlich gebannt. Standardmaeßig wird dann 3 h gewartet.
  - `cooldown_after_success` - Cooldown, nachdem ein Impftermin gefunden wurde. Standardmaeßig wird dann 15 min gewartet (in Sekunden)
  - `jitter` - Zufällige Zeitspanne von 0-jtter Sekunden, die auf die Wartezeiten addiert wird (Default: `5`)
  - `sleep_at_night` - Legt fest, ob der Bot nachts schlafen soll (Default: `true`, da eh keine Termine veröffentlicht werden)
  - `user_agent`- Der User Agent, der im Header übermittelt wird (Default: `impfbot`)


Beispiel Config:

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

## Sonstiges

## 🙋 Feedback & Probleme beim Einrichten

Schreib [hier](https://github.com/sibalzer/impfbot/issues/5) oder [twitter](https://twitter.com/datearl) mich an.

### ⭐ Sponsoring

Dir hat der impfbot geholfen und du möchtest monetär etwas beitragen? Dann spende doch unter [dieser Spendenaktion an Ärzte ohne Grenzen](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz). (Ja, etwas abgekupfert von [vaccipy](https://github.com/iamnotturner/vaccipy). Aber ich fand die Idee gut.)

### 🙏 Vielen Dank an:

- [paulypeter](https://github.com/paulypeter) - Telegram Integration & mehr
