#!/usr/bin/python3 -I
import os
from pathlib import Path
import select
import signal
import stat
import subprocess
import sys
import time


def run(provider: Path, mode: str, target: Path) -> bytes:
    signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)
    process: subprocess.Popen[bytes] | None = None
    interruption: int | None = None

    def interrupted(number: int, frame: object) -> None:
        nonlocal interruption
        interruption = number
        if process is not None:
            raise ValueError(f"Extension operation interrupted by signal {number}")

    handlers = {number: signal.signal(number, interrupted) for number in signals}
    try:
        process = subprocess.Popen(
            [str(provider), mode, str(target)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            env={**os.environ, "PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C.UTF-8", "GGM_OVERLAY_LOCK_FD": "9"},
            close_fds=False,
            start_new_session=True,
        )
        if interruption is not None:
            raise ValueError(f"Extension operation interrupted by signal {interruption}")
        assert process.stdout is not None
        os.set_blocking(process.stdout.fileno(), False)
        deadline = time.monotonic() + 60
        limit = 4096 if mode == "prepare" else 0
        data = bytearray()
        eof = False
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("Extension operation exceeded 60 seconds")
            ready = [] if eof else select.select([process.stdout], [], [], min(remaining, 0.1))[0]
            if ready:
                chunk = os.read(process.stdout.fileno(), limit + 1 - len(data))
                data.extend(chunk)
                eof = not chunk
                if len(data) > limit:
                    message = "Extension prepare output exceeds 4096 bytes" if limit else "Extension commit must not produce stdout"
                    raise ValueError(message)
            code = process.poll()
            if code is not None:
                if code:
                    raise ValueError(f"Extension {mode} failed with status {code}")
                if not eof and select.select([process.stdout], [], [], 0)[0]:
                    continue
                return bytes(data)
            if eof:
                time.sleep(min(remaining, 0.1))
    finally:
        previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, signals)
        try:
            if process is not None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
                if process.stdout is not None:
                    process.stdout.close()
        finally:
            for number, handler in handlers.items():
                signal.signal(number, handler)
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


def trusted(path: Path, directory: bool) -> None:
    if not path.is_absolute() or path.resolve(strict=True) != path:
        raise ValueError(f"Noncanonical extension path: {path}")
    for item in (*reversed(path.parents), path):
        info = item.lstat()
        expected_directory = item != path or directory
        correct_type = stat.S_ISDIR(info.st_mode) if expected_directory else stat.S_ISREG(info.st_mode)
        if not correct_type or info.st_uid != 0 or info.st_gid != 0 or info.st_mode & 0o022:
            raise ValueError(f"Untrusted extension path: {item}")
        if not expected_directory and info.st_nlink != 1:
            raise ValueError(f"Linked extension file: {item}")


def release(path: Path, releases: Path) -> None:
    trusted(releases, True)
    trusted(path, True)
    if path.parent != releases:
        raise ValueError("Extension release must be a direct child of releases")
    for item in path.rglob("*"):
        trusted(item, item.is_dir())


def main() -> None:
    mode, provider_text, releases_text, target_text = sys.argv[1:]
    if mode not in ("prepare", "commit"):
        raise ValueError("Unknown extension operation")
    provider = Path(provider_text)
    releases = Path(releases_text)
    target = Path(target_text)
    trusted(provider, False)
    if not os.access(provider, os.X_OK):
        raise ValueError("Extension provider is not executable")
    release(target, releases)
    data = run(provider, mode, target)
    if mode == "commit":
        return
    if not data.endswith(b"\n") or data.count(b"\n") != 1:
        raise ValueError("Extension prepare must return exactly one release path")
    text = data[:-1].decode("utf-8", errors="strict")
    if "\r" in text or "\x00" in text:
        raise ValueError("Invalid extension release path")
    result = Path(text)
    if str(result) != text:
        raise ValueError("Noncanonical extension release output")
    release(result, releases)
    print(result)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Overlay extension: {error}", file=sys.stderr)
        sys.exit(1)
