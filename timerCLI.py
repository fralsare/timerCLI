#!/usr/bin/env python3
import glob
import os
import sys
import time

IDLE_LIMIT = 30  # seconds


class InputWatcher:
    """Watches /dev/input/event* for any keyboard/mouse/touch activity."""

    def __init__(self):
        self.last_event = time.monotonic()
        self._fds = []
        for path in sorted(glob.glob('/dev/input/event*')):
            try:
                fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                self._fds.append(fd)
            except PermissionError:
                continue

    @property
    def idle(self):
        """Seconds since last input event. Returns None if no devices readable."""
        # Returns None only if no device could be opened at startup.
        # If fds exist but all reads fail later (e.g. permissions revoked
        # mid-run), we still report real elapsed time — the timer will pause.
        if not self._fds:
            return None
        for fd in self._fds:
            try:
                if os.read(fd, 64):  # drain pending events
                    self.last_event = time.monotonic()
            except (BlockingIOError, OSError):
                pass  # no data right now — that's normal
        return time.monotonic() - self.last_event

    def close(self):
        for fd in self._fds:
            os.close(fd)


def fmt_duration(seconds):
    """Format seconds as MM:SS, or H:MM:SS once an hour is reached."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    watch = InputWatcher()

    if not watch._fds:
        print("ERROR: Cannot read /dev/input/event* (no permission).")
        print("  You need to be in the 'input' group:")
        print("    sudo usermod -aG input $USER")
        print("  Then log out and back in.")
        sys.exit(1)

    print(f"Watching {len(watch._fds)} input device(s).")
    print(f"Pauses after {IDLE_LIMIT}s idle. Ctrl+C to stop.\n")

    start = time.monotonic()
    paused_total = 0.0
    pause_start = None

    try:
        while True:
            idle = watch.idle
            if idle is None:  # no readable devices (e.g. lost permission) — keep running
                time.sleep(1)
                continue

            if idle >= IDLE_LIMIT:
                pause_start = time.monotonic()
                print(f"\n\u23f8  Idle {int(idle)}s \u2014 pausing\u2026")
                while (cur := watch.idle) is not None and cur >= IDLE_LIMIT:
                    time.sleep(1)
                paused_total += time.monotonic() - pause_start
                print("\u25b6  Resumed.\n")
                idle = cur if cur is not None else 0.0  # refresh stale idle value after pause

            active = time.monotonic() - start - paused_total
            sys.stdout.write(f"\rIdle: {int(idle):3d}s | Active: {fmt_duration(active)}   ")
            sys.stdout.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        if pause_start is not None:  # account for pause in progress
            paused_total += time.monotonic() - pause_start
        active = time.monotonic() - start - paused_total
        print(f"\nStopped. Active: {fmt_duration(active)} | Paused: {fmt_duration(paused_total)}")
    finally:
        watch.close()


if __name__ == "__main__":
    main()
