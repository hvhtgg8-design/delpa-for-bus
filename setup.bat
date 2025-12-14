@echo off
SET APPDATA_DIR=%LOCALAPPDATA%\delpa_for_bus
IF NOT EXIST "%APPDATA_DIR%" mkdir "%APPDATA_DIR%"

REM Download files if they don't exist in the APPDATA folder
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/main.py' -OutFile '%APPDATA_DIR%\main.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/oauth_client.py' -OutFile '%APPDATA_DIR%\oauth_client.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/code_it_for_it.py' -OutFile '%APPDATA_DIR%\code_it_for_it.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/make_config.py' -OutFile '%APPDATA_DIR%\make_config.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/encoded_secrets.json' -OutFile '%APPDATA_DIR%\encoded_secrets.json'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/server.js' -OutFile '%APPDATA_DIR%\server.js'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/refs/heads/main/LICENSE' -OutFile '%APPDATA_DIR%\LICENSE'"

REM Create a desktop shortcut/batch to run the app as admin
echo @echo off > "%USERPROFILE%\Desktop\run_main.bat"
echo cd /d "%APPDATA_DIR%" >> "%USERPROFILE%\Desktop\run_main.bat"
echo powershell -Command "Start-Process python main.py -Verb runAs" >> "%USERPROFILE%\Desktop\run_main.bat"

echo Setup completed! All files are in %APPDATA_DIR%.
pause
