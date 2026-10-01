# Minimaler Sitzungsschutz vor dem GDM-Greeter

## Umfang und Freigaben

- Der zusätzliche GNOME-Entsperrdialog wird im bestehenden Minimalism-Overlay durch einen minimalen opaken Schutz-Actor ersetzt. Die Umsetzung und Installation einer regulär gebauten neuen DEB-Version sind freigegeben.
- Vergleichsbasis: `857b7eabc392fbf798236e7c8bc825c83310a817`; regulär installiert und paketvalidiert ist 1.0.7. Die übergreifenden Prüf- und Liefergrenzen stehen in [full-code-review.md](full-code-review.md).
- Greeter-Design, Feldgröße, Feldposition, Benutzername-/Passworteingabe, Autologin und Security-Chain-Authentifizierung bleiben unverändert. Minimalism erhält keine eigene Stick-, Faktor- oder PAM-Logik.
- Die Security-Chain-Erweiterung prüft ihre tatsächlich verwendeten AuthPrompt-/LoginDialog-Schnittstellen, nicht die interne Implementierung des authentifizierungsfreien Schutz-Actors. Eine dafür notwendige Korrektur wird ausschließlich in deren eigenem Paket ausgeführt.
- Keine Löschung von GNOME-Komponenten, kein deaktivierter Sitzungsschutz, keine neuen Abhängigkeiten, kein automatischer GDM-Neustart und kein Ende laufender Sitzungen. Privilegierte Schritte verwenden gebündeltes `pkexec`.
- Nach der Korrektur ist eine Bewertung des Projekts gegenüber einem umgebauten GNOME-Sperrbildschirm beauftragt. Die lokale Entsperrfläche muss systemweit für die jeweils gesperrte Sitzung gelten, ohne fest verdrahteten Benutzer. Zuerst erscheint ausschließlich ein leeres Benutzernamenfeld, ohne sichtbaren Namen, Avatar oder Vorauswahl; manuelle Eingabe ist verpflichtend. Erst danach erscheint „Passwort oder Eingabe mit Schlüssel“. Entsperrt werden darf ausschließlich die zum eingegebenen Benutzer gehörende gesperrte Sitzung. Auf dieser Maschine gibt es einen Desktopbenutzer; Neuanmeldung ist keine Anforderung an den Sperrweg. Eine Umstellung ist nicht freigegeben.

## Zielzustand

- `ui/unlockDialog.js` stellt weiterhin den von GNOME verwendeten Constructor bereit, erzeugt aber keine Wallpaper-, Blur-, Uhr-, Benachrichtigungs-, Swipe- oder lokalen Authentifizierungsinstanzen.
- Die Schutzfläche ist einfarbig, deckt alle Monitore vollständig ab und wird ohne Einblend- oder Schiebeanimation gezeichnet. Ubuntu-Hintergrundeinstellungen machen sie nicht transparent.
- Echte Modalität und Eingabeschutz, Zwischenablagenbereinigung, Sperrzustand und logind-Meldung, Suspend-Sicherung, Crash-Wiederherstellung sowie legitime Entsperrung durch GDM bleiben erhalten.
- Der Greeter-Wechsel beginnt erst nach dem gezeichneten Schutz. Gleichzeitige Sperranforderungen und Sperren während einer laufenden Entsperrung behalten den bestehenden sicheren Lebenszyklus.
- Ein GDM-Fehler entsperrt die Sitzung nicht und wird über den bestehenden Fehlerkanal gemeldet. Ein Erfolg bestätigt keine bereits gezeichnete GDM-Oberfläche.
- GDM verwendet unverändert seinen eigenen LoginDialog. Nur dessen Authentifizierung gibt die bestehende Sitzung frei.
- Der zusätzliche Entsperrdialog und seine Ressourcen entfallen; die notwendige Schutzfläche und ein gegebenenfalls erforderlicher GDM-Kaltstart bleiben bestehen.

## Ausführung und Nachweise

1. Constructor-Aufrufer, Actor-Lebenszyklus, Hintergrundaktualisierung, Animationen, Entsperrsignale und Suspend-Inhibitor gegen die installierten GNOME-Ressourcen prüfen.
2. Bestehendes Overlay, dazugehörige Verifikation und passende gezielte Regressionen korrigieren; keine zusätzliche Authentifizierungsarchitektur einführen.
3. Normale unabhängige Nachprüfung mit Sol 6.1 high durchführen; bestätigte Funde mit Sol 6.1 medium korrigieren. Sicherheits- und Race-Fälle mit Astra 6 high prüfen. Erst bei fundfreien normalen Prüfungen abschließend Astra 6 xhigh einsetzen.
4. Quell- und Paketdokumentation sowie Versionsmetadaten auf 1.0.7 abgleichen. Shell-Syntax, statische Analyse, reale isolierte Ressourcen-/Schnittstellenprüfungen und konventionellen DEB-Bau durchführen. Modulparsing ersetzt keine Compositor-Laufzeit; nicht beobachtbare physische Kriterien bleiben offen.
5. Das geprüfte DEB per SHA256 binden, regulär installieren und installierte Nutzdateien, Paketintegrität, Ressourcenverifikation und Erweiterungsintegration prüfen. Greeter-Layout, PAM, Autologin und laufende Sitzungsprozesse gegen den Vorzustand prüfen.
6. Nach vom Betreiber neu gestarteter GNOME-Sitzung Super+L, Wiederholungen, authentifizierte Rückkehr, geschützten VT-Rückwechsel, mehrere Monitore und Suspend/Resume abnehmen. Keine produktiven Sperr- oder Suspend-Aktionen durch den Agenten.
7. Vor freigegebenem Commit die vollständige Projektdokumentation prüfen; installierten paketvalidierten Stand committen und pushen. Physische Nachweislücken ausdrücklich erhalten; keine Tags oder GitHub-Releases.
8. Anschließend einen systemweit umgebauten Sperrbildschirm für die jeweils gesperrte Sitzung untersuchen: verpflichtende manuelle Benutzernameneingabe ohne sichtbares Konto, bewusste Stick- und Passwortentsperrung, Autologin-Unabhängigkeit, Feldgestaltung, Sperr-/Suspend-Sicherheit, Ressourcen, Startlatenz, GNOME-Update-Stabilität und Änderungsumfang. Initiale Anmeldung bleibt GDM-Aufgabe. Ergebnis unter `docs/lock-screen-comparison.md` dokumentieren; keine Umstellung vornehmen.

