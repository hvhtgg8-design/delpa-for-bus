@echo off
SET APPDATA_DIR=%LOCALAPPDATA%\delpa_for_bus
IF NOT EXIST "%APPDATA_DIR%" mkdir "%APPDATA_DIR%"

IF EXIST "%USERPROFILE%\Downloads\main.py" copy "%USERPROFILE%\Downloads\main.py" "%APPDATA_DIR%\main.py"
IF EXIST "%USERPROFILE%\Desktop\main.py" copy "%USERPROFILE%\Desktop\main.py" "%APPDATA_DIR%\main.py"
IF EXIST "C:\main.py" copy "C:\main.py" "%APPDATA_DIR%\main.py"

IF EXIST "%USERPROFILE%\Downloads\oauth_client.py" copy "%USERPROFILE%\Downloads\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"
IF EXIST "%USERPROFILE%\Desktop\oauth_client.py" copy "%USERPROFILE%\Desktop\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"
IF EXIST "C:\oauth_client.py" copy "C:\oauth_client.py" "%APPDATA_DIR%\oauth_client.py"

IF EXIST "%USERPROFILE%\Downloads\code_it_for_it.py" copy "%USERPROFILE%\Downloads\code_it_for_it.py" "%APPDATA_DIR%\code_it_for_it.py"
IF EXIST "%USERPROFILE%\Desktop\code_it_for_it.py" copy "%USERPROFILE%\Desktop\code_it_for_it.py" "%APPDATA_DIR%\code_it_for_it.py"
IF EXIST "C:\code_it_for_it.py" copy "C:\code_it_for_it.py" "%APPDATA_DIR%\code_it_for_it.py"

IF EXIST "%USERPROFILE%\Downloads\make_config.py" copy "%USERPROFILE%\Downloads\make_config.py" "%APPDATA_DIR%\make_config.py"
IF EXIST "%USERPROFILE%\Desktop\make_config.py" copy "%USERPROFILE%\Desktop\make_config.py" "%APPDATA_DIR%\make_config.py"
IF EXIST "C:\make_config.py" copy "C:\make_config.py" "%APPDATA_DIR%\make_config.py"

IF EXIST "%USERPROFILE%\Downloads\encoded_secrets.json" copy "%USERPROFILE%\Downloads\encoded_secrets.json" "%APPDATA_DIR%\encoded_secrets.json"
IF EXIST "%USERPROFILE%\Desktop\encoded_secrets.json" copy "%USERPROFILE%\Desktop\encoded_secrets.json" "%APPDATA_DIR%\encoded_secrets.json"
IF EXIST "C:\encoded_secrets.json" copy "C:\encoded_secrets.json" "%APPDATA_DIR%\encoded_secrets.json"

IF NOT EXIST "%APPDATA_DIR%\main.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/main/main.py' -OutFile '%APPDATA_DIR%\main.py'"
IF NOT EXIST "%APPDATA_DIR%\oauth_client.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/main/oauth_client.py' -OutFile '%APPDATA_DIR%\oauth_client.py'"
IF NOT EXIST "%APPDATA_DIR%\code_it_for_it.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/main/code_it_for_it.py' -OutFile '%APPDATA_DIR%\code_it_for_it.py'"
IF NOT EXIST "%APPDATA_DIR%\make_config.py" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/main/make_config.py' -OutFile '%APPDATA_DIR%\make_config.py'"
IF NOT EXIST "%APPDATA_DIR%\encoded_secrets.json" powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hvhtgg8-design/delpa-for-bus/main/encoded_secrets.json' -OutFile '%APPDATA_DIR%\encoded_secrets.json'"

echo @echo off > "%USERPROFILE%\Desktop\run_main.bat"
echo cd /d "%APPDATA_DIR%" >> "%USERPROFILE%\Desktop\run_main.bat"
echo powershell -Command "Start-Process python main.py -Verb runAs" >> "%USERPROFILE%\Desktop\run_main.bat"

echo Setup completed!
pause
