# Benachrichtigungs-Bot für das niedersächische Impfportal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)

Ein kleines Wochenend-Projekt von mir. Der Bot überwacht die REST-API des niedersächsischen Impfportals (https://impfportal-niedersachsen.de) auf freie Impfslots und sendet eine Benachrichtigung via Mail. Ab da gilt leider der Schnellste gewinnt. Bitte missbraucht den Bot nicht und verwendet moderate Intervalle. Ansonsten werdet ihr sowieso IP gebannt.

> ### ⚠ Hilfe gesucht! (Zeiten und Shadowbans/IP-Bans)
>
> Derzeit fragt der Bot alle 5min die API ab ich würde das gerne etwas optmieren brauche dafür aber Hilfe poste dazu deine Settings [hier](https://github.com/sibalzer/impfbot/issues/6)

## Setup 🤖

### Voraussetzungen

- python 3.x mit py-Launcher via https://www.python.org/downloads/

### Schritt für Schritt 📝

1. Python von hier laden und installieren: https://www.python.org/downloads/
2. Den Bot runterladen (Rechts oben der grüne Button und da ZIP-Archiv oder [hier](https://github.com/sibalzer/impfbot/archive/refs/heads/main.zip))
3. Das Archiv (Die Zip Datei) entpacken
4. `config.ini.example` nach `config.ini` umbennen und deine Daten eintragen (PLZ, Geburtstag, Email Server Daten
5. Doppelklick auf `test_mail.bat` um die E-Mail Einstellungen zu prüfen
6. Doppelklick auf `windows_start.bat`

Für Fortgeschrittene steht alternativ auch ein Docker-Container zur Verfügung. Siehe dazu [docker](https://github.com/sibalzer/impfbot/tree/main/docker).

### Einrichten von Telegram 📣

1. https://t.me/BotFather anschreiben und Bot erstellen. Den Token dann in die `config.ini` kopieren.
Folgene Schritte muss für jeden ausgeführt werden, der Nachrichten
2. https://t.me/userinfobot anschreiben und "Id"-Nummer in die `config.ini` kopieren (mit ```.``` getrennt).
3. Wichtig! Mit dem eigenen Bot muss vorher eine Konversation begonnen werden! (Url steht in der Bothfather Nachricht und dann start drücken)
4. Fertig

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

Dir hat der impfbot geholfen und du möchtest monetär etwas beitragen? Dann spende doch unter [dieser Spendenaktion an Ärzte ohne Grenzen](https://www.aerzte-ohne-grenzen.de/spenden-sammeln?cfd=z1suz).
