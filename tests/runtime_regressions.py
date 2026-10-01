import os
from pathlib import Path
import shlex
import subprocess
import tempfile


SOURCE = Path(__file__).resolve().parents[1] / "scripts/gdm-greeter-minimalism.sh"
SETUP = f"""
source {shlex.quote(str(SOURCE))} notify
export XDG_CONFIG_HOME=/tmp/config XDG_CACHE_HOME=/tmp/cache
export GSETTINGS_BACKEND=keyfile
mkdir -p "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" /tmp/state /tmp/candidates
resolved_target_user="$(id -un)"
target_user_state=/tmp/state/target-user
printf '%s\\n' "$resolved_target_user" >"$target_user_state"
user_shortcut_state=/tmp/state/shortcut
resolve_shell_resource
candidate_root=/tmp/candidates
stock_releases=/tmp/stock
overlay_releases=/tmp/releases
stock_overlay_state=/tmp/state/stock
"""


def run(body: str, root: bool = False) -> None:
    with tempfile.TemporaryDirectory(prefix="ggm-runtime-readonly-") as readonly:
        subprocess.run(
            [
                "bwrap", "--ro-bind", "/", "/", "--tmpfs", "/tmp",
                "--tmpfs", "/var/lib",
                "--dev", "/dev", "--proc", "/proc",
                "--ro-bind", readonly, "/tmp/readonly", "--unshare-all",
                *(["--uid", "0", "--gid", "0"] if root else []),
                "--die-with-parent", "bash", "-c", SETUP + body,
            ],
            check=True,
            timeout=120,
            env={**os.environ, "LC_ALL": "C.UTF-8"},
        )


run("""
empty="$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)"
[[ "$empty" == '@as []' ]]
[[ -z "$(list_custom_keybinding_paths "$empty")" ]]
binding_contains_super_l "@s '<Super>l'"
binding_contains_super_l "'<Super>L'"
for binding in "'<Super>less'" "'<Shift><Super>l'" "'<Control><Super>l'"; do
    if binding_contains_super_l "$binding"; then exit 1; fi
done
if binding_contains_super_l "'<Alt>l'"; then exit 1; fi
if (list_custom_keybinding_paths '@ai [1]'); then exit 1; fi
if binding_contains_super_l '@as []'; then exit 1; fi
apply_user_shortcut
[[ "$(gsettings get org.gnome.desktop.lockdown disable-lock-screen)" == false ]]
[[ "$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)" == "['$user_shortcut_path']" ]]
restore_user_shortcut
[[ "$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)" == '@as []' ]]
printf '%s\\n' 'Typed GVariant values and empty shortcut apply/restore: PASS'
""")

run("""
original=/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/original/
schema="org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$original"
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['$original']"
gsettings set "$schema" name "'Original Name'"
gsettings set "$schema" command "$previous_greeter_command_setting"
gsettings set "$schema" binding "'<Super>l'"
apply_user_shortcut
cp "$user_shortcut_state" /tmp/first-backup
apply_user_shortcut
cmp "$user_shortcut_state" /tmp/first-backup
python3 - "$user_shortcut_state" "$original" <<'PY'
import json
import pathlib
import sys
assert json.loads(pathlib.Path(sys.argv[1]).read_text())["path"] == sys.argv[2]
PY
restore_user_shortcut
[[ "$(gsettings get "$schema" name)" == "'Original Name'" ]]
[[ "$(gsettings get "$schema" command)" == "$previous_greeter_command_setting" ]]
[[ "$(gsettings get "$schema" binding)" == "'<Super>l'" ]]
[[ "$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)" == "['$original']" ]]
printf '%s\\n' 'Existing shortcut migration, stable backup and exact restore: PASS'
""")

