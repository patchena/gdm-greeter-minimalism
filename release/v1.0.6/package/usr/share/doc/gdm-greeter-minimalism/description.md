# GDM Greeter Minimalism

## Purpose

`gdm-greeter-minimalism` configures the Ubuntu GDM greeter as a reduced login surface. The greeter has no notifications, system sounds, panel, quick settings, calendar, accessibility button, auxiliary login buttons, or user avatar. Username and password inputs are centered. The background and focus colors are neutral. `Super+L` fully locks the GNOME session before activating GDM. Normal GDM authentication unlocks the existing session; autologin remains unchanged.

The system package maintains this state across GDM and GNOME Shell package updates without automatically restarting GDM.

## Components

The project contains:

- `/usr/bin/gdm-greeter-minimalism`: installed management command
- `scripts/gdm-greeter-minimalism.sh`: command source
- `/usr/lib/gdm-greeter-minimalism/run-overlay-extension`: optional extension runner
- `scripts/overlay-extension.py`: runner source
- `packaging/`: Debian metadata, maintainer scripts, triggers, autostart entry, and manual page
- `scripts/build-release.sh`: versioned package builder
- `docs/release.md`: release verification and publication procedure
- `release/v1.0.6/`: package root and installable Debian package

The package version is `1.0.6` and its architecture is `all`.

## Installation

Install the release package and apply the configuration:

```bash
pkexec apt install ./release/v1.0.6/gdm-greeter-minimalism_1.0.6_all.deb
gdm-greeter-minimalism apply
```

The package depends on:

- `dbus-daemon`
- `dconf-cli`
- `gdm3`
- `gjs`
- `gnome-shell`
- `libglib2.0-bin`
- `python3`
- `sudo`
- `systemd`

GTK4 introspection is supplied by `gnome-shell`; Essential packages supply the base tools and an `awk` provider.

The command requires:

- `/etc/gdm3/greeter.dconf-defaults`
- `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`
- an executable GDM `generate-config` at `/usr/share/gdm/generate-config`, `/usr/libexec/gdm/generate-config`, or `/usr/lib/gdm/generate-config`
- an installed GNOME Shell resource library matching `libshell-*.so`
- a GDM theme resource at `/usr/share/gnome-shell/gdm-theme.gresource`, `/usr/share/gnome-shell/gdm3-theme.gresource`, or `/usr/share/gnome-shell/gnome-shell-theme.gresource`

An active legacy CSS override additionally requires the `gdms` Python module from `gdm-settings`.

## Command Interface

Without arguments, the command opens a single-key interactive selector:

- `1` or `a`: apply
- `2`, `p`, or `v`: verify
- `3`, `w`, or `r`: restore
- `4` or `q`: exit

Direct commands:

```bash
gdm-greeter-minimalism apply
gdm-greeter-minimalism verify
gdm-greeter-minimalism lock
gdm-greeter-minimalism restore
gdm-greeter-minimalism apply --restart
gdm-greeter-minimalism restore --restart
```

`apply` and `restore` re-execute through `sudo` when the caller is not root. `--restart` restarts GDM after the requested action and ends running graphical sessions.

`refresh` and `notify` are internal package commands. `refresh` requires root, updates the managed shortcut, and is called by package maintenance. `notify` runs in the managed user's GNOME session.

TTY output uses ANSI colors unless `NO_COLOR` is set. Steps use `=>`, successful final states use `OK`, and errors are written to `stderr`. Successful `dbus-run-session` and `gjs` diagnostics remain silent.

## Package Lifecycle

The package registers `interest-noawait` triggers for:

- `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`
- `/usr/lib/gnome-shell`
- `/usr/share/gnome-shell`

`postinst configure` and `postinst triggered` call `refresh` when the installation is enabled or existing managed shortcut state is present.

`prerm remove` and `prerm deconfigure` call `restore` while the command is still installed. Package upgrades do not restore the configuration.

The autostart file `/etc/xdg/autostart/gdm-greeter-minimalism-notify.desktop` is a package conffile.

## Transactional Overlay

The stable resource path is:

```text
/usr/local/share/gnome-shell-overrides/greeter-controls/active
```

It is a symlink to one validated release directory. Candidates, customized releases, and stock releases share the same filesystem below the overlay base, so directory and symlink activation uses atomic renames.

### Stock Release

Before a customized overlay is evaluated, `refresh` creates or validates a stock release.

Its fingerprint covers the overlay revision, installed GNOME Shell resource library and active GDM theme resource. A changed resource scope receives a new generation; existing releases remain unchanged. It contains byte-identical copies of:

