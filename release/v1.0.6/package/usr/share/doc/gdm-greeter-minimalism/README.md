# gdm-greeter-minimalism

`gdm-greeter-minimalism` installs a reduced Ubuntu GDM login surface with neutral colors, centered credentials, no notifications, system sounds, or GNOME Shell controls. `Super+L` fully locks the GNOME session before activating the login greeter. Normal GDM authentication unlocks the existing session; autologin settings remain unchanged.

The Debian package maintains the customization across GDM and GNOME Shell updates. New overlays are generated and validated before atomic activation. Without an optional extension, an incompatible update activates verified stock resources, removes the custom startup integration, fails visibly, and reports the condition through a GNOME notification in the managed user's normal desktop session at the next login. Registered overlay extensions participate before activation and are never silently discarded on refresh failure; the interface is defined in [docs/description.md](docs/description.md#optional-overlay-extension).

## Installation

Install the versioned release package:

```bash
pkexec apt install ./release/v1.0.6/gdm-greeter-minimalism_1.0.6_all.deb
gdm-greeter-minimalism apply
```

The package installs the command, optional overlay-extension runner, targeted `dpkg` triggers, login notifier, and manual page. `apply` requests root privileges when needed.

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

The package root and `.deb` are written to `release/v1.0.6/`.

Fixes require a new installed and validated version before commit and push. Tags and GitHub Releases require separate authorization after package and physical Greeter validation. Tags are immutable and are never reused.

The complete build, verification, tag, and publication procedure is defined in [docs/release.md](docs/release.md).

## Documentation

- Target state: [docs/description.md](docs/description.md)
- Release process: [docs/release.md](docs/release.md)
- Installed command reference: `man gdm-greeter-minimalism`
- License: [GPL-3.0-only](LICENSE)
