import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def isolated(root: str) -> None:
    os.umask(0o022)
    sys.dont_write_bytecode = True
    source = Path(__file__).resolve().parents[1] / "scripts/overlay-extension.py"
    spec = importlib.util.spec_from_file_location("overlay_extension", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load extension runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    os.chroot(root)
    os.chdir("/")
    os.chmod("/", 0o755)
    releases = Path("/releases")
    target = releases / "valid"
    target.mkdir(parents=True)
    resource = target / "resource.js"
    resource.write_text("export const enabled = true;\n")
    resource.chmod(0o644)
    module.release(target, releases)
    rejected = 0

    def reject(path: Path) -> None:
        nonlocal rejected
        try:
            module.release(path, releases)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError(f"Unsafe path accepted: {path}")

    resource.chmod(0o666)
    reject(target)
    resource.chmod(0o644)
    alias = target / "alias.js"
    alias.symlink_to(resource)
    reject(target)
    alias.unlink()
    os.link(resource, alias)
    reject(target)
    alias.unlink()
    releases.chmod(0o777)
    reject(target)
    releases.chmod(0o755)
    nested = target / "nested"
    nested.mkdir()
    reject(nested)
    reject(Path("releases/valid"))
    module.release(target, releases)
    assert rejected == 6
    print("Extension paths: trusted release accepted; six unsafe paths rejected")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--isolated":
        isolated(sys.argv[2])
    else:
        if os.geteuid() == 0:
            raise RuntimeError("Run as unprivileged user")
        with tempfile.TemporaryDirectory(prefix="ggm-extension-test-") as root:
            subprocess.run(
                ["unshare", "--user", "--map-root-user", sys.executable, __file__, "--isolated", root],
                check=True,
                timeout=30,
            )
