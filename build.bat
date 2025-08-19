@echo off
set APP_NAME="Projects Manager"

pyinstaller --noconsole --onefile ^
            --name=%APP_NAME% main.py

echo.
echo Executable build complete.
pause
