# Anleitung für das Aufsetzen des E-Mail-Versands bei verschiedenen Anbietern

Bei manchen Anbietern müssen zunächst bestimmte Einstellungen vorgenommen werden, um dem Bot den Zugriff zu erlauben. (Wenn ihr den Bot nicht mehr nutzt, einfach alles rückgängig machen 😉)

## GMail

1. Bei Gmail anmelden
2. Unter den [IMAP-Einstellungen](https://mail.google.com/mail/u/0/#settings/fwdandpop) IMAP aktivieren
3. Unter [Zugriff durch weniger sichere Apps](https://myaccount.google.com/lesssecureapps) weniger sichere Apps zulassen


### Beispiel-Config

```ini
[EMAIL]
enable=true
sender=meinemail@gmail.com
user=meinemail@gmail.com
password=xxxxxx
server=smtp.gmail.com
port=465
receivers=meinemail@gmail.com
```

## Web.de

1. Bei Webmail auf Einstellungen Gehen
2. Den Reiter POP3/IMAP Abruf auswählen
3. Unter "WEB.DE Mail über POP3 & IMAP" das Häkchen neben "POP3 und IMAP Zugriff erlauben" setzen
4. Speichern

Alternativ: Anleitung mit Video von Web.de gibt es [hier](https://hilfe.web.de/pop-imap/einschalten.html)

### Beispiel-Config

```ini
[EMAIL]
enable=true
sender=meinemail@web.de
user=meinemail@web.de
password=xxxxxx
server=smtp.web.de 
port=587
receivers=meinemail@web.de
```

## GMX

1. Bei E-Mail auf Einstellungen Gehen
2. Den Reiter POP3/IMAP Abruf auswählen
3. Unter "GMX Mail über POP3 & IMAP" das Häkchen neben "POP3 und IMAP Zugriff erlauben" setzen
4. Speichern

Alternativ: Anleitung mit Video von GMX gibt es [hier](https://hilfe.gmx.net/pop-imap/imap/outlook.html#textlink_help_pop-imap_imap_imap-serverdaten)

### Beispiel-Config

```ini
[EMAIL]
enable=true
sender=meinemail@gmx.net
user=meinemail@gmx.net
password=xxxxxx
server=mail.gmx.net  
port=587
receivers=meinemail@gmx.net
```
