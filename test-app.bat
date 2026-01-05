@echo off
REM 배치 파일이 있는 디렉토리를 기준으로 경로 설정
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend

REM ADB 경로 자동 감지
if defined ANDROID_HOME (
    set ADB_PATH=%ANDROID_HOME%\platform-tools\adb.exe
) else if exist "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" (
    set ADB_PATH=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe
) else (
    set ADB_PATH=adb
)

REM 백엔드 실행
start "Backend" cmd /k "cd /d %BACKEND_DIR% && venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

REM 프론트엔드 실행
if exist "%ADB_PATH%" (
    start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && echo Restarting ADB server... && %ADB_PATH% kill-server && timeout /t 2 /nobreak >nul && %ADB_PATH% start-server && timeout /t 2 /nobreak >nul && echo Checking for existing devices... && %ADB_PATH% devices | findstr /C:\"device\" >nul && (echo Device found. Running Flutter... && flutter run && exit) || (echo No device found. Please start emulator manually or connect a device. && echo Waiting 10 seconds... && timeout /t 10 /nobreak >nul && flutter run && exit)"
) else (
    REM ADB가 없으면 Flutter만 실행
    start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
)