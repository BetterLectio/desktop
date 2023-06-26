import tkinter as tk
from PIL import ImageTk, Image
from threading import Thread

import tempfile
import platform
import os
import subprocess

system = platform.system()

windowSize = [300, 400]
iconSize = [125, 125]

win = tk.Tk()

win.geometry(f"{windowSize[0]}x{windowSize[1]}")
if system == "Windows":
    win.overrideredirect(True)
    win.eval("tk::PlaceWindow . center")
else:
    win.wm_attributes("-type", "splash")
win.configure(bg="#2A303C")

# https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
def start_move(event):
    win.x = event.x
    win.y = event.y

def stop_move(event):
    win.x = None
    win.y = None

def do_move(event):
    deltax = event.x - win.x
    deltay = event.y - win.y
    x = win.winfo_x() + deltax
    y = win.winfo_y() + deltay
    win.geometry(f"+{x}+{y}")

win.bind("<ButtonPress-1>", start_move)
win.bind("<ButtonRelease-1>", stop_move)
win.bind("<B1-Motion>", do_move)

canvas = tk.Canvas(win, width=iconSize[0], height=iconSize[1], bg="#2A303C", highlightthickness=0)
canvas.place(x=windowSize[0]/2, y=windowSize[1]/2.5, anchor="center")

icon = Image.open("./images/favicon.png")
icon = icon.resize((iconSize[0], iconSize[1]), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)
canvas.create_image(iconSize[0]/2, iconSize[1]/2, anchor="center", image=icon)

status = tk.StringVar()
statusLabel = tk.Label(win, textvariable=status, bg="#2A303C", fg="#A6ADBB", bd=0)
status.set("Begynder installationen af BetterLectio")
statusLabel.place(x=windowSize[0]/2, y=windowSize[1]/4*3, anchor="center")

def installer():
    folder = tempfile.gettempdir()

    if system == "Linux":
        updateStatus("Spørger om adgang")
        adgangskode = subprocess.Popen("echo $(zenity --password --title=\"Skriv din sudo adgangskode\")", stdout=subprocess.PIPE, shell=True, text="Text").communicate()[0].strip()

        updateStatus(f"Klargøre mapperne")
        os.system(f"rm -rf {folder}/betterlectio_temp && $echo {adgangskode} | sudo -S rm -rf /usr/share/betterlectio/ && mkdir {folder}/betterlectio_temp && $echo {adgangskode} | sudo -S mkdir /usr/share/app-logos")

        updateStatus("Henter BetterLectio")
        os.system(f"""
        cd {folder}/betterlectio_temp &&
        wget https://github.com/BetterLectio/desktop/releases/download/0.0.1/betterlectio-linux.zip &&
        wget https://raw.githubusercontent.com/BetterLectio/betterLectio/main/static/favicon.png --output-document=betterlectio.png &&
        wget https://raw.githubusercontent.com/BetterLectio/desktop/main/installers/betterlectio.desktop
        """)

        updateStatus("Installerer BetterLectio")
        os.system(f"""
        $echo {adgangskode} | sudo -S unzip {folder}/betterlectio_temp/betterlectio-linux.zip -d /usr/share/betterlectio/ &&
        $echo {adgangskode} | sudo -S mv {folder}/betterlectio_temp/betterlectio.png /usr/share/app-logos/
        $echo {adgangskode} | sudo -S mv {folder}/betterlectio_temp/betterlectio.desktop /usr/share/applications/
        """)

        updateStatus("Ryder op")
        os.system(f"$echo {adgangskode} | sudo -S rm -rf {folder}/betterlectio_temp")

        updateStatus("BetterLectio blev installeret succesfuldt")
        win.quit()

    elif system == "Windows":
        updateStatus("Spørger om adgang")
        ###

        updateStatus(f"Klargøre mapperne")
        os.system("rmdir /S /Q \"%Temp%\\betterlectio\"")
        os.system("rmdir /S /Q C:\\Program Files\\betterlectio")
        os.system("rmdir /S /Q C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\betterlectio")

        os.system("mkdir \"%Temp%\\betterlectio\"")
        os.system("mkdir \"C:\\Program Files\\betterlectio\"")
        os.system("mkdir \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\betterlectio\"")

        updateStatus(f"Henter BetterLectio")
        os.system("cd \"%Temp%\\betterlectio\" && curl -O -L https://github.com/BetterLectio/desktop/releases/download/0.0.1/betterlectio-win.zip")

        updateStatus("Installerer BetterLectio")
        os.system("tar -xf \"%Temp%\\betterlectio\\betterlectio-win.zip\" -C \"C:\\Program Files\\betterlectio\"")
        os.system("powershell \"$s=(New-Object -COM WScript.Shell).CreateShortcut('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\betterlectio\Better Lectio.lnk');$s.TargetPath='C:\Program Files\betterlectio\BetterLectio.exe';$s.Arguments='connect';$s.IconLocation='C:\Program Files\betterlectio\BetterLectio.exe';$s.WorkingDirectory='C:\Program Files\betterlectio';$s.WindowStyle=7;$s.Save()\"")

        updateStatus("Ryder op")
        os.system("rmdir /S /Q \"%Temp%\\betterlectio\"")

        updateStatus("BetterLectio blev installeret succesfuldt")
        win.quit()


def updateStatus(message):
    status.set(message)


thread = Thread(target=installer)
thread.start()

win.mainloop()
exit()