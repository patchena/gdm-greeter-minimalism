# GDM Greeter Minimalism

## Zweck

`gdm-greeter-minimalism.sh` richtet den Ubuntu-GDM-Greeter als reduzierte Login-Oberfläche ein. Der Greeter zeigt keine GNOME-Shell-Bedienelemente, kein Panel, keine Quick-Settings, keinen Kalender, keine Barrierefreiheits-Schaltfläche und keinen Benutzeravatar. Benutzername und Passwort werden als zentrale Eingabefelder dargestellt.

## Bedienung

Das Skript kann ohne Argumente gestartet werden. Im interaktiven Modus wird eine Aktion per einzelner Taste gewählt; `Enter` ist nicht nötig.

```bash
./scripts/gdm-greeter-minimalism.sh
```

Verfügbare Aktionen:

- `1` oder `a`: Greeter-Minimalismus anwenden
- `2` oder `p`: Installation prüfen
- `3` oder `w`: Originalzustand wiederherstellen
- `4` oder `q`: abbrechen

Für `apply` und `restore` startet sich das Skript bei Bedarf automatisch über `sudo` neu. Danach wird optional abgefragt, ob `gdm` direkt neu gestartet werden soll.

Der nichtinteraktive Modus bleibt verfügbar:

```bash
./scripts/gdm-greeter-minimalism.sh apply
./scripts/gdm-greeter-minimalism.sh verify
./scripts/gdm-greeter-minimalism.sh restore
./scripts/gdm-greeter-minimalism.sh apply --restart
./scripts/gdm-greeter-minimalism.sh restore --restart
```

## Ausgabe

Die Ausgabe nutzt ANSI-Farben auf TTYs. Schritte werden mit `=>` ausgegeben, erfolgreiche Endzustände mit `OK`, Fehler rot und fett. Wenn `NO_COLOR` gesetzt ist, werden keine ANSI-Codes verwendet.

Erfolgreiche `dbus-run-session`- und `gjs`-Diagnoseausgaben werden ausgeblendet. Bei Fehlern wird die abgefangene Originalausgabe auf `stderr` geschrieben.

## Voraussetzungen

Benötigte Programme:

- `bash`
- `chown`
- `dbus-run-session`
- `dconf`
- `flock`
- `gdbus`
- `getent`
- `gjs`
- `gresource`
- `gsettings`
- `install`
- `localectl`
- `python3`
- `readlink`
- `runuser`
- `systemctl`

Benötigte Systemdateien:

- `/etc/gdm3/greeter.dconf-defaults`
- `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`
- eine installierte GNOME-Shell-Ressource `libshell-*.so`
- ein aktives GDM-Theme unter `/usr/share/gnome-shell/gdm-theme.gresource` oder `/usr/share/gnome-shell/gdm3-theme.gresource`

Für die Migration eines aktiven Legacy-CSS-Overrides wird zusätzlich das Python-Modul `gdms` benötigt.

## Systemdateien

Das Skript verwaltet folgende Dateien und Verzeichnisse:

- Overlay-Verzeichnis: `/usr/local/share/gnome-shell-overrides/greeter-controls`
- User-Shell-Drop-in: `/etc/systemd/user/org.gnome.Shell@wayland.service.d/90-disable-greeter-controls.conf`
- GDM-Service-Drop-in: `/etc/systemd/system/gdm.service.d/90-disable-greeter-controls.conf`
- GDM-User-Drop-in: `<gdm-home>/.config/systemd/user/org.gnome.Shell@wayland.service.d/90-disable-greeter-controls.conf`
- Greeter-dconf-Datei: `/etc/gdm3/greeter.dconf-defaults`
- Greeter-Desktop-Datei: `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`

State-Dateien:

- `/etc/gdm3/.ggm-gdm-input-sources.state`
- `/etc/gdm3/.ggm-gdm-background.state`
- `/etc/gdm3/.ggm-gdm-accent.state`
- `/etc/gdm3/.ggm-user-shortcut.state`
- `/etc/gdm3/.ggm-greeter-desktop.state`

## GResource-Overlay

Das Overlay wird über `G_RESOURCE_OVERLAYS=/org/gnome/shell=/usr/local/share/gnome-shell-overrides/greeter-controls` geladen. Diese Umgebung wird in drei systemd-Drop-ins und zusätzlich in der Greeter-Desktop-Datei gesetzt.