- `ui/sessionMode.js`
- `ui/panel.js`
- `misc/systemActions.js`
- `ui/screenShield.js`
- `ui/shellDBus.js`
- `ui/unlockDialog.js`
- `gdm/authPrompt.js`
- `gdm/loginDialog.js`
- `theme/gdm.css`

Each file is compared with a fresh `gresource extract`. All resource paths are then resolved through `gjs` with the stock overlay active.

### Customized Release

The customized fingerprint covers:

- the management script
- the overlay revision
- the installed GNOME Shell resource library
- the active GDM theme resource
- the managed user's `custom-yaru-theme` state and referenced CSS when present

Generation writes to a unique candidate directory. Every expected JavaScript patch, CSS replacement, file, and GResource lookup is checked before the candidate is moved into `releases/<fingerprint>`.

Activation performs:

1. atomic `active` symlink replacement
2. active release state update
3. atomic systemd drop-in writes
4. atomic `Exec=` transformation of the current package-owned greeter desktop file
5. complete installed-resource verification

The desktop transformation strips existing `G_RESOURCE_OVERLAYS` prefixes and adds exactly one current prefix. Restore removes only this prefix from the current file. No complete backup of the package-owned desktop file is retained or restored.

## Update Failure

Without a registered extension, customized generation or validation failure performs:

1. `active` is atomically switched to the validated stock release.
2. system and user systemd drop-ins are removed.
3. the custom environment prefix is removed from the current greeter desktop file.
4. systemd configuration is reloaded.
5. `/var/lib/gdm-greeter-minimalism/failure.json` is written.
6. the package action exits with an error.

The stable `active` path remains valid for a GDM daemon that already inherited `G_RESOURCE_OVERLAYS`; newly started greeter processes resolve the current stock resources without a GDM restart.

The failure state contains:

- error identity
- notification summary and body
- normalized diagnostic detail
- installed GDM version
- installed GNOME Shell version

At the next login to the managed user's normal GNOME desktop session, the autostart notifier checks the configured target user and calls `org.freedesktop.Notifications.Notify`. The GDM login and unlock modes do not display this notification. A user state file at `~/.local/state/gdm-greeter-minimalism/notified` prevents repeated notifications for the same failure state. A successful refresh removes `failure.json`. A later distinct failure receives a new identity.

Managed background, accent, sound, input-source, and shortcut settings remain in place during an update incompatibility. The GNOME Shell resource surface and startup integration use the safe stock path.

## Optional Overlay Extension

An optional executable at `/usr/lib/gdm-greeter-minimalism/overlay-extension` participates in every refresh. No extension package is required. The provider, its parent directories, the returned release and all release contents must be canonical, root-owned, and not group- or world-writable. Symbolic links and hard-linked files are rejected.

After base resource validation, `prepare ABSOLUTE_BASE_RELEASE` must return exactly one absolute release path followed by a newline, at most 4096 bytes. The release must be a direct child of `/usr/local/share/gnome-shell-overrides/greeter-controls/releases`. The composed resources pass the same generic checks before activation. After activation and installed-resource verification, `commit ABSOLUTE_COMPOSED_RELEASE` must succeed without stdout output. Standard output is bounded while the provider runs. Each operation has a 60-second timeout; failure is reported explicitly. Completion, error, timeout and handled SIGTERM, SIGINT or SIGHUP terminate the provider process group and reap its leader.

The provider inherits the held greeter lock through file descriptor 9 and `GGM_OVERLAY_LOCK_FD=9`. It must validate and reuse that descriptor, not acquire a second conflicting greeter lock. Other explicitly inheritable descriptors and the calling environment remain available. A busy greeter lock fails immediately. The provider owns any extension-specific preparation journal and verification.

With a registered provider, a failed preparation leaves the active generation unchanged. A failure after activation is reported without switching to stock resources or removing the startup integration. The provider's pending journal remains available for recovery. Missing, malformed or untrusted provider output never silently disables the registered extension.

## System Integration

The overlay environment is:

```text
G_RESOURCE_OVERLAYS=/org/gnome/shell=/usr/local/share/gnome-shell-overrides/greeter-controls/active
```

It is written to:

- `/etc/systemd/user/org.gnome.Shell@.service.d/90-disable-greeter-controls.conf`
- `/etc/systemd/system/gdm.service.d/90-disable-greeter-controls.conf`
- `<gdm-home>/.config/systemd/user/org.gnome.Shell@.service.d/90-disable-greeter-controls.conf`
- the `Exec=` line in `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`

