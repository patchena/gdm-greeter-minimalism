# Vollständige Codeprüfung

## Umfang und Freigaben

- Vollständiger aktueller Code unter `scripts/`, `packaging/` und `tests/`, einschließlich nicht versionierter Dateien; neuer Paketbaum und DEB unter `release/v1.0.6/` werden gegen ihre Quellen geprüft.
- Vergleichsbasis: `6a03e40d89ca942fd29f02f858f03a38df8d9d61`.
- Frühere versionierte Release-Artefakte bleiben unverändert; sie sind keine aktuelle Implementierungsquelle.
- Die aktuelle Freigabe hat Vorrang vor früheren Arbeitspaketen: keine Beendigung alter Greeter-Sitzungen, keine Tags und keine GitHub-Veröffentlichung.
- Bestehende Funktionsverträge stehen in `docs/description.md` und den Greeter-Arbeitspaketen. Security-Chain-Integration wird gegen deren `tasks/gdm-stick-unlock.md` und `tasks/full-code-review.md` geprüft.
- Bestätigte Fehler werden korrigiert und unabhängig nachgeprüft. Neue Sicherheits-, Geräte-, Faktor- oder PAM-Logik gehört nicht in Minimalism.
- Bei erforderlichen Fixes wird eine neue Paketversion gebaut, installiert und am installierten Stand validiert, bevor Commit und Push erfolgen. Privilegierte Schritte verwenden gebündeltes `pkexec`.
- Die Validierungsinstallation erfolgt ausschließlich über die regulär gebaute `.deb`; keine Skriptkopien, Direktinstallation aus dem Quellbaum oder Ersatzinstallation.
- Laufende Sitzungen, Autologin, Schlüssel, LUKS-Slots und Stickdaten bleiben erhalten. GDM-Neustart, Sitzungsende, produktives Restore sowie neue Tags und GitHub-Releases sind nicht freigegeben.
- Commit und Push des abschließend geprüften Minimalism-Projekts sind freigegeben. Vor jedem Commit wird die vollständige Projektdokumentation abgeglichen.

## Modellzuordnung

- Orchestrierung und Sitzung sowie normale Reviews: Sol 6.1 high.
- Umsetzung und Fixes: Sol 6.1 medium.
- Schwierige Fälle: Astra 6 high.
- Abschließendes Gesamtreview: Astra 6 xhigh, erst nach fundfreier normaler Nachprüfung aller Bereiche.

## Prüfkriterien

- Vollständige Quell-, Aufrufer-, Konfigurations-, Paket- und Testabdeckung; bestätigte Funde mit Quelle, Auslöser, Wirkung und überprüfbarem Nachweis.
- Apply, Refresh, Verify, Restore, Lock und Notify erfüllen den bestehenden Greeter-Vertrag und melden Fehler sichtbar.
- Kandidaten, Ressourcenprüfung, Fingerprints, Aktivierung, Locks, Fehlerzustände und Rücknahme erhalten konsistente Generationen und vorhandene Einstellungen.
- Die optionale Erweiterung bleibt projektunabhängig, root-vertrauenswürdig und begrenzt; Prepare-/Commit-Fehler entfernen die registrierte Security-Chain-Integration nicht stillschweigend.
- Paketbau, Maintainerskripte, Trigger, Metadaten und Ressourcen stimmen mit den aktuellen Quellen überein.
- Korrekturen bestehen passende Builds und isolierte Regressionen ohne Mock-Daten oder produktive Teständerungen.
- Bei Fixes stimmen installierte Dateien und Paketintegrität mit dem geprüften neuen Artefakt überein; installierte Verifikation gelingt ohne automatischen GDM-Neustart.
- Physische Greeter-, Suspend- und Sitzungsnachweise bleiben getrennt von Codeprüfung und isolierten Tests; erforderliche Benutzerinteraktion wird ausdrücklich abgestimmt.
- Normale Reviews und anschließendes Astra-Gesamtreview sind ohne offene bestätigte Funde abgeschlossen; finale Commits sind remote verifiziert.

## Stand

- Vollständige Codeprüfung und abschließendes Astra-6-xhigh-Review fundfrei; installierter Minimalism-Stand 1.0.6.
- Security-Chain-Codeprüfung ist abgeschlossen und als `d912bfb30f9ec2951788ba0c6fa4f1eaafb5eacb` gesichert. Boot 1.023 und GDM 1.001 sind regulär installiert; M2-Migration und Aktivierung sind paketvalidiert. Physische Freigaben bleiben separat offen.

## Offene Prüfungen und Korrekturen

