@echo off
setlocal enabledelayedexpansion

:: === CONFIG ===
set "APP_NAME=Wdb"
set "CURRENT_EXE=Wdb.exe"
set "NEW_EXE=Wdb_new.exe"
set "UPDATE_URL=https://github.com/fariasjim/wordbuddy/releases/latest/download/Wdb.exe"
set "VERSION_URL=https://raw.githubusercontent.com/fariasjim/wordbuddy/main/version.txt"
set "CURRENT_VERSION=1.0.2[1]"

echo ========================================
echo Checking for updates...
echo ========================================

:: === GET LATEST VERSION ===
powershell -Command "(New-Object Net.WebClient).DownloadString('%VERSION_URL%')" > latest_version.txt
set /p LATEST_VERSION=<latest_version.txt
del latest_version.txt

echo Latest version available: %LATEST_VERSION%
echo.

:: === DOWNLOAD NEW VERSION ===
echo Downloading update...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%UPDATE_URL%', '%NEW_EXE%')"

if not exist "%NEW_EXE%" (
    echo ERROR: Failed to download update.
    pause
    exit /b
)

echo Update downloaded successfully!
echo.

:: === REPLACE LOCAL EXECUTABLE ===
echo Replacing local %CURRENT_EXE%...
if exist "%CURRENT_EXE%" del "%CURRENT_EXE%"
rename "%NEW_EXE%" "%CURRENT_EXE%"
echo Local executable updated.
echo.

:: === REPLACE EXECUTABLE IN PATH FOLDERS ===
echo Searching PATH directories for %CURRENT_EXE%...
echo.

for %%D in ("%PATH:;=" "%") do (
    if exist "%%~D\%CURRENT_EXE%" (
        echo Found: %%~D\%CURRENT_EXE%
        echo Replacing...

        :: Delete old one
        del "%%~D\%CURRENT_EXE%" 2>nul

        :: Copy new exe
        copy "%CURRENT_EXE%" "%%~D\%CURRENT_EXE%" >nul
        echo ✓ Updated in: %%~D
        echo.
    )
)

echo ========================================
echo Update completed!
echo Launching %APP_NAME%...
echo ========================================
start "" "%CURRENT_EXE%"

pause
endlocal