Erzeugte Overlay-Dateien:

- `ui/sessionMode.js`
- `ui/panel.js`
- `misc/systemActions.js`
- `ui/screenShield.js`
- `ui/unlockDialog.js`
- `gdm/authPrompt.js`
- `gdm/loginDialog.js`
- `theme/gdm.css`
- `theme/source.env`

## Greeter-Oberfläche

`sessionMode.js` setzt im `gdm`- und `unlock-dialog`-Modus die Panel-Zonen auf leer oder nur Tastatur. `panelStyle` wird auf `null` gesetzt.

`panel.js` blendet das Panel aus, sobald die Session im Greeter- oder Lock-Modus läuft. In normalen Sessions wird das Panel wieder angezeigt.

`authPrompt.js` entfernt den sichtbaren Benutzeravatar und behält nur den Authentifizierungsfluss.

`loginDialog.js` entfernt die unteren Zusatzschaltflächen, deaktiviert die sichtbare Barrierefreiheits-Schaltfläche und stabilisiert die Cancel-Button-Allokation. Die AuthPrompt-Allokation richtet sich an der Eingabezeile aus, damit Benutzername und Passwort horizontal und vertikal gleich zentriert sind.

## Lock-Verhalten

`systemActions.js` macht die Lock-Aktion verfügbar, solange die Session nicht bereits gesperrt oder im Greeter ist. Die Lock-Aktion ruft `Main.screenShield.switchToGreeter()` auf.

`screenShield.js` ergänzt `switchToGreeter()`. Die Methode löscht Clipboard und Primary Selection und ruft über den Systembus `org.gnome.DisplayManager.LocalDisplayFactory.CreateTransientDisplay` auf. Ein kurzer Timeout verhindert parallele Mehrfachaufrufe. Bei aktivem GNOME-Lockdown wird ebenfalls direkt zum Greeter gewechselt.

`unlockDialog.js` zeigt direkt den Prompt statt der Uhrseite. Fehlgeschlagene Authentifizierung führt zurück zum Prompt.

## Farben und Theme

Der Greeter-Hintergrund ist `#1d1d1d`.

Der GDM-Accent-Wert wird in `dconf` und `greeter.dconf-defaults` auf `'slate'` gesetzt. Zusätzlich ersetzt das Overlay-CSS dynamische `-st-accent-color`-Verwendungen durch eine neutrale Fokusfarbe:

- Fokus-Akzent: `#747474`
- Fokus-Vordergrund: `#ffffff`

Damit bleiben aktive Eingabefelder, Fokusrahmen und Selection-Farben neutral und übernehmen keine benutzerbezogene Akzentfarbe.

Wenn beim aufrufenden Benutzer ein `custom-yaru-theme`-State existiert, wird das installierte Theme aus diesem State verwendet:

- State: `<home>/.local/state/custom-yaru-theme/last-state.env`
- validierte Felder: `dark_css_target`, `target_css_sha256`, `preset`
- Theme-Quelle in `source.env`: `custom-yaru-theme:<preset>`

Wenn kein gültiger `custom-yaru-theme`-State vorhanden ist, nutzt das Skript lokal hinterlegte `ubuntu25.10`-Farbwerte. Diese Werte liegen direkt im GDM-Skript und benötigen kein anderes Projekt. Die Theme-Quelle lautet dann `local:ubuntu25.10:default`.

## Tastaturlayout

Die Greeter-Input-Sources werden aus dem aufrufenden Benutzerkontext übernommen:

- `org.gnome.desktop.input-sources sources`
- `org.gnome.desktop.input-sources mru-sources`
- `org.gnome.desktop.input-sources xkb-options`

Wenn kein aufrufender Benutzer ermittelt werden kann, wird das Systemlayout aus `localectl status` verwendet. Leere MRU-Sources werden auf die aktiven Sources gesetzt.

Die Werte werden in `/etc/gdm3/greeter.dconf-defaults` und direkt in der dconf-Datenbank des `gdm`-Benutzers geschrieben.

## Benutzer-Shortcut

Für den aufrufenden Benutzer wird `Super+L` auf den Greeter-Pfad gesetzt. Der Befehl ist:

```bash
gdbus call --system --dest org.gnome.DisplayManager --object-path /org/gnome/DisplayManager/LocalDisplayFactory --method org.gnome.DisplayManager.LocalDisplayFactory.CreateTransientDisplay
```

