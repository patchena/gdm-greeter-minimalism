import fcntl
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time


SOURCE = Path(__file__).resolve().parents[1] / "scripts/overlay-extension.py"


def provider(case: Path) -> None:
    assert os.environ["GGM_OVERLAY_LOCK_FD"] == "9"
    assert os.environ["SECURITY_CHAIN_LOCK_FD"] == "10"
    for descriptor in (9, 10):
        assert os.fstat(descriptor).st_ino == (case.parent / str(descriptor)).stat().st_ino
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    child = os.fork()
    if child == 0:
        (case.parent / "child").write_text(str(os.getpid()))
        while True:
            signal.pause()
    while not (case.parent / "child").exists():
        time.sleep(0.01)
    (case.parent / "ready").write_text(str(os.getpid()))
    if case.name == "normal":
        os.write(1, b"/releases/valid\n")
        return
    if case.name == "failure":
        sys.exit(7)
    if case.name == "empty":
        return
    if case.name == "boundary":
        os.write(1, b"a" * 4096)
        return
    if case.name in ("overflow", "commit"):
        while True:
            os.write(1, b"a" * 65536)
    while True:
        signal.pause()


def runner(provider_path: str, mode: str, case: str) -> None:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("overlay_extension", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load extension runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        data = module.run(Path(provider_path), mode, Path(case))
        sys.stdout.buffer.write(data)
    except (OSError, ValueError) as error:
        print(f"Overlay extension: {error}", file=sys.stderr)
        sys.exit(1)


def wait_ready(path: Path, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 5
    while not path.exists():
        if process.poll() is not None or time.monotonic() >= deadline:
            raise AssertionError("Provider did not become ready")
        time.sleep(0.01)


def isolated() -> None:
    cases = ("normal", "empty", "failure", "boundary", "overflow", "commit", "SIGTERM", "SIGINT", "SIGHUP", "timeout")
    with tempfile.TemporaryDirectory(prefix="ggm-extension-runtime-") as directory:
        root = Path(directory)
        provider_path = root / "provider"
        provider_path.write_text(f"#!{sys.executable}\nimport runpy\nrunpy.run_path({str(Path(__file__).resolve())!r}, run_name='__main__')\n")
        provider_path.chmod(0o755)
        for name in cases:
            case_root = root / name
            case_root.mkdir()
            for descriptor in (9, 10):
                opened = os.open(case_root / str(descriptor), os.O_RDWR | os.O_CREAT, 0o600)
                os.dup2(opened, descriptor, inheritable=True)
                if opened != descriptor:
                    os.close(opened)
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            started = time.monotonic()
            process = subprocess.Popen(
                [sys.executable, __file__, "--runner", str(provider_path), "commit" if name in ("commit", "empty") else "prepare", str(case_root / name)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                pass_fds=(9, 10),
                env={**os.environ, "SECURITY_CHAIN_LOCK_FD": "10"},
            )
            os.close(9)
            os.close(10)
            try:
                if name.startswith("SIG"):
                    wait_ready(case_root / "ready", process)
                    process.send_signal(getattr(signal, name))
                output, errors = process.communicate(timeout=65 if name == "timeout" else 8)
                elapsed = time.monotonic() - started
                if name == "normal":
                    assert process.returncode == 0 and output == b"/releases/valid\n" and not errors
                elif name == "empty":
                    assert process.returncode == 0 and not output and not errors
                elif name == "boundary":
                    assert process.returncode == 0 and output == b"a" * 4096 and not errors
                else:
                    assert process.returncode == 1 and not output, (name, process.returncode, output, errors)
                    expected = {
                        "failure": b"status 7",
                        "overflow": b"exceeds 4096 bytes",
                        "commit": b"must not produce stdout",
                        "timeout": b"exceeded 60 seconds",
                    }.get(name, b"interrupted by signal")
                    assert expected in errors, (name, errors)
                assert elapsed >= 60 if name == "timeout" else elapsed < 8
                for descriptor in (9, 10):
                    with (case_root / str(descriptor)).open("r+") as lock:
                        deadline = time.monotonic() + 2
                        while True:
                            try:
                                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                                break
                            except BlockingIOError:
                                if time.monotonic() >= deadline:
                                    raise AssertionError(f"{name}: inherited lock remains held")
                                time.sleep(0.01)
                print(f"Extension runtime: {name} passed", flush=True)
            finally:
                if process.poll() is None:
                    process.send_signal(signal.SIGTERM)
                    process.wait(timeout=5)
                for identity in ("ready", "child"):
                    path = case_root / identity
                    if path.exists():
                        pid = int(path.read_text())
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ("prepare", "commit"):
        provider(Path(sys.argv[2]))
    elif len(sys.argv) == 5 and sys.argv[1] == "--runner":
        runner(*sys.argv[2:])
    elif sys.argv[1:] == ["--isolated"]:
        isolated()
    else:
        if os.geteuid() == 0:
            raise RuntimeError("Run as unprivileged user")
        subprocess.run(
            ["unshare", "--user", "--map-root-user", "--pid", "--fork", "--mount-proc", sys.executable, __file__, "--isolated"],
            check=True,
            timeout=90,
        )
