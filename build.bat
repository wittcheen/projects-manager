@echo off
set APP_NAME="Projects Manager"

pyinstaller --noconsole --onefile ^
            --icon=icon.ico ^
            --add-data "icon.ico;." ^
            --name=%APP_NAME% main.py

echo.
echo Executable build complete.
pause