Dabei werden diese Benutzerwerte gesichert und verwaltet:

- `org.gnome.settings-daemon.plugins.media-keys screensaver`
- `org.gnome.desktop.lockdown disable-lock-screen`
- `org.gnome.settings-daemon.plugins.media-keys custom-keybindings`
- Name, Befehl und Binding des verwalteten Custom-Keybindings

Wenn `Super+L` bereits durch einen anderen Befehl belegt ist, bricht das Skript ab. Ein vorhandener verwalteter Greeter-Befehl oder ein älterer `gdmflexiserver`-Befehl wird akzeptiert.

## Apply

`apply` führt diese Schritte aus:

1. Legacy-CSS-Override wiederherstellen, falls aktiv.
2. GResource-Overlay-Dateien aus den installierten GNOME-Shell-Ressourcen erzeugen.
3. Greeter-Hintergrund, Greeter-Accent und Input-Sources in `/etc/gdm3/greeter.dconf-defaults` schreiben.
4. GDM-Konfiguration über `generate-config` aktualisieren.
5. Aktuelle GDM-dconf-Werte sichern.
6. Greeter-Hintergrund, Greeter-Accent und Input-Sources direkt für den `gdm`-Benutzer setzen.
7. Benutzer-Shortcut sichern und `Super+L` setzen.
8. Greeter-Desktop-Datei sichern und `G_RESOURCE_OVERLAYS` in `Exec=` setzen.
9. systemd-Drop-ins schreiben und `systemctl daemon-reload` ausführen.
10. Installation verifizieren.
11. Optional `gdm` neu starten.

## Verify

`verify` prüft:

- alle Drop-ins
- alle Overlay-Dateien
- Greeter-Desktop-State und `Exec=env G_RESOURCE_OVERLAYS=...`
- alle erwarteten JavaScript-Patches
- neutralisierte CSS-Fokusfarbe
- Greeter-Hintergrundfarbe
- GDM-State-Dateien
- verwaltete Blöcke in `/etc/gdm3/greeter.dconf-defaults`
- GResource-Lookups über `gjs`
- Shortcut- und Lockdown-Werte des aufrufenden Benutzers
- Abwesenheit eines aktiven Legacy-CSS-Overrides

Bei Erfolg wird eine Zusammenfassung mit Drop-ins, Hintergrund, Theme-Quelle, Layout, Shortcut und Overlay-Pfad ausgegeben.

## Restore

`restore` führt diese Schritte aus:

1. systemd-Drop-ins entfernen und `systemctl daemon-reload` ausführen.
2. verwaltete Blöcke aus `/etc/gdm3/greeter.dconf-defaults` entfernen.
3. GDM-Konfiguration über `generate-config` aktualisieren.
4. GDM-dconf-Werte aus den State-Dateien wiederherstellen oder zurücksetzen.
5. Benutzer-Shortcut aus dem State wiederherstellen.
6. Greeter-Desktop-Datei aus dem State wiederherstellen.
7. Legacy-CSS-Override wiederherstellen, falls aktiv.
8. Restzustände prüfen.
9. Optional `gdm` neu starten.

Nach erfolgreicher Wiederherstellung dürfen die verwalteten State-Dateien und Drop-ins nicht mehr vorhanden sein. Die Greeter-Desktop-Datei darf kein `G_RESOURCE_OVERLAYS=` mehr enthalten.

## Legacy-CSS-Override

Das Skript erkennt einen aktiven Legacy-Override über den CSS-Block `#panel.login-screen > * {`. Ist er aktiv, wird er aus dem Backup `/usr/share/gnome-shell/gnome-shell-theme.gresource.ggm-backup-greeter-controls` wiederhergestellt. Ein gespeicherter alternatives-State wird über `update-alternatives` reaktiviert.

## Fehlerverhalten

Das Skript läuft mit `set -euo pipefail`. Fehlende Programme, fehlende Systemdateien, nicht passende Patch-Blöcke, fremde Shortcut-Belegungen, inkonsistente Theme-States und fehlgeschlagene Verifikationen brechen die Ausführung ab.

Erfolgreiche dconf- und GResource-Diagnoseausgaben werden unterdrückt. Fehlerausgaben bleiben sichtbar.
