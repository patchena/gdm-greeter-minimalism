# Benachrichtigungen im Greeter deaktivieren

## Zielzustand

- Der GDM-Login-Modus zeigt keine Benachrichtigungen.
- Der Unlock-Modus zeigt keine Benachrichtigungen.
- Der normale Desktop-Modus zeigt weiterhin Benachrichtigungen.
- Die installierte Verifikation prüft alle drei Moduswerte im geladenen GResource.
- Das Debian-Paket wird als Version `1.0.1` erzeugt und ohne GDM-Neustart installiert.
- Die laufende GNOME-Shell-Sitzung bleibt während Installation und Verifikation unverändert aktiv.

## Ausführung

1. `sessionMode.js` für `gdm` und `unlock-dialog` auf `hasNotifications: false` setzen.
2. Die Overlay-Verifikation um die modusspezifischen Benachrichtigungswerte erweitern.
3. Paketmetadaten und Zieldokumentation auf Version `1.0.1` aktualisieren.
4. Release `v1.0.1` bauen und Paketinhalt prüfen.
5. Paket ohne GDM-Neustart installieren.
6. Paketversion, aktives Overlay, GResource-Werte und GNOME-Shell-PID prüfen.
