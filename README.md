# gdm-greeter-minimalism

`gdm-greeter-minimalism` richtet den Ubuntu-GDM-Greeter als reduzierte Login-Oberfläche ein. Der Greeter nutzt eine neutrale Farbgebung, blendet GNOME-Shell-Bedienelemente aus und führt `Super+L` direkt zum Login-Greeter.

## Dokumentation

Die vollständige Zielzustands-Dokumentation steht in [docs/description.md](docs/description.md).

## Bedienung

Interaktiv:

```bash
./scripts/gdm-greeter-minimalism.sh
```

Direkt:

```bash
./scripts/gdm-greeter-minimalism.sh apply
./scripts/gdm-greeter-minimalism.sh verify
./scripts/gdm-greeter-minimalism.sh restore
```

`apply` und `restore` fordern bei Bedarf automatisch `sudo` an. Mit `--restart` wird `gdm` nach `apply` oder `restore` direkt neu gestartet.

## Lizenz

GPL-3.0-only. Siehe [LICENSE](LICENSE).
