# Greeter-Systemklänge deaktivieren

## Zielzustand

- Der GDM-Greeter verwendet keine Ereignis-, Eingabe-, System-Bell-, Lautstärke-, Netzteil- oder Akkuwarnklänge.
- Die Konfiguration gilt unabhängig von den Einstellungen eines Desktop-Benutzers.
- `apply` und Paket-Refreshes stellen den lautlosen Zustand wieder her.
- `verify` prüft Konfigurationsquellen, Klangthema und die wirksamen Werte des aktiven sowie des paketierten GDM-Profils.
- `restore` entfernt den projektverwalteten Sound-Block, die Sound-Sperren und das Klangthema und stellt ein angepasstes GDM-Profil aus seiner Sicherung wieder her.
- Der installierte Zustand wird vor Dokumentation und Release durch einen manuellen Greeter-Test bestätigt.
- Nach der Bestätigung werden Version, Changelog, README, Zieldokumentation und Manpage aktualisiert, das Release gebaut, installiert, geprüft, committet und gepusht.

## Ausführung

1. Einen markierten Sound-Block in `/etc/gdm3/greeter.dconf-defaults` verwalten.
2. `event-sounds`, `input-feedback-sounds` und `audible-bell` auf `false` sowie das Greeter-Klangthema setzen.
3. Ein Greeter-eigenes Klangthema mit deaktivierten direkten GNOME-Settings-Daemon-Ereignissen verwalten.
4. Ein vorhandenes namensaufgelöstes GDM-Profil gesichert auf die aktuelle Greeter-Datenbank ausrichten und diese über `generate-config` kompilieren.
5. Quellblock, Sperren, Klangthema und wirksame Werte im aktiven und paketierten GDM-Profil prüfen.
6. Den Entwicklungsstand anwenden und den manuellen Greeter-Test abwarten.
7. Nach Bestätigung Dokumentation und Release-Metadaten aktualisieren.
8. Vollständig reviewen, bauen, installieren und verifizieren.
9. Mit `git add -A` committen und nach `origin/main` pushen.
