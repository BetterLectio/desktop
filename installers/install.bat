@echo off
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'"
    exit /b
)

echo

rmdir /S /Q "%Temp%\betterlectio"

mkdir "%Temp%\betterlectio"
cd "%Temp%\betterlectio"

curl -O -L https://github.com/BetterLectio/desktop/releases/download/0.0.1/betterlectio-win.zip

mkdir "C:\Program Files\betterlectio"
tar -xf betterlectio-win.zip -C "C:\Program Files\betterlectio"

mkdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\betterlectio"

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\betterlectio\Better Lectio.lnk');$s.TargetPath='C:\Program Files\betterlectio\BetterLectio.exe';$s.Arguments='connect';$s.IconLocation='C:\Program Files\betterlectio\BetterLectio.exe';$s.WorkingDirectory='C:\Program Files\betterlectio';$s.WindowStyle=7;$s.Save()"