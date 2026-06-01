# gdm-greeter-minimalism

`gdm-greeter-minimalism` configures the Ubuntu GDM greeter as a reduced login surface. The greeter uses neutral colors, hides GNOME Shell controls, and routes `Super+L` directly to the login greeter.

## Documentation

The full target-state documentation is available in [docs/description.md](docs/description.md).

## Usage

Interactive:

```bash
./scripts/gdm-greeter-minimalism.sh
```

Direct:

```bash
./scripts/gdm-greeter-minimalism.sh apply
./scripts/gdm-greeter-minimalism.sh verify
./scripts/gdm-greeter-minimalism.sh restore
```

`apply` and `restore` automatically request `sudo` when needed. With `--restart`, `gdm` is restarted immediately after `apply` or `restore`.

## License

GPL-3.0-only. See [LICENSE](LICENSE).
