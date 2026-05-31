@echo on
setlocal

:: === CONFIG ===
set "APP_NAME=Wdb"
set "CURRENT_EXE=Wdb.exe"
set "NEW_EXE=Wdb_new.exe"
set "UPDATE_URL=https://github.com/fariasjim/wordbuddy/releases/latest/download/Wdb.exe"

echo.
echo === Starting Update for %APP_NAME% (%CURRENT_EXE%) ===

:: === DOWNLOAD NEW VERSION ===
echo Downloading latest version from %UPDATE_URL% to %NEW_EXE%...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%UPDATE_URL%', '%NEW_EXE%')"

if exist "%NEW_EXE%" (
    echo Download of %NEW_EXE% successful.
    echo.
    
    :: === TERMINATE RUNNING EXECUTABLE (MOVED HERE) ===
    echo Checking for running process: %CURRENT_EXE%
    
    :: Check for running instance
    tasklist /FI "IMAGENAME eq %CURRENT_EXE%" 2>NUL | find /I /N "%CURRENT_EXE%">NUL
    if not errorlevel 1 (
        echo Running instance found. Attempting to terminate...
        :: Terminate forcefully
        taskkill /IM "%CURRENT_EXE%" /F
        
        echo Giving OS 2 seconds to release file lock after termination...
        timeout /t 2 /nobreak
    ) else (
        echo %CURRENT_EXE% is not currently running.
    )
    
    echo.
    :: === FILE REPLACEMENT ===
    echo Deleting old executable: %CURRENT_EXE%
    
    :: Try to delete the old file. If it fails, the process is still locked.
    del "%CURRENT_EXE%"
    
    if exist "%CURRENT_EXE%" (
        echo ERROR: FAILED to delete %CURRENT_EXE%. The file is still locked or access is denied.
        del "%NEW_EXE%"
        goto :EOF
    )
    
    echo Old executable deleted. Renaming %NEW_EXE% to %CURRENT_EXE%...
    rename "%NEW_EXE%" "%CURRENT_EXE%"
    
    :: === LAUNCH NEW VERSION ===
    echo Launching updated %APP_NAME%...
    start "" "%CURRENT_EXE%"
) else (
    echo ERROR: Failed to download update file. Check URL and connectivity.
)

endlocal