for second_command in ("'/usr/bin/gnome-calculator'", "${greeter_command_setting}"):
    run(f"""
first=/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/first/
second=/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/second/
first_schema="org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$first"
second_schema="org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$second"
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['$first', '$second']"
gsettings set "$first_schema" name "'First original name'"
gsettings set "$first_schema" command "$greeter_command_setting"
gsettings set "$first_schema" binding "'<Super>l'"
gsettings set "$second_schema" name "'Second original name'"
gsettings set "$second_schema" command "{second_command}"
gsettings set "$second_schema" binding "'<Super>L'"
cp -r "$XDG_CONFIG_HOME" /tmp/settings-before
if (apply_user_shortcut); then exit 1; fi
[[ ! -e "$user_shortcut_state" ]]
diff -r /tmp/settings-before "$XDG_CONFIG_HOME"
printf '%s\\n' 'Ambiguous exact GTK accelerators rejected before backup or settings changes: PASS'
""")

for operation in ("stock", "overlay"):
    run(f"""
{operation}_releases=/tmp/readonly/releases
prepared_{operation}=stale
if prepare_{operation}_release; then exit 1; fi
[[ -z "$prepared_{operation}" ]]
[[ "$refresh_error" == *'Read-only file system'* ]]
[[ ! -e "$stock_overlay_state" ]]
printf '%s\\n' '{operation} publication on read-only filesystem: PASS'
""")

run("""
stock_overlay_state=/tmp/readonly/status
if prepare_stock_release; then exit 1; fi
[[ -z "$prepared_stock" ]]
[[ "$refresh_error" == *'Read-only file system'* ]]
[[ -d "$stock_releases/$(stock_fingerprint)" ]]
if prepare_stock_release; then exit 1; fi
[[ -z "$prepared_stock" ]]
[[ "$refresh_error" == *'Read-only file system'* ]]
printf '%s\\n' 'New and existing stock status on read-only filesystem: PASS'
""")

run(r"""
prepare_stock_release || { printf '%s\n' "$refresh_error" >&2; exit 1; }
[[ -d "$prepared_stock" ]]
[[ "$(cat "$stock_overlay_state")" == "$prepared_stock" ]]
prepare_overlay_release || { printf '%s\n' "$refresh_error" >&2; exit 1; }
[[ -d "$prepared_overlay" ]]
python3 - "$prepared_overlay" "$shell_resource" <<'PY'
from pathlib import Path
import re
import subprocess
import sys

release = Path(sys.argv[1])
stock = subprocess.check_output(
    ["gresource", "extract", sys.argv[2], "/org/gnome/shell/ui/screenShield.js"], text=True
)
generated = (release / "ui/screenShield.js").read_text()

def method(source: str, name: str) -> str:
    match = re.search(r"    (?:async )?" + re.escape(name) + r"\([^\n]*\) \{\n(.*?)\n    \}", source, re.S)
    assert match is not None, name
    return match[1]

assert method(stock, "lock") == method(generated, "_lockSession")
assert method(generated, "_setLocked").removeprefix(
    "        if (!locked)\n            this._greeterSwitchDone = false;\n"
) == method(stock, "_setLocked")
assert method(generated, "deactivate").removeprefix(
    "        if (!Main.sessionMode.isGreeter) {\n"
    "            this._greeterUnlocking = true;\n"
    "            this._greeterSwitchDone = false;\n"
    "        }\n"
) == method(stock, "deactivate")
assert method(generated, "_completeDeactivate").removesuffix(
    "\n        this._greeterUnlocking = false;\n        this.emit('deactivated');"
) == method(stock, "_completeDeactivate")
for name in ("_syncInhibitor", "_continueDeactivate", "_prepareForSleep"):
    assert method(stock, name) == method(generated, name), name
for path in release.rglob("*.js"):
    subprocess.run(
        ["gjs", "-c", "const Gio=imports.gi.Gio; const ByteArray=imports.byteArray; const [,data]=Gio.File.new_for_path(ARGV[0]).load_contents(null); Reflect.parse(ByteArray.toString(data), {target:'module'});", str(path)],
        check=True,
    )
PY
printf '%s\n' 'Real stock and customized GResource publication: PASS'
""")