## Stand

- Boot-ID `9f6db99e-8025-4ec4-83de-2335caa57089`: Der Betreiber bestätigt funktionierende Schlüssel und Super+L zum Greeter. Die noch laufende Shell mit Ressourcen von 1.0.6 erzeugt den zusätzlichen Entsperrdialog vor dem Wechsel; die installierten neuen Ressourcen ersetzen ihn durch die minimale Schutzfläche.
- Unabhängige Astra-6-high-Diagnose bestätigt den Constructor-Vertrag, die Opazitäts- und Animationsanforderungen sowie die notwendige Schutzfläche bis zum legitimen GDM-Entsperrsignal.
- Der reduzierte Actor und die animationsfreien Benutzer-Übergänge sind umgesetzt. Shell-Syntax, ShellCheck und elf reale isolierte Ressourcen-/Regressionsgruppen bestehen. Normale, vertiefte und abschließende Artefaktprüfung sowie reguläre Installation bestehen; die physische Prüfung der neu geladenen Ressourcen bleibt offen.
- Der Modalvertrag ist gegen die installierte Mutter-50.1-Typelib geprüft. Überlagerte Grabs sind regulär; APIs früherer Mutter-Versionen sind keine Prüfbasis.
- Der animationsfreie Benutzer-Ablauf erfasst tatsächliche `after-paint`-Ereignisse aller aktuellen Stage-Views und führt den Stock-Abschluss erst in `after-update` aus. Leere View-Listen geben nichts frei; Monitoränderungen verwerfen den Nachweis. Abschluss und Entsperrung entfernen alle drei Signalverbindungen. Erst dieser Abschluss setzt Active und gibt den bestehenden Suspend-Inhibitor frei, unabhängig vom späteren GDM-Erfolg. Der Greeter-Wechsel verwendet anschließend direkt den abgesicherten SHOWN-Zustand ohne weiteren Warte-Frame.
- Normale und vertiefte Prüfung des Mehrmonitor-Ablaufs sowie die normale Nachbindung der Entfernung des redundanten Warte-Frames sind code-seitig fundfrei. Quelle: SHA256 `8b812a4458cd2e5a0b9fa0275b3c0414d0dafbbe8c61cd4f6c3a6ca62e27ccf5`; Regressionen: SHA256 `8992c65bf549ab912bb1d8174906610b74b02fe7317c334007367e50c54e16ca`.
- Reguläres DEB 1.0.7: SHA256 `ede6b84dfdd2c0866b95d3234d9f0bede0219757619be9692fdfdbc0e2b5b795`. Alle fünf Kontroll- und neun Nutzdateien sind unabhängig gegen die Quellen geprüft; normale Nachbindung und abschließendes Astra-6-xhigh-Vorinstallationsreview sind fundfrei.
- Die optionale Erweiterung prüft ausschließlich ihre verwendeten AuthPrompt-/LoginDialog-Schnittstellen. Der reduzierte Actor bleibt unverändert erhalten. GDM-DEB 1.002: SHA256 `e456c0daa8db31c96054ab70c994a6d3cce88e1c9532d4f238c7b5a8992ea8ed`; vier Kontroll- und vier Nutzdateien stimmen mit den Quellen überein. Reale isolierte Zusammensetzung, normale und abschließende Nachbindung sind fundfrei.
- Regulär installiert sind Minimalism 1.0.7, GDM 1.002 und unverändert Boot 1.023. Installationshelfer: SHA256 `dc5ece4be4d5f2a430115ad6724a3923f083e38cc3cc3798dbb52138ea2be597`, Exit 0. Root-only Nachweise: `/root/ggm-shield-install-g0hl_1vi` und `/root/ggm-shield-resume-cw_cnx5w`. Alle 13 Nutzdateien stimmen einschließlich Modi und Eigentümern mit den DEBs überein; `dpkg -V`, `dpkg --audit`, installierte Minimalism-Verifikation und GDM-Journal-/Overlay-Prüfung bestehen. PAM, Autologin, Schlüssel, Registry, LUKS-Metadaten, ESP, sieben Greeter-Ressourcen und Sitzungs-/Prozessidentitäten sind gegen den ursprünglichen Vorzustand unverändert.
- Die abschließende Astra-6-xhigh-Installationsnachbindung ist fundfrei. Die laufende Benutzer-Shell PID 3313 verwendet noch 1.0.6; der Betreiber muss seine Sitzung neu laden. Die tatsächliche neue Schutzfläche, Multimonitor-, VT-Rückkehr- und Suspend-/Resume-Verhalten sind nicht physisch abgenommen.