The desktop and drop-in files are replaced atomically. Drop-in creation and removal use directory descriptors without following symbolic links. Ownership changes affect only newly created files, not existing directory contents. The system manager and the available managed user manager are reloaded after drop-in changes. The generic system-wide template drop-in applies the lock behavior to every desktop user after the respective user manager starts or reloads it. An already running desktop shell requires a logout or reboot before it uses a newly installed overlay.

## Runtime State

Persistent runtime state is stored under `/var/lib/gdm-greeter-minimalism`:

- `active-overlay`: customized release selected during the last activation
- `stock-overlay`: validated stock release for the installed resources
- `enabled`: installation state
- `target-user`: managed user
- `failure.json`: current incompatibility state when present

Overlay storage is under `/usr/local/share/gnome-shell-overrides/greeter-controls`:

- `active`: stable active symlink
- `candidates`: generation candidates
- `releases`: validated customized releases
- `stock-releases`: validated byte-identical stock releases

Configuration backups are:

- `/etc/gdm3/.ggm-gdm-input-sources.state`
- `/etc/gdm3/.ggm-gdm-background.state`
- `/etc/gdm3/.ggm-gdm-accent.state`
- `/etc/gdm3/.ggm-gdm-profile.state`
- `/etc/gdm3/.ggm-user-shortcut.state`

Generated overlay releases remain after restore but are inactive.

## Greeter Surface

`sessionMode.js` disables notifications in `gdm` and `unlock-dialog`, limits both panel zones to the keyboard indicator, and sets `panelStyle` to `null`. The `user` mode keeps notifications enabled.

`panel.js` hides the panel in greeter and locked modes and restores it in normal sessions.

`authPrompt.js` removes the visible user avatar.

`loginDialog.js` removes auxiliary buttons and the accessibility button, preserves stable cancel-button allocation, shows the round cancel button only for password input, and aligns username and password prompts to the same centered input position.

## Lock Behavior

The CLI synchronously calls `org.gnome.ScreenSaver.Lock`. `systemActions.js` uses the common Shell locking path for lock and user-switch actions.

`screenShield.js`:

- clears clipboard and primary selection
- executes the complete stock GNOME session lock before switching, including modal input protection and locked state
- shares the pending operation between concurrent calls
- reuses an already successful greeter switch until the session is unlocked
- waits for any current stock unlock to finish before locking again
- limits waiting for completed unlocking and the painted shield to 15 seconds; timeout is an error, not an unlock
- switches to an existing login session or creates one when required through `Gdm.goto_login_session_sync(null)`
- preserves stock suspend inhibition and logind unlocking
- rejects greeter switches from existing greeter sessions

`shellDBus.js` answers each lock request after the shared operation succeeds or returns a D-Bus error. A failed GDM switch does not unlock the session. Existing GDM authentication and logind `UnlockSession` release the regular Shell lock.

`unlockDialog.js` opens directly on the authentication prompt and returns failed authentication to the prompt.

## Colors and Theme

The greeter background is `#1d1d1d`. The GDM accent is `'slate'`.

Overlay CSS sets:

- focus accent: `#747474`
- focus foreground: `#ffffff`

Dynamic `-st-accent-color` and `-st-accent-fg-color` references are replaced with these neutral values.

If `<home>/.local/state/custom-yaru-theme/last-state.env` exists:

- `dark_css_target` must reference an existing CSS file
- `target_css_sha256` is validated when present
- `preset` identifies the source in `theme/source.env`

When no custom state exists, the local `ubuntu25.10` preset transforms the installed GDM CSS to neutral gray surfaces. Its recorded source is `local:ubuntu25.10:default`. Existing invalid state, missing CSS or checksum mismatches are errors.

## Keyboard Layout

The greeter copies these settings from the calling user:

- `org.gnome.desktop.input-sources sources`
- `org.gnome.desktop.input-sources mru-sources`
- `org.gnome.desktop.input-sources xkb-options`

The system layout from `localectl status` is used when no caller is available. An empty GNOME MRU value is replaced with the active sources.

Values are written to `/etc/gdm3/greeter.dconf-defaults` and the `gdm` user's dconf database.

## Greeter Sound

The managed sound configuration sets:

- `org.gnome.desktop.sound event-sounds=false`
- `org.gnome.desktop.sound input-feedback-sounds=false`
- `org.gnome.desktop.sound theme-name='gdm-greeter-minimalism'`
- `org.gnome.desktop.wm.preferences audible-bell=false`

The values are written to a marked block in `/etc/gdm3/greeter.dconf-defaults` and locked through `/usr/share/gdm/dconf/locks/99-gdm-greeter-minimalism`. `/usr/share/gdm/generate-config` regenerates `/var/lib/gdm3/greeter-dconf-defaults` and reloads the GDM dconf service.

