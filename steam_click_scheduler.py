#!/usr/bin/env python3
"""Daily Windows mouse-click scheduler; no Steam controls or dependencies."""
"Created By samiop12"
"Steam Tool : game Downloader"

# Edit these settings before running. Coordinates are screen pixels.
START_TIME = '3:28 PM'
END_TIME = '3:29 PM'
X = 1493
Y = 250

import ctypes
import os
import time
from datetime import datetime, timedelta

TIME_FORMAT = '%I:%M %p'
LEFTDOWN = 0x0002
LEFTUP = 0x0004


def parse_time(value):
    """Parse a 12-hour time such as '2:00 AM' or '11:30 PM'."""
    try:
        return datetime.strptime(value.strip(), TIME_FORMAT).time()
    except (AttributeError, ValueError) as exc:
        raise ValueError(f'Invalid time {value!r}; use a value such as 2:00 AM.') from exc


def next_cycle(now, start_time, end_time):
    """Return the next start strictly after now and its matching later end."""
    start = datetime.combine(now.date(), start_time)
    if start <= now:
        start += timedelta(days=1)
    end = datetime.combine(start.date(), end_time)
    if end <= start:
        end += timedelta(days=1)
    return start, end


def click_windows(x, y):
    """Move to the exact requested pixel and send one left-button click."""
    if os.name != 'nt':
        raise OSError('This script requires Windows.')
    user32 = ctypes.windll.user32
    if not user32.SetCursorPos(int(x), int(y)):
        raise OSError(f'Windows could not move the cursor to ({x}, {y}).')
    user32.mouse_event(LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(LEFTUP, 0, 0, 0, 0)


def wait_until(target):
    """Poll the system clock, sleeping no more than 30 seconds per check."""
    while True:
        remaining = (target - datetime.now()).total_seconds()
        if remaining <= 0:
            return
        time.sleep(min(30, max(1, remaining)))


def main():
    if not isinstance(X, int) or not isinstance(Y, int):
        raise ValueError('X and Y must be integer screen coordinates.')
    start_time = parse_time(START_TIME)
    end_time = parse_time(END_TIME)
    if os.name != 'nt':
        raise OSError('This script runs on Windows only.')

    print('Daily scheduler started. Press Ctrl+C to quit.')
    print('Each event sends one click only; Resume/Pause is not guaranteed and depends on the same unchanged Steam toggle button remaining visible.')
    now = datetime.now()
    while True:
        start, end = next_cycle(now, start_time, end_time)
        print(f'Next start: {start:%Y-%m-%d %I:%M %p}; next end: {end:%Y-%m-%d %I:%M %p}', flush=True)

        wait_until(start)
        # If the computer was asleep for the whole interval, skip it rather than
        # issuing a late start and end pair.
        if datetime.now() >= end:
            print(f'Skipped missed cycle ({start} to {end}).', flush=True)
            now = datetime.now()
            continue
        click_windows(X, Y)
        print(f'Start action: moved to ({X}, {Y}) and clicked once at {datetime.now():%Y-%m-%d %I:%M:%S %p}.', flush=True)

        wait_until(end)
        click_windows(X, Y)
        print(f'End action: moved to ({X}, {Y}) and clicked once at {datetime.now():%Y-%m-%d %I:%M:%S %p}.', flush=True)
        now = datetime.now()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Scheduler stopped by Ctrl+C.')
