# Anleitung für Nutzung auf Android-Geräten

Termux ist eine App, die eine Linux-Umgebung inkl. Terminal emulator auf dem Adnroid-Smartphone zugänglich macht. Dort lässt sich u. a. `python` installieren. Die anschließende Einrichtung unterscheidet sich nicht von der unter Linux. E-Mails und Telegram-Benachrichtigungen können versendet werden, eine direkte Implementierung von Push-Nachrichten könnte ggf. noch implementiert werden.

## Voraussetzungen

- Termux https://termux.com/
- ggf. PC mit `ssh`-Client für einfachere Einrichtung

## Anleitung

1. [Termux](https://termux.com/) über [f-droid](https://f-droid.org/en/packages/com.termux/) installieren (ggf. apk von dort runterladen). [Installation über Playstore macht Probleme](https://github.com/termux/termux-packages/issues/6726)

2. Termux-Umgebung vorbereiten:
```
pkg upgrade
pkg install python
termux-setup-storage
```
Der letzte Befehl ermöglicht (wenn ihr dem Dateizugriff zustimmt) den Dateiaustausch mit gewissen Directories des Smartphones. So könnt ihr die `config.ini` auf dem Rechner ausfüllen bzw. die dort bereits funktionierende kopieren.

3. Den Bot runterladen und entpacken:
```
curl -L https://api.github.com/repos/sibalzer/impfbot/tarball -o impfbot.tar.gz
mkdir impfbot && cd impfbot
tar xf ../impfbot.tar.gz --strip-components 1
```

4. config.ini kopieren (unter der Annahme, dass sie im Android-Download-Ordner liegt)
```
cp ../storage/downloads/config.ini .
```

5. Bot starten (installiert beim ersten Mal die benötigten Pakete)
```
./linux_start.sh
```

6. Einstellungen (Mailversand, Telegram) testen kann man ggf. mit
```
./linux_validate.sh
```

## mögliche Probleme

- Die Energiesparfunktionen könnten ggf. Termux beenden. Infos für dein Gerät ggf. hier lesen: https://dontkillmyapp.com/

Die Benachrichtung von Termux selbst hat bei mir den Knopf "Acquire wakelock". Das allein reicht aber nicht, die App wurde irgendwann beendet (ohne Deaktivierung anderer Energiesparfunktionen)

- wenn du dich durch Funklöcher bewegst und das Impfportal nicht erreichbar ist, denkt der Bot, dass du einem IP-Ban unterliegst und wartet (bei den Standardeinstellungen)


## weitere Ideen

wenn du in Termux  `ssh` installierst kannst du (als Server oder Client) mit  `scp` das Directory vom PC einfach komplett rüberkopieren

man könnte in den Impfbot noch direkte Push-Nachrichten über die Termux:API integrieren
