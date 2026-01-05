@echo off
setlocal enabledelayedexpansion

REM 명령줄 인자로 에뮬레이터 이름 받기
set EMULATOR_ARG=%~1

REM 인자 체크: 없으면 에러 메시지 표시 (종료하지 않음)
if "!EMULATOR_ARG!"=="" (
    echo Error: Emulator name is required.
    echo.
    echo Usage: test-app.bat ^<emulator_name^>
    echo.
    echo Example: test-app.bat Pixel_7
    echo.
    echo Available emulators:
    cd /d %~dp0frontend
    flutter emulators
    echo.
    echo Continuing without emulator...
    echo.
)

set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend

if defined ANDROID_HOME (
    set ADB_PATH=%ANDROID_HOME%\platform-tools\adb.exe
) else if exist "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" (
    set ADB_PATH=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe
) else (
    set ADB_PATH=adb
)

start "Backend" cmd /k "cd /d %BACKEND_DIR% && venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

if exist "%ADB_PATH%" (
    %ADB_PATH% kill-server >nul 2>&1
    timeout /t 2 /nobreak >nul
    %ADB_PATH% start-server >nul 2>&1
    timeout /t 2 /nobreak >nul
    
    cd /d %FRONTEND_DIR%
    flutter devices | findstr /I "android" >nul
    if !errorlevel! equ 0 (
        start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
    ) else (
        echo No Android device found.
        
        REM 인자가 있으면 에뮬레이터 시작
        if not "!EMULATOR_ARG!"=="" (
            echo Starting emulator: !EMULATOR_ARG!...
            cd /d %FRONTEND_DIR%
            REM 임시 배치 파일 생성
            echo @echo off > "%TEMP%\launch_emulator.bat"
            echo cd /d %FRONTEND_DIR% >> "%TEMP%\launch_emulator.bat"
            echo flutter emulators --launch "!EMULATOR_ARG!" >> "%TEMP%\launch_emulator.bat"
            REM 백그라운드 실행
            start /B "" "%TEMP%\launch_emulator.bat"
            
            REM 기기 대기
            set /a COUNT=0
            :wait_loop
            timeout /t 2 /nobreak >nul
            flutter devices | findstr /I "android" >nul
            if !errorlevel! equ 0 (
                echo Emulator ready! Starting Flutter...
                start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
                goto :end
            )
            set /a COUNT+=1
            if !COUNT! lss 60 goto :wait_loop
            
            echo Timeout. Starting Flutter anyway...
            start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
        ) else (
            echo No emulator specified. Starting Flutter to select platform...
            start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
        )
    )
) else (
    start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && flutter run"
)

:end
endlocal