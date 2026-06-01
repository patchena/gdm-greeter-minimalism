# GDM Greeter Minimalism

## Purpose

`gdm-greeter-minimalism.sh` configures the Ubuntu GDM greeter as a reduced login surface. The greeter shows no GNOME Shell controls, no panel, no quick settings, no calendar, no accessibility button, and no user avatar. Username and password are shown as centered input fields.

## Usage

The script can be started without arguments. In interactive mode, the action is selected with a single key; `Enter` is not required.

```bash
./scripts/gdm-greeter-minimalism.sh
```

Available actions:

- `1` or `a`: apply greeter minimalism
- `2`, `p`, or `v`: verify the installation
- `3`, `w`, or `r`: restore the original state
- `4` or `q`: cancel

For `apply` and `restore`, the script automatically re-executes itself through `sudo` when needed. Interactive mode asks whether `gdm` should be restarted before privilege escalation.

Non-interactive mode remains available:

```bash
./scripts/gdm-greeter-minimalism.sh apply
./scripts/gdm-greeter-minimalism.sh verify
./scripts/gdm-greeter-minimalism.sh restore
./scripts/gdm-greeter-minimalism.sh apply --restart
./scripts/gdm-greeter-minimalism.sh restore --restart
```

## Output

The output uses ANSI colors on TTYs. Steps are printed with `=>`, successful final states with `OK`, and errors in bold red. If `NO_COLOR` is set, no ANSI codes are used.

Successful `dbus-run-session` and `gjs` diagnostic output is hidden. On failure, the captured original output is written to `stderr`.

## Requirements

The script checks these core commands before `apply`, `verify`, and `restore`:

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

It also uses standard system utilities such as `awk`, `cp`, `grep`, `head`, `id`, `rm`, and `sed`. `sudo` is required only for non-root `apply` and `restore` runs. `update-alternatives` is required only when an alternatives-based legacy CSS override is migrated.

Required system files:

- `/etc/gdm3/greeter.dconf-defaults`
- `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`
- an executable GDM `generate-config` at `/usr/share/gdm/generate-config`, `/usr/libexec/gdm/generate-config`, or `/usr/lib/gdm/generate-config`
- an installed GNOME Shell resource library matching `libshell-*.so`
- a theme resource readable by `gresource`; the lookup order is `/usr/share/gnome-shell/gdm-theme.gresource`, `/usr/share/gnome-shell/gdm3-theme.gresource`, then `/usr/share/gnome-shell/gnome-shell-theme.gresource`

The Python module `gdms` is additionally required when an active legacy CSS override must be migrated.

## System Files

The script manages these files and directories:

- Overlay directory: `/usr/local/share/gnome-shell-overrides/greeter-controls`
- User shell drop-in: `/etc/systemd/user/org.gnome.Shell@wayland.service.d/90-disable-greeter-controls.conf`
- GDM service drop-in: `/etc/systemd/system/gdm.service.d/90-disable-greeter-controls.conf`
- GDM user drop-in: `<gdm-home>/.config/systemd/user/org.gnome.Shell@wayland.service.d/90-disable-greeter-controls.conf`
- Greeter dconf file: `/etc/gdm3/greeter.dconf-defaults`
- Greeter desktop file: `/usr/share/gdm/greeter/wayland-sessions/gnome-greeter.desktop`

State files:

- `/etc/gdm3/.ggm-gdm-input-sources.state`
- `/etc/gdm3/.ggm-gdm-background.state`
- `/etc/gdm3/.ggm-gdm-accent.state`
- `/etc/gdm3/.ggm-user-shortcut.state`
- `/etc/gdm3/.ggm-greeter-desktop.state`

## GResource Overlay

The overlay is loaded through `G_RESOURCE_OVERLAYS=/org/gnome/shell=/usr/local/share/gnome-shell-overrides/greeter-controls`. This environment value is written to three systemd drop-ins and additionally into the greeter desktop file.

Generated overlay files:

- `ui/sessionMode.js`
- `ui/panel.js`
- `misc/systemActions.js`
- `ui/screenShield.js`
- `ui/unlockDialog.js`
- `gdm/authPrompt.js`
- `gdm/loginDialog.js`
- `theme/gdm.css`
- `theme/source.env`

## Greeter Surface

`sessionMode.js` sets the panel zones in `gdm` and `unlock-dialog` mode to keyboard-only. `panelStyle` is set to `null`.

`panel.js` hides the panel whenever the session is in greeter or locked mode. In normal sessions, the panel is shown again.

`authPrompt.js` removes the visible user avatar and keeps only the authentication flow.

`loginDialog.js` removes the lower auxiliary buttons, disables the visible accessibility button, and stabilizes the cancel button allocation. The AuthPrompt allocation is aligned to the input row so username and password are centered at the same horizontal and vertical position.

## Lock Behavior

`systemActions.js` makes the lock action available as long as the session is not already locked or in the greeter. The lock action calls `Main.screenShield.switchToGreeter()`.

`screenShield.js` adds `switchToGreeter()`. The method clears the clipboard and primary selection, then calls `org.gnome.DisplayManager.LocalDisplayFactory.CreateTransientDisplay` through the system bus. A short timeout prevents parallel duplicate calls. When GNOME lockdown is active, it also switches directly to the greeter.