When `/etc/dconf/profile/gdm` exists, its original content is stored in `/etc/gdm3/.ggm-gdm-profile.state` and its legacy file database reference is replaced with `/var/lib/gdm3/greeter-dconf-defaults`. This preserves its `system-db:gdm` settings while using the current Greeter database. The packaged `/usr/share/dconf/profile/gdm` already references that database.

The sound theme at `/usr/share/sounds/gdm-greeter-minimalism` disables these direct sound events:

- `audio-volume-change`
- `battery-caution`
- `battery-low`
- `bell-window-system`
- `power-plug`
- `power-unplug`
- `system-ready`

The theme is selected only by the GDM configuration. Desktop-user sound settings and themes remain unchanged.

## User Shortcut

The managed `Super+L` command is:

```text
/usr/bin/gdm-greeter-minimalism lock
```

The following settings are backed up:

- `org.gnome.settings-daemon.plugins.media-keys screensaver`
- `org.gnome.desktop.lockdown disable-lock-screen`
- `org.gnome.settings-daemon.plugins.media-keys custom-keybindings`
- managed custom-keybinding name, command, and binding

An unrelated existing `Super+L` binding aborts `apply`. The managed command and the previous package command are accepted.

GTK parses the complete accelerator and compares its key and modifiers. The backup captures the actual modified shortcut path, remains unchanged across refreshes, and is written only after successful settings reads. Managed `disable-lock-screen=false` preserves GNOME session locking.

## Apply

`apply` performs:

1. target-user and enabled-state persistence
2. active legacy CSS override normalization
3. greeter background, accent, sound, and input-source block writes
4. sound-theme installation and GDM database regeneration
5. GDM dconf backup and value writes
6. stock overlay generation and validation
7. customized candidate generation and validation
8. atomic customized activation
9. user shortcut backup and update
10. complete installation verification
11. optional GDM restart

## Verify

`verify` checks:

- all three systemd drop-ins
- the current desktop `Exec=` environment
- every customized overlay file
- expected JavaScript and CSS transformations
- background, accent, sound, and input-source blocks
- the active and packaged GDM profiles, sound locks, and the managed sound theme
- GDM backup state
- GResource resolution through `gjs`
- user shortcut and lockdown settings when a user context is available
- absence of an active legacy CSS override

Success prints the active drop-ins, background, theme origin, input origin, shortcut owner, and stable overlay path.

## Restore

With a registered overlay extension, restore and package removal are rejected before changing the integration. The extension must first be removed through its owning package's removal workflow.

`restore` performs:

1. validated stock release preparation
2. atomic `active` switch to stock resources
3. systemd drop-in removal and daemon reload
4. desktop environment prefix removal
5. managed greeter block, sound locks, and sound-theme removal
6. GDM database regeneration, profile restoration, and dconf restoration
7. user shortcut restoration
8. legacy override normalization
9. runtime state removal
10. leftover-state verification
11. optional GDM restart

The stable overlay symlink remains on validated stock resources. Customized and stock release directories remain stored but inactive. Settings without a backup are not reset to invented original values. Already absent managed sound directories are valid partial-restore states; other removal errors remain visible.

## Legacy CSS Override

An active legacy override is detected through `#panel.login-screen > * {` in the active GDM CSS. It is restored from `/usr/share/gnome-shell/gnome-shell-theme.gresource.ggm-backup-greeter-controls`. A stored alternatives selection is restored through `update-alternatives`.

## Release Build

`scripts/build-release.sh` creates:

- `release/v1.0.6/package`: Debian package root
- `release/v1.0.6/gdm-greeter-minimalism_1.0.6_all.deb`: installable package

The package contains:

- management command
- optional extension runner
- dpkg triggers
- `postinst` and `prerm`
- GNOME autostart notifier
- project README, target-state documentation, and release procedure
- Debian changelog and copyright metadata
- compressed manual page

## GitHub Distribution

Each published version has an annotated immutable Git tag named `v<version>`. The GitHub Release uses the same name, points to the verified release commit, and contains the corresponding `.deb` from the versioned release directory.

Release publication occurs only after the package build, installed verification, and required manual Greeter validation succeed. The complete procedure is defined in `docs/release.md`.

## Error Behavior

All management paths use strict shell error handling. Missing tools or files, resource extraction errors, unmatched patch blocks, theme checksum mismatches, conflicting shortcuts, failed atomic writes, inconsistent state, and failed verification terminate the action with a nonzero exit.

No package-triggered path suppresses incompatibility or restarts GDM.
