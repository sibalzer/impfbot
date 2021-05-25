# Benachrichtigungs-Bot für das niedersächische Impfportal 🐴

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sibalzer/impfbot?label=version)
[![Python](https://img.shields.io/badge/Made%20with-Python%203.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/sibalzer/impfbot)](https://github.com/sibalzer/impfbot/blob/main/LICENSE)
![GitHub all releases](https://img.shields.io/github/downloads/sibalzer/impfbot/total)

Ein kleines Wochenend-Projekt von mir. Der Bot überwacht die REST-API des niedersächsischen Impfportals (https://impfportal-niedersachsen.de) auf freie Impfslots und sendet eine Benachrichtigung via Mail. Ab da gilt leider der Schnellste gewinnt. Bitte missbraucht den Bot nicht und verwendet moderate Intervalle. Ansonsten werdet ihr sowieso IP gebannt.

> ### ⚠ Hilfe gesucht! (Zeiten und Shadowbans/IP-Bans)
> Derzeit fragt der Bot alle 5min die API ab ich würde das gerne etwas optmieren brauche dafür aber Hilfe poste dazu deine Settings [hier](https://github.com/sibalzer/impfbot/issues/6)

## Setup
### Voraussetzungen
  - python 3.x mit py-Launcher via https://www.python.org/downloads/
### Einrichtung
Per git clone oder [ZIP-Download](https://github.com/sibalzer/impfbot/archive/refs/heads/main.zip) herunterladen. Die config.ini.example in config.ini umbenennen und anpassen. Dann kann der Bot auch schon via ```windows_start.bat``` oder ```linux_start.sh``` gestartet werden.
Für Fortgeschrittene steht alternativ auch ein Docker-Container zur Verfügung. Siehe dazu [docker](https://github.com/sibalzer/impfbot/tree/main/docker).

## Support & Contributing 

### Feedback & Probleme bei einrichten
Schreib mir [hier](https://github.com/sibalzer/impfbot/issues/5) in oder twitter mich an [twitter](https://twitter.com/datearl)

### Feature Requests
Eröffne ein Issue unter [issues](https://github.com/sibalzer/impfbot/issues/new/choose)

### Pull Request
Du möchtest mithelfen? Super! Aktuell gibt es nur E-Mail Benachrichtigungen, aber auch Benachrichtigungen via telegram o.ä. wären toll. Gehe dazu wie folgt vor:
  1. Füge den Service unter ```altets.py``` - ```alert(msg)``` hinzu
  2. Vervollständige benötigte Einstellungen unter ```settings.py``` und ```config.ini.example```
  3. Erstelle einen Pull Request & fertig

## Sonstiges
Ich war mir nicht ganz sicher, ob man solch einen Bot schreiben und veröffentlichen soll, aufgrund der aktuellen Lage habe ich mich doch dazu entschieden. Es werden täglich kurzfristig freigewordene Impfdosen über das Impfportal (je nach Impfzentrum stündlich) zu Verfügung gestellt, aber an einer "Spontan"-Warteliste mangelt es. D.h. entwender man campiert tagelang auf der Seite des Impfportals (für Arbeitnehmer btw nicht möglich), bis die F5 Taste den Geist aufgibt oder man nutzt einen Bot wie diesen hier.

## TODO
 - Englische Beschreibung
 - Ein ausführliches Tutorial für nicht technikaffine Menschen