- GSettings-Varianten werden typisiert verarbeitet; Shortcut-Backups erfassen den tatsächlich geänderten Pfad. Veröffentlichungsfehler setzen keinen vorbereiteten Erfolg. Unabhängige normale Nachprüfung ist fundfrei.
- Erweiterungsprozesse haben begrenzte Ausgabe und vollständige Prozessgruppenbereinigung bei Erfolg, Fehler, Timeout und behandelten Abbruchsignalen. Zehn isolierte Prozess-, Ausgabe- und Sperrdeskriptorprüfungen sowie sechs Pfadablehnungen bestehen. Unabhängige Sol-6.1-high-Nachprüfung ist fundfrei; Runner-SHA256: `8518e054b1ff2deb91a5840c15a44d66e0bd734e3733dee5e1758cde570e1f54`.
- Alle Sperreinstiege verschließen die Ausgangssitzung durch GNOMEs vollständigen Sperrablauf, bevor GDM aktiviert wird. Der reguläre Suspend-Sperrinhibitor bleibt wirksam. Wiederholte D-Bus-Sperraufrufe erhalten zuverlässig eine Antwort. Normale und unabhängige vertiefte Nachprüfung sind fundfrei; physischer Nachweis bleibt offen.
- Einstellungs-Backups werden nur nach erfolgreichen Abfragen veröffentlicht. Fehlende Backups erlauben beim Restore keine erfundenen Originalwerte. Fehlende verwaltete Soundverzeichnisse sind ein gültiger partieller Restore-Zustand. GTK vergleicht die vollständige Super+L-Belegung. Unabhängige normale Nachprüfung ist fundfrei.
- Schreib- und Löschzugriffe auf GDM-Drop-ins verwenden sichere Verzeichnisdeskriptoren ohne Symlink-Folgen. Eigentumsänderungen betreffen nur neu erzeugte Dateien, keine vorhandenen fremden Verzeichnisinhalte. Unabhängige normale Nachprüfung ist fundfrei.
- Reguläres DEB 1.0.6 installiert; alle neun Nutzdateien stimmen bytegenau einschließlich Modi und Eigentümern überein. `dpkg -V` und installierte Verifikation bestehen. Geschützte GDM-/PAM-Dateien, Autologin, GDM-/Shell-Prozessidentitäten, Sitzungszustand und Fremdpaketversionen bleiben unverändert. Physische Sperr-, Rückanmeldungs- und Suspend-Abnahme mit neu geladenen Shell-Ressourcen ist offen. Ein sichtbarer Greeter allein beweist keine gesperrte Ausgangssitzung.
- Stock-Fingerprints enthalten die Ressourcenrevision. Bereits erfolgreiche Greeter-Wechsel werden innerhalb derselben Sperrepoche wiederverwendet; neue Paint-Wartevorgänge sind auf 15 Sekunden begrenzt. Neun isolierte Regressiongruppen und normale Nachprüfung sind fundfrei.
- Neue Sperranforderungen während einer noch laufenden Stock-Entsperrung erhalten keinen gecachten Erfolg. Sie warten den vollständigen Abschluss ab und sperren danach erneut regulär. Normale und unabhängige vertiefte Nachprüfung sind fundfrei.
- Die Super+L-Konfliktsuche prüft die vollständige Liste und lehnt fremde oder mehrdeutige exakte Treffer vor Backup und Einstellungsänderungen ab. Elf isolierte Regressiongruppen bestehen; unabhängige normale Nachprüfung einschließlich eindeutiger, fehlender und fremder Einzelbelegung ist fundfrei.
- Dokumentations- und Paketnachprüfung der Version 1.0.6 sind fundfrei. Der reguläre Neubau enthält die korrigierte Shortcut-Suche; alle 14 Kontroll- und Nutzdateien stimmen mit den Quellen überein. Abschließende Astra-6-xhigh-Nachbindung ist fundfrei.
- Quell-SHA256: `3d81ccfea7b166dd814e168087f4a69bcb52c46e5e5c6b13adbf9016aa01cba8`; DEB-SHA256: `18543fcc960f49133ecc2f42aad3c2bff4a2e8479fb7cab1d621d81ae2d624d2`.
- Die laufende Benutzer-Shell PID 3848 verwendet weiterhin vor der Installation geladene Sperrmodule. Der neue CLI-Aufruf und `disable-lock-screen=false` führen mit diesen alten Modulen zum lokalen GNOME-Entsperrdialog mit Wallpaper und Blur. Theme-CSS und Login-Positionierung sind gegenüber der vorherigen Basis byteidentisch. Zwei unabhängige lesende Nachprüfungen bestätigen den Mischzustand. Die Abnahme des direkten minimalistischen Greeter-Wechsels erfordert eine vom Betreiber neu gestartete Shell-Sitzung; geladene Module werden nicht im laufenden Prozess ersetzt und der vollständige Sitzungsverschluss bleibt erhalten.
