@echo off
REM TransBot 실행 스크립트 (Windows)

echo 🚀 TransBot 실행 중...
echo.

REM 가상환경 찾기 및 활성화
if exist "venv\Scripts\activate.bat" (
    echo ✓ 가상환경 활성화 중 (venv)...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo ✓ 가상환경 활성화 중 (.venv)...
    call .venv\Scripts\activate.bat
) else (
    echo ❌ 가상환경을 찾을 수 없습니다.
    echo 다음 명령어로 가상환경을 생성하세요:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM .env 파일 확인
if not exist ".env" (
    echo ⚠️  경고: .env 파일이 없습니다.
    echo    .env.example 파일을 복사하여 .env 파일을 생성하고 API 키를 설정하세요.
    echo    copy .env.example .env
    echo.
)

REM Streamlit 설치 확인
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit이 설치되지 않았습니다.
    echo 다음 명령어로 설치하세요:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Streamlit 앱 실행
echo ✓ Streamlit 앱 실행 중...
echo.
streamlit run app.py