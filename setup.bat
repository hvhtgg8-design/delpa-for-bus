@echo off
SET APPDATA_DIR=%LOCALAPPDATA%\delpa_for_bus
IF NOT EXIST "%APPDATA_DIR%" mkdir "%APPDATA_DIR%"

:: Move existing files if they exist in Downloads, Desktop, or C:\
IF EXIST "%USERPROFILE%\Downloads\main.py" copy "%USERPROFILE%\Downloads\main.py" "%APPDATA_DIR%\main.py"
IF EXIST "%USERPROFILE%\Desktop\main.py" copy "%USERPROFILE%\Desktop\main.py" "%APPDATA_DIR%\main.py"
IF EXIST "C:\main.py" copy "C:\main.py" "%APPDATA_DIR%\main.py"

IF EXIST "%USERPROFILE%\Downloads\oauth_client.py" copy "%USERPROFILE%\Downloads\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"
IF EXIST "%USERPROFILE%\Desktop\oauth_client.py" copy "%USERPROFILE%\Desktop\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"
IF EXIST "C:\oauth_client.py" copy "C:\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"

IF NOT EXIST "%APPDATA_DIR%\main.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main.py' -OutFile '%APPDATA_DIR%\main.py'"
IF NOT EXIST "%APPDATA_DIR%\oauth_client.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/oauth_client.py' -OutFile '%APPDATA_DIR%\oauth_client.py'"
IF NOT EXIST "%APPDATA_DIR%\encoded_secrets.json" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/encoded_secrets.json' -OutFile '%APPDATA_DIR%\encoded_secrets.json'"

:: Create run_main.bat on Desktop
echo @echo off > "%USERPROFILE%\Desktop\run_main.bat"
echo cd /d "%APPDATA_DIR%" >> "%USERPROFILE%\Desktop\run_main.bat"
echo powershell -Command "Start-Process python main.py -Verb runAs" >> "%USERPROFILE%\Desktop\run_main.bat"

echo Setup completed!
pause
