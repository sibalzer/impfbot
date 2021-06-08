# Anleitung für Nutzung auf Android-Geräten

Termux ist eine App, die eine Linux-Umgebung inkl. Terminal emulator auf dem Smartphone zugänglich macht. Dort lässt sich u. a. python installieren. Die anschließende Einrichtung unterscheidet sich nicht von der unter Linux. E-Mails und Telegram-Benachrichtigungen können versendet werden, eine direkte Implementierung von Push-Nachrichten könnte ggf. noch implementiert werden.

## Voraussetzungen

- Termux https://termux.com/
- ggf. PC mit ssh-Client für einfachere Einrichtung

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
curl -L https://github.com/sibalzer/impfbot/archive/refs/tags/v2.0.0.tar.gz -o impfbot.tar.gz
tar -zxvf impfbot.tar.gz
```
4. config.ini kopieren (unter der Annahme, dass sie im Android-Download-Ordner liegt)
```
cd impfbot-2.0.0
cp ../storage/downloads/config.ini .
```
5. Bot starten (installiert beim ersten Mal die benötigten Pakete)
```
./linux_start.sh
```
6. Einstellungen testen kann man ggf. mit
```
python src/test_email.py
python src/test_telegram.py
```

## mögliche Probleme

Die Energiesparfunktionen könnten ggf. Termux beenden. Infos für dein Gerät ggf. hier lesen: https://dontkillmyapp.com/
Die Benachrichtung von Termux selbst hat bei mir den Knopf "Acquire wakelock". Das allein reicht aber nicht, die App wurde irgendwann beendet (ohne Deaktivierung anderer Energiesparfunktionen)
