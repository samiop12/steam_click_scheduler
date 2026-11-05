For Find X And Y Enter This CMD in PowerShell
py -c "import ctypes, ctypes.wintypes, time; pt = ctypes.wintypes.POINT(); [print(f'\rX: {pt.x:4d} | Y: {pt.y:4d}   ', end='', flush=True) or time.sleep(0.05) for _ in iter(lambda: ctypes.windll.user32.GetCursorPos(ctypes.byref(pt)), 0)]"