`unlockDialog.js` shows the prompt directly instead of the clock page. Failed authentication returns to the prompt.

## Colors and Theme

The greeter background is `#1d1d1d`.

The GDM accent value is set to `'slate'` in both `dconf` and `greeter.dconf-defaults`. Additionally, the overlay CSS replaces dynamic `-st-accent-color` usage with a neutral focus color:

- Focus accent: `#747474`
- Focus foreground: `#ffffff`

This keeps active input fields, focus rings, and selection colors neutral and prevents them from inheriting a user-related accent color.

If the calling user has a `custom-yaru-theme` state, the CSS file referenced by that state is used:

- State: `<home>/.local/state/custom-yaru-theme/last-state.env`
- `dark_css_target` must point to an existing CSS file
- `target_css_sha256` is checked when present
- `preset` labels the recorded theme source
- Theme source in `source.env`: `custom-yaru-theme:<preset>`

If no valid `custom-yaru-theme` state exists, the script uses locally embedded `ubuntu25.10` color values. These values live directly in the GDM script and do not depend on another project. The local preset maps upstream dark Yaru shell surfaces to neutral gray values and keeps common shell surfaces at `#353535`. The theme source is then `local:ubuntu25.10:default`.

## Keyboard Layout

Greeter input sources are copied from the calling user's context:

- `org.gnome.desktop.input-sources sources`
- `org.gnome.desktop.input-sources mru-sources`
- `org.gnome.desktop.input-sources xkb-options`

If no calling user can be resolved, the system layout from `localectl status` is used. GNOME's empty MRU value `@a(ss) []` is replaced with the active sources.

The values are written to `/etc/gdm3/greeter.dconf-defaults` and directly into the `gdm` user's dconf database.

## User Shortcut

For the calling user, `Super+L` is routed to the greeter path. The command is:

```bash
gdbus call --system --dest org.gnome.DisplayManager --object-path /org/gnome/DisplayManager/LocalDisplayFactory --method org.gnome.DisplayManager.LocalDisplayFactory.CreateTransientDisplay
```

These user settings are backed up and managed:

- `org.gnome.settings-daemon.plugins.media-keys screensaver`
- `org.gnome.desktop.lockdown disable-lock-screen`
- `org.gnome.settings-daemon.plugins.media-keys custom-keybindings`
- name, command, and binding of the managed custom keybinding

If `Super+L` is already assigned to another command, the script aborts. An existing managed greeter command or older `gdmflexiserver` command is accepted.

## Apply

`apply` performs these steps:

1. Normalize an active legacy CSS override back to the stock GDM theme.
2. Generate GResource overlay files from the installed GNOME Shell resources.
3. Write greeter background, greeter accent, and input sources to `/etc/gdm3/greeter.dconf-defaults`.
4. Refresh the GDM configuration through `generate-config`.
5. Back up current GDM dconf values.
6. Set greeter background, greeter accent, and input sources directly for the `gdm` user.
7. Back up the user shortcut and set `Super+L`.
8. Back up the greeter desktop file and add `G_RESOURCE_OVERLAYS` to `Exec=`.
9. Write systemd drop-ins and run `systemctl daemon-reload`.
10. Verify the installation.
11. Optionally restart `gdm`.

## Verify

`verify` checks:

- all drop-ins
- all overlay files
- greeter desktop state and `Exec=env G_RESOURCE_OVERLAYS=...`
- all expected JavaScript patches
- neutralized CSS focus color
- greeter background color
- GDM state files
- managed blocks in `/etc/gdm3/greeter.dconf-defaults`
- GResource lookups through `gjs`
- shortcut and lockdown values for the calling user
- absence of an active legacy CSS override

On success, a summary is printed with drop-ins, background, theme source, layout, shortcut, and overlay path.

## Restore

`restore` performs these steps:

1. Remove systemd drop-ins and run `systemctl daemon-reload`.
2. Remove managed blocks from `/etc/gdm3/greeter.dconf-defaults`.
3. Refresh the GDM configuration through `generate-config`.
4. Restore or reset GDM dconf values from the state files.
5. Restore the user shortcut from state.
6. Restore the greeter desktop file from state.
7. Normalize an active legacy CSS override back to the stock GDM theme.
8. Check for leftover managed state.
9. Optionally restart `gdm`.

After a successful restore, the managed state files and drop-ins must no longer exist. The greeter desktop file must no longer contain `G_RESOURCE_OVERLAYS=`. Generated overlay files can remain on disk because the loading paths are removed.

## Legacy CSS Override

The script detects an active legacy override through the CSS block `#panel.login-screen > * {`. If it is active, it is restored from the backup `/usr/share/gnome-shell/gnome-shell-theme.gresource.ggm-backup-greeter-controls`. A stored alternatives state is reactivated through `update-alternatives`.

## Error Behavior

The script runs with `set -euo pipefail`. Missing commands, missing system files, unmatched patch blocks, conflicting shortcut assignments, inconsistent theme states, and failed verification checks abort execution.

Successful dconf and GResource diagnostic output is suppressed. Error output remains visible.
