#!/usr/bin/env python3
"""Windows port of timerCLI.py.

Uses user32's GetLastInputInfo() to get the timestamp of the last
keyboard/mouse (session-wide) input, instead of reading /dev/input/event*.
No admin rights or extra packages are needed — standard library only.
"""
import ctypes
import os
import sys
import time
from ctypes import wintypes

IDLE_LIMIT = 30  # seconds


class InputWatcher:
    """Reports seconds since the last keyboard/mouse input (Windows)."""

    class _LastInputInfo(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]

    def __init__(self):
        # Windows-only APIs; type: ignore keeps non-Windows linters quiet.
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)  # type: ignore[attr-defined]
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
        self._kernel32.GetTickCount64.restype = ctypes.c_uint64
        try:
            _ = self.idle  # verify the APIs work before we start the loop
        except OSError as e:
            print(f"ERROR: Cannot query Windows input state: {e}")
            sys.exit(1)

    @property
    def idle(self):
        """Seconds since the last input event (float)."""
        lii = self._LastInputInfo()
        lii.cbSize = ctypes.sizeof(self._LastInputInfo)
        if not self._user32.GetLastInputInfo(ctypes.byref(lii)):
            raise OSError(ctypes.get_last_error(), "GetLastInputInfo failed")  # type: ignore[attr-defined]
        # GetTickCount64 avoids the 49.7-day wraparound of GetTickCount.
        return (self._kernel32.GetTickCount64() - lii.dwTime) / 1000.0

    def close(self):
        pass  # nothing to release


def fmt_duration(seconds):
    """Format seconds as MM:SS, or H:MM:SS once an hour is reached."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    if os.name != "nt":
        print("ERROR: timerCLI_windows.py only runs on Windows.")
        print("  Use timerCLI.py on Linux.")
        sys.exit(1)

    watch = InputWatcher()

    print("Tracking system input activity (GetLastInputInfo).")
    print(f"Pauses after {IDLE_LIMIT}s idle. Ctrl+C to stop.\n")

    start = time.monotonic()
    paused_total = 0.0
    pause_start = None

    try:
        while True:
            idle = watch.idle

            if idle >= IDLE_LIMIT:
                pause_start = time.monotonic()
                print(f"\n\u23f8  Idle {int(idle)}s \u2014 pausing\u2026")
                while (cur := watch.idle) >= IDLE_LIMIT:
                    time.sleep(1)
                paused_total += time.monotonic() - pause_start
                print("\u25b6  Resumed.\n")
                idle = cur  # refresh stale idle value after pause

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
