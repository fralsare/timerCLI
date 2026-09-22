#add this for permission - sudo usermod -aG input $USER
import os, glob, time, sys 

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


def main():
    watch = InputWatcher()

    if not watch._fds:
        print("ERROR: Cannot read /dev/input/event* (no permission).")
        print(f"  You need to be in the 'input' group:")
        print(f"    sudo usermod -aG input $USER")
        print(f"  Then log out and back in.")
        sys.exit(1)

    print(f"Watching {len(watch._fds)} input device(s).")
    print(f"Pauses after {IDLE_LIMIT}s idle. Ctrl+C to stop.\n")

    start = time.monotonic()
    paused_total = 0.0

    try:
        while True:
            idle = watch.idle

            if idle >= IDLE_LIMIT:
                pause_start = time.monotonic()
                print(f"\n\u23f8  Idle {int(idle)}s \u2014 pausing\u2026")
                while watch.idle >= IDLE_LIMIT:
                    time.sleep(1)
                paused_total += time.monotonic() - pause_start
                print("\u25b6  Resumed.\n")
                idle = watch.idle  # changed: refresh stale idle value after pause

            active = time.monotonic() - start - paused_total
            sys.stdout.write(f"\rIdle: {int(idle):3d}s | Active: {int(active//60):02d}:{int(active%60):02d}   ")
            sys.stdout.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        if pause_start is not None:  # changed: account for pause in progress
            paused_total += time.monotonic() - pause_start
        active = time.monotonic() - start - paused_total
        print(f"\nStopped. Active: {int(active//60)}m {int(active%60)}s | Paused: {int(paused_total)}s")
    finally:
        watch.close()


if __name__ == "__main__":
    main()