run(r"""
old_fingerprint="$(python3 - "$shell_resource" "$(active_theme_path)" <<'PY'
import hashlib
from pathlib import Path
import sys
digest = hashlib.sha256()
for path in map(Path, sys.argv[1:]):
    content = path.read_bytes()
    digest.update(len(content).to_bytes(8, "big"))
    digest.update(content)
print(digest.hexdigest()[:24])
PY
)"
installed_stock=/usr/local/share/gnome-shell-overrides/greeter-controls/stock-releases/$old_fingerprint
[[ -d "$installed_stock" && ! -e "$installed_stock/ui/shellDBus.js" ]]
mkdir -p "$stock_releases"
cp -r "$installed_stock" "$stock_releases/$old_fingerprint"
find "$stock_releases/$old_fingerprint" -type f -exec sha256sum '{}' + >/tmp/old-stock-sha
prepare_stock_release || { printf '%s\n' "$refresh_error" >&2; exit 1; }
[[ "$prepared_stock" != "$stock_releases/$old_fingerprint" ]]
[[ -f "$prepared_stock/ui/shellDBus.js" ]]
sha256sum --check /tmp/old-stock-sha
[[ ! -e "$stock_releases/$old_fingerprint/ui/shellDBus.js" ]]
verify_stock_overlay "$prepared_stock"
printf '%s\n' 'Installed legacy stock copy preserved; new resource scope generates distinct stock: PASS'
""")

run("""
if (backup_user_shortcut "$user_shortcut_path"); then exit 1; fi
[[ ! -e "$user_shortcut_state" ]]
gdm_input_state=/tmp/state/input
gdm_background_state=/tmp/state/background
gdm_accent_state=/tmp/state/accent
for action in input_sources background accent; do
    if "backup_gdm_$action"; then exit 1; fi
done
[[ ! -e "$gdm_input_state" && ! -e "$gdm_background_state" && ! -e "$gdm_accent_state" ]]
restore_gdm_input_sources
restore_gdm_background
restore_gdm_accent
greeter_sound_theme_dir=/tmp/sounds
remove_greeter_sound_theme
mkdir -p "$greeter_sound_theme_dir/stereo"
printf '%s\\n' keep >"$greeter_sound_theme_dir/stereo/foreign"
if (remove_greeter_sound_theme); then exit 1; fi
[[ "$(cat "$greeter_sound_theme_dir/stereo/foreign")" == keep ]]
printf '%s\\n' 'Failed real session/dconf reads leave backups absent; partial restore and missing sounds: PASS'
""", root=True)

run("""
mkdir -p /tmp/dropins /tmp/victim
printf '%s\\n' original >/tmp/victim/managed.conf
ln -s /tmp/victim /tmp/dropins/ancestor
if write_dropin_file /tmp/dropins/ancestor/managed.conf; then exit 1; fi
if remove_dropin_file /tmp/dropins/ancestor/managed.conf; then exit 1; fi
[[ "$(cat /tmp/victim/managed.conf)" == original ]]
mkdir -p /tmp/dropins/real
ln -s /tmp/victim/managed.conf /tmp/dropins/real/managed.conf
printf '%s\\n' unrelated >/tmp/dropins/real/foreign
chmod 600 /tmp/dropins/real/foreign
write_dropin_file /tmp/dropins/real/managed.conf
[[ ! -L /tmp/dropins/real/managed.conf ]]
[[ "$(cat /tmp/victim/managed.conf)" == original ]]
[[ "$(stat -c %a /tmp/dropins/real/foreign)" == 600 ]]
grep -Fx "Environment=G_RESOURCE_OVERLAYS=$(overlay_env)" /tmp/dropins/real/managed.conf
remove_dropin_file /tmp/dropins/real/managed.conf
remove_dropin_file /tmp/dropins/missing/managed.conf
write_dropin_file /tmp/dropins/new/parent/managed.conf
[[ -f /tmp/dropins/new/parent/managed.conf ]]
[[ "$(stat -c %a /tmp/dropins/new/parent/managed.conf)" == 644 ]]
printf '%s\\n' 'Directory-FD publication/removal reject symlink ancestors and preserve foreign files: PASS'
""", root=True)
