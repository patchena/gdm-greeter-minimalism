# Lokale Entsperrfläche und GDM-Greeter

## Geltungsbereich

Verglichen werden der installierte Minimalism-Stand 1.0.7 und eine mögliche reduzierte lokale Entsperrfläche auf GNOME Shell/GDM 50.1. Die Bewertung autorisiert keine Umstellung. Auf dieser Maschine gibt es einen Desktopbenutzer; die Umsetzung muss trotzdem systemweit ohne fest verdrahteten Benutzer gelten.

Der erforderliche Ablauf beginnt mit einem leeren Benutzernamenfeld, ohne sichtbaren Namen, Avatar oder Vorauswahl. Der Name muss manuell eingegeben werden. Erst danach erscheint „Passwort oder Eingabe mit Schlüssel“. Enter im leeren Passwortfeld bestätigt einen USB-Versuch; eingegebener Text verwendet die Passwortauthentifizierung. Nur die zum eingegebenen Benutzer gehörende gesperrte Sitzung darf entsperrt werden. Ein abweichender Name darf keinen Authentifizierungserfolg für die Ausgangssitzung erzeugen. Autologin bleibt unverändert.

## Vergleich

| Bereich | Installierter Greeter-Sperrweg | Lokale reduzierte Entsperrfläche |
|---|---|---|
| Sitzungsschutz | Minimaler opaker Actor, Stock-Sperrvertrag, anschließend GDM-Wechsel | Stock-Sperrvertrag mit lokalem Authentifizierungsdialog |
| Namenseingabe | Bestehender Greeter-Prompt | Eigener leerer Prompt mit Bindung an den dynamischen Sitzungseigentümer erforderlich |
| Authentifizierung | Gemeinsamer AuthPrompt und `gdm-password` | Derselbe AuthPrompt und PAM-Pfad wiederverwendbar; reale Abnahme erforderlich |
| Darstellung | Einfarbiges bestehendes Greeter-Layout | Gleiches Feldlayout ohne Uhr, Blur, Wallpaper, Benachrichtigungen oder Avatar umzusetzen |
| Sitzungswechsel | Greeter-Start oder Wiederverwendung, VT-Wechsel und Wechselkoordination | Für das Entsperren der aktuellen Sitzung nicht erforderlich |
| Initialanmeldung | GDM | Weiterhin GDM |
| Wartung | Greeter-UI und Wechselkoordination | Greeter-UI und reduzierte lokale UI; weniger Wechselkoordination |

## Verifizierte Schnittstellen

Der vorhandene globale Shell-Template-Drop-in bindet das Overlay für darüber gestartete GNOME-Sitzungen. Stock UnlockDialog ermittelt seinen Benutzer dynamisch mit `GLib.get_user_name()` und verwendet `UNLOCK_ONLY`. Eine lokale Umsetzung benötigt keine feste UID; der zusätzliche Namensprompt muss an diesen Sitzungseigentümer gebunden bleiben. Das vollständige Greeter-Login ist ein anderer Vertrag. [GNOME UnlockDialog](https://github.com/GNOME/gnome-shell/blob/50.1/js/ui/unlockDialog.js), [GNOME LoginDialog](https://github.com/GNOME/gnome-shell/blob/50.1/js/gdm/loginDialog.js).

Ein normaler Benutzer-Shell-Aufrufer erhält im GDM-Reauthentifizierungspfad seine eigene Display-Sitzung; nur ein Login-Screen-Aufrufer wählt anhand des Namens andere Sitzungen. Die lokale Namenseingabe ist deshalb keine freie Sitzungswahl. [GDM-Aufruferbindung](https://github.com/GNOME/gdm/blob/50.1/daemon/gdm-manager.c).

Die gemeinsame GNOME-Verifikation verwendet auch lokal `gdm-password`. Die optionale Security-Chain-Erweiterung verändert ausschließlich AuthPrompt, bindet die bewusste Aktion an Dienst und Nonce und prüft über das bestehende PAM-Modul. Eine lokale Alternative darf keine Faktorprüfung duplizieren. Die Wiederverwendbarkeit ist quellengestützt, nicht als lokaler Laufzeitnachweis abgenommen. [GNOME-Verifier](https://github.com/GNOME/gnome-shell/blob/50.1/js/gdm/util.js); lokale Verträge: `../custom-security-chain/src/gdm_overlay.py` und `../custom-security-chain/src/pam_security_chain.c`.

GDM bietet per `disable-user-list=true` bereits eine manuelle Namenseingabe. Für die reduzierte lokale UI mit Pflicht-Namensprompt, exakter Feldgestaltung und ohne Uhr, Swipe oder Blur reicht diese Einstellung nicht. [GNOME-Administration](https://help.gnome.org/system-admin-guide/login-userlist-disable.html).

Das separate GDM-Profil isoliert seine Ton- und Darstellungseinstellungen vom Desktop. Eine lokale Oberfläche muss sperrzustandsbezogene Töne und Meldungen gezielt behandeln, ohne normale Desktopfunktionen zu deaktivieren. Ausgeblendete Inhalte belegen nicht, dass ihre Instanzen entfallen.

## Bewertung und Prüfgrenzen

Für den geforderten Sperrweg ist eine globale lokale Minimal-Entsperrfläche strukturell schlanker: zusätzlicher Greeter-Start, VT-Wechsel und deren Koordination entfallen beim normalen Entsperren. Gegenüber dem bereits implementierten Greeter-Sperrweg entsteht zunächst zusätzlicher Umsetzungs- und Abnahmeaufwand für Pflicht-Namenseingabe, AuthPrompt-Lebenszyklus und die sichere Übergabe. Langfristig entfällt Wechselkoordination; gleichzeitig bleiben zwei gestaltete, updateabhängige Oberflächen zu pflegen. Der lokale Sperrpfad ist daher einfacher, der gesamte Wartungsaufwand aber nicht ohne Weiteres kleiner. Diese Bewertung ist eine Architekturfolgerung, keine gemessene Entwicklungszeit oder Leistungszusage.

GDM-Minimalism bleibt für die reduzierte Initialanmeldung sinnvoll. Die spätere lokale Entsperrfläche ist als eigenes Projekt `gnome-lockscreen-minimalism` getrennt geplant. Ihre Overlays müssen zusammenspielen, ohne gemeinsame Logik zu duplizieren. Die optionale Security-Chain-Authentifizierung bleibt getrennt. Private GNOME-UI-Schnittstellen und beide Oberflächen bleiben updateabhängig.

Planung: [lokaler Lockscreen](../../gnome-lockscreen-minimalism/tasks/minimal-lockscreen.md) und [spätere Entfernung der Greeter-Sperrumleitung](../tasks/remove-greeter-lock-routing.md). Freigegeben sind die APs, nicht deren Umsetzung; die produktive Schaltung bleibt bis zur abgesicherten Übergabe erhalten.

Eine Umsetzung verlangt regulären DEB-Bau, unabhängige Nachprüfung und installierte Validierung sowie physische Abnahme von Pflicht-Namenseingabe, falschem Benutzer, bewusstem Enter, Passwort, fehlendem Stick, Fehler/Abbruch, wiederholtem Sperren, mehreren Monitoren, Suspend/Resume und Crash-Wiederherstellung. Zeit- und Speicherersparnis sind ohne vergleichbare Messungen nicht bezifferbar; GDM-Daemon und PAM bleiben beteiligt.
