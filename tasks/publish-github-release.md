# GitHub-Release 1.0.4 veröffentlichen

## Zielzustand

- Der Release-Prozess ist in README und Projektdokumentation vollständig beschrieben.
- Das Release-Artefakt enthält den aktuellen Quellcode und die aktuelle Dokumentation.
- Der annotierte Tag `v1.0.4` zeigt auf den verifizierten Release-Commit.
- Das GitHub Release `v1.0.4` ist veröffentlicht und enthält das installierbare Debian-Paket.
- Tag, Ziel-Commit, Assetname und Veröffentlichungsstatus sind nach dem Upload verifiziert.

## Ausführung

1. Release-Prozess und GitHub-Veröffentlichung dokumentieren.
2. Debian-Paket neu bauen und Quell- sowie Paketinhalt vergleichen.
3. Änderungen mit `git add -A` committen und nach `origin/main` pushen.
4. Den Release-Commit als `v1.0.4` taggen und den Tag pushen.
5. Das Debian-Paket als Asset des GitHub Releases `v1.0.4` veröffentlichen.
6. Remote-Tag, Release-Metadaten, Asset und sauberen Worktree prüfen.
