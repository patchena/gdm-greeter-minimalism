# Zurück-Button am Benutzernamen korrigieren

## Zielzustand

- Beim Eingeben des Benutzernamens ist der runde Zurück-Button links neben dem Eingabefeld unsichtbar, nicht reaktiv und nicht fokussierbar.
- Beim Eingeben des Passworts ist der Zurück-Button sichtbar, reaktiv und fokussierbar.
- Der reservierte Button-Slot bleibt erhalten, damit die zentrierte Position des Eingabefelds stabil bleibt.
- Die Zustandsaktualisierung bleibt nach GNOME-Shell-Resets und beim Wechsel vom Benutzernamen zum Passwort wirksam.
- Die Overlay-Validierung prüft die Sichtbarkeit des Buttons anhand des aktiven Eingabefelds.
- Release `1.0.2` wird als Debian-Paket gebaut und installiert.
- Installation und Verifikation starten weder GDM noch `gnome-shell` neu und beenden keinen laufenden `gnome-shell`-Prozess.

## Ausführung

1. `loginDialog.js` so anpassen, dass der Zurück-Button nur beim aktiven Passwortfeld sichtbar und interaktiv ist.
2. Die Zustandsaktualisierung beim Anzeigen eines Authentifizierungs-Prompts und beim manuellen Benutzernamen-Prompt sicherstellen.
3. Overlay-Prüfungen, Paketmetadaten, Changelog und Zieldokumentation auf Release `1.0.2` aktualisieren.
4. Shell-Skript syntaktisch prüfen und Release `v1.0.2` bauen.
5. Paketinhalt und Versionsdaten prüfen.
6. Das DEB ohne GDM-Neustart installieren.
7. Installierte Overlay-Quellen, GResource-Lookups, Paketstatus und unveränderte `gnome-shell`-PID validieren.
