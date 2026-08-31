# Rekursive Greeter-Erzeugung beim Suspend korrigieren

## Zielzustand

- Sperren und Suspend wechseln zu einer vorhandenen GDM-Anmeldesitzung.
- Nur wenn keine Anmeldesitzung existiert, darf GDM eine neue erzeugen.
- GDM-Greeter-Sitzungen lösen keinen weiteren Greeter-Wechsel aus.
- Der Suspend-Pfad verwendet GNOMEs regulären `lock(true)`-Ablauf.
- `Super+L`, Shell-Sperraktion und Suspend verwenden denselben idempotenten GDM-Pfad.
- Paket-Refreshes aktualisieren die verwaltete `Super+L`-Belegung.
- Alle GNOME-Shell-Instanzen laden das Overlay über das generische Template-Drop-in.
- Die Overlay-Prüfung lehnt direkte `CreateTransientDisplay`-Aufrufe ab.
- Bereits laufende Greeter-Sitzungen mit altem Code werden nach der Installation beendet.
- Release `1.0.3` wird gebaut, installiert und vollständig verifiziert.
- Installation und Verifikation starten GDM nicht neu und beenden keine Desktop-Benutzersitzung.

## Ausführung

1. Greeter-Wechsel auf `Gdm.goto_login_session_sync(null)` umstellen und im Greeter-Modus sperren.
2. Suspend wieder über `lock(true)` führen.
3. `Super+L` auf den idempotenten Paketbefehl umstellen und bei Refresh aktualisieren.
4. Validierung, Paketmetadaten, Changelog und Dokumentation auf Release `1.0.3` aktualisieren.
5. Shell-Syntax, statische Analyse, Paketbau und Paketinhalt prüfen.
6. Das DEB ohne GDM-Neustart installieren.
7. Verwaiste Greeter-Sitzungen mit geladenem Altcode gezielt beenden.
8. Installierte Quellen, Ressourcen, Paketstatus und Seiteneffekte verifizieren.
9. Änderungen vollständig reviewen, Findings korrigieren, committen und pushen.
