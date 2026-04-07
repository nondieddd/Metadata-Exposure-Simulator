## ⚠️ Disclaimer
**This project is for educational and security research purposes only.**
The author is not responsible for any misuse of this tool. It was developed to explore how unauthorized scripts can interact with the Windows API, extract network metadata, and take control of system peripherals.

## Technical Features
- **Network Metadata Extraction:** Uses external APIs and local sub-processes (`arp -a`, `netstat`)
- **Win32 API Integration:** Direct interaction with `user32.dll` to hide the taskbar and manage window focus.
- **Low-Level Keyboard Hooking:** Blocks system-level hotkeys (Windows Key, Alt+Tab, Alt+F4)
- **Hardware Interaction:** Uses `pycaw` (Python Common Audio Windows) for direct hardware volume manipulation, bypassing the OS visual feedback (OSD).
- **Asynchronous Execution:** Implements Python's `threading` module to handle concurrent audio playback, UI rendering, and erratic peripheral movement.

## How it Works
The script initializes a full-screen, top-most Tkinter environment that claims system focus every 10ms. It simultaneously runs multiple threads:
1. **Network Thread:** Fetches geolocation and local routing tables.
2. **Input Thread:** Erratically moves the cursor using `pyautogui`.
3. **Media Thread:** Forces system volume to 100% and loops multiple audio streams via PowerShell background processes.

## 🛑 Termination
The simulation can be terminated at any time by pressing the [ N ] key, which triggers a clean-up process (unhooking keys, killing background processes, and restoring the taskbar).
