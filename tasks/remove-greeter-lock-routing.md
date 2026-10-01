# Greeter-Sperrumleitung nach Lockscreen-Abnahme entfernen

## Umfang und Ausführungsgrenze

- Dieses AP definiert die spätere Bereinigung; seine Erstellung, nicht seine Ausführung oder Installation, ist freigegeben.
- Abhängigkeit: `../gnome-lockscreen-minimalism/tasks/minimal-lockscreen.md` muss einen regulär installierten, paketvalidierten und physisch abgenommenen lokalen Lockscreen liefern.
- Bis dahin bleibt die bestehende Greeter-Sperrumleitung unverändert aktiv. Ein Quellstand, Paketbau oder sichtbares Eingabefeld allein erfüllt die Übergabebedingung nicht.
- GDM-Minimalism behält ausschließlich die reduzierte Anmeldeoberfläche und deren unabhängige Aktualisierung. Security-Chain-Authentifizierung, Autologin und produktive Sitzungen bleiben erhalten.

## Zielzustand

- Super+L führt über GNOMEs regulären Sperrpfad zum lokalen Lockscreen, nicht über `gdm-greeter-minimalism lock` zum Greeter.
- Shell-Sperraktion, D-Bus-Sperre und Suspend erreichen ebenfalls den lokalen Lockscreen. Das Entfernen nur der eigenen Shortcut-Belegung genügt nicht.
- Benutzerwechsel und Initialanmeldung bleiben GDM-Aufgaben; authentifizierte Entsperrung der lokalen Sitzung bleibt dem neuen Lockscreen vorbehalten.
- GDM-Minimalism installiert keine lokale Greeter-Wechselkoordination, keinen authentifizierungsfreien Benutzer-Schutz-Actor und keine Umleitung von ScreenShield oder ScreenSaver mehr.
- Apply, Refresh, Pakettrigger, Verifikation und Restore reaktivieren weder den alten Shortcut noch die entfernten Sperrumleitungen.
- Greeter-Hintergrund, Theme, Feldgröße, Zentrierung, Skalierung, Benutzername-/Passwortablauf, fehlende Avatare, Benachrichtigungen und Systemtöne bleiben unverändert.
- Gemeinsame AuthPrompt-/PAM-Erweiterung bleibt optional und funktionsfähig. Keine neue Faktorlogik oder Abhängigkeit von Security Chain.

## Übergabe und Bereinigung

1. Aktuelle Paketstände, aktive und geladene Ressourcen, Super+L-Belegungen, Shortcut-Backups, globale Shell-/GDM-Drop-ins und Erweiterungskomposition prüfen.
2. Mit dem Lockscreen-Projekt Ressourcenbesitz und reguläre DEB-Übergangsfolge festlegen. Noch geladene alte Shells und partielle dpkg-Zustände ausdrücklich berücksichtigen; keine ungeschützte oder nicht authentifizierbare Zwischenkonfiguration zulassen.
3. Vor produktiver Übergabe die lokale Passwort- und gegebenenfalls Stickentsperrung, manuelle Namenseingabe ohne Kontodarstellung sowie Sperr-/Suspend-Schutz nachweisen. Betreiber lädt Ressourcen und führt physische Aktionen aus.
4. Ausschließlich die eigene Super+L-Umleitung und erforderliche eigene Backup-/Shortcut-Einträge kontrolliert zurücknehmen. Fremde und zwischenzeitlich geänderte Belegungen erhalten; Konflikte sichtbar melden. Keine erfundenen Ursprungswerte und kein `disable-lock-screen=true`.
5. Lokale Overrides für `screenShield.js`, `shellDBus.js`, `unlockDialog.js` und Sperraktionen in `systemActions.js` entsprechend dem geprüften Ressourcenbesitz entfernen. Legitimen Benutzerwechsel und Greeter-Funktionen erhalten.
6. Globale Benutzer-Shell-Startintegration nur entfernen oder übergeben, wenn der installierte Lockscreen sie nachweislich korrekt übernimmt. GDM-Daemon-/Greeter-Startintegration und gemeinsame AuthPrompt-Komposition erhalten. Beide Publisher dürfen sich nicht überschreiben.
7. Entfallene Befehle, Shortcut-Verwaltung, Zustände und Prüfer vollständig aus Apply, Refresh, Triggern, Verify, Restore und Paketierung entfernen; keine unbeabsichtigte Reaktivierung beim nächsten Update.
8. Dokumentation, Manpage und Versionsmetadaten abgleichen. Neue konventionelle `.deb` bauen, unabhängig prüfen, nach Freigabe installieren und am installierten Stand validieren.

## Validierung und Lieferung

- Normale unabhängige Prüfung: Sol 6.1 high; Umsetzung: Sol 6.1 medium; Sicherheits-/Übergangsfälle: Astra 6 high; abschließend Astra 6 xhigh erst nach fundfreien normalen Prüfungen.
- Reale isolierte Komposition und Paket-Lebenszyklen mit beiden Projekten sowie optionaler Security-Chain-Erweiterung prüfen. Unbekannte Ressourcen oder fehlende Authentifizierung verhindern Aktivierung.
- Installierte Nutzdateien, Paketintegrität, GDM-/Benutzerressourcen und Shortcut-Zustand gegen die gebundenen Artefakte prüfen. Keine Quellskriptinstallation.
- Super+L und alle übrigen Sperreinstiege erreichen den neuen Lockscreen; bewusste Stick- und Passwortentsperrung bleiben funktionsfähig. Wiederholungen, Suspend/Resume, Reset, Abbruch und geschützter VT-Rückwechsel sind physisch geprüft.
- Paket-Refreshes und GNOME-Updates erzeugen keine alte Umleitung. Laufende Sitzungen werden nicht automatisch beendet; notwendiges Neuladen erfolgt durch den Betreiber.
- GDM-Anmeldung, Autologin, Greeter-Design, Boot-Unlock, Schlüssel, LUKS-Slots, Stickdaten und Fremdkonfiguration bleiben unverändert.
- Vor jedem gesondert freigegebenen Commit vollständige Projektdokumentation prüfen; `git add -A`, Commit und Push mit verifiziertem Remote-Stand. Keine Tags oder GitHub-Releases ohne eigene Freigabe.
