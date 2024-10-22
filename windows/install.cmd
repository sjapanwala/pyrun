@echo off
setlocal enabledelayedexpansion

set notify=PYRUN INSTALLER
set folderpath=C:\.pyrun

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [%notify%] Requesting Admin Privileges To Continue Installation
    powershell -Command "Start-Process cmd -ArgumentList '/c %~f0' -Verb RunAs"
    exit /b
)

:STARTINSTALLATION
:: Your commands that require admin privileges go here
python --version >nul 2>&1
if not %errorLevel% == 0 (
    echo [%notify%] Installing Python
    winget install --id 9NRWMJP3717K --accept-package-agreements --silent >nul
    if %errorLevel% == 0 (
        echo [%notify%] Installed Python Successfully
    )
)

:: Check for pip
pip --version >nul 2>&1
if not %errorLevel% == 0 (
    echo [%notify%] Installing PIP
    python -m ensurepip --default-pip >nul 2>&1
    if %errorLevel% == 0 (
        echo [%notify%] Installed PIP Successfully
    ) else (
        echo [%notify%] Failed to Install PIP
    )
) else (
    echo [%notify%] PIP Is Already Installed
)

:: Create the directory if it doesn't exist
if not exist %folderpath% (
    mkdir %folderpath%
)

:: Add folder to PATH
setx PATH "%PATH%;%folderpath%" >nul

:: Download the app file
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/sjapanwala/pyrun/refs/heads/main/windows/pyrun.py' -OutFile '%folderpath%\pyrun.py'"

:: Download the shortcut file
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/sjapanwala/pyrun/refs/heads/main/windows/pyrun.bat' -OutFile '%folderpath%\pyrun.bat'"

echo [%notify%] Installation Complete!
