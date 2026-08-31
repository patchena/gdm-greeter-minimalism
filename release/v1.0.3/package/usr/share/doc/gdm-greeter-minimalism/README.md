# gdm-greeter-minimalism

`gdm-greeter-minimalism` installs a reduced Ubuntu GDM login surface with neutral colors, centered credentials, no notifications or GNOME Shell controls, and `Super+L` routing to the login greeter.

The Debian package maintains the customization across GDM and GNOME Shell updates. New overlays are generated and validated before atomic activation. An incompatible update activates verified stock resources, removes the custom startup integration, fails visibly, and reports the condition through a GNOME notification in the managed user's normal desktop session at the next login.

## Installation

Install the versioned release package:

```bash
sudo apt install ./release/v1.0.3/gdm-greeter-minimalism_1.0.3_all.deb
gdm-greeter-minimalism apply
```

The package installs the command, targeted `dpkg` triggers, the login notifier, and the manual page. `apply` requests root privileges when needed.

Log out or reboot after installation so the running desktop shell loads the overlay.

## Usage

```bash
gdm-greeter-minimalism
gdm-greeter-minimalism apply
gdm-greeter-minimalism verify
gdm-greeter-minimalism lock
gdm-greeter-minimalism restore
```

`apply` and `restore` accept `--restart`. Restarting GDM ends running graphical sessions. Package-triggered refreshes never restart GDM.

## Release

Build the release package:

```bash
./scripts/build-release.sh
```

The package root and `.deb` are written to `release/v1.0.3/`.

## Documentation

- Target state: [docs/description.md](docs/description.md)
- Installed command reference: `man gdm-greeter-minimalism`
- License: [GPL-3.0-only](LICENSE)
