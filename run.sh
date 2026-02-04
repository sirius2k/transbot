#!/bin/bash
# TransBot 실행 스크립트 (macOS/Linux)

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 TransBot 실행 중..."
echo ""

# 가상환경 찾기 및 활성화
if [ -d "venv" ]; then
    echo "✓ 가상환경 활성화 중 (venv)..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✓ 가상환경 활성화 중 (.venv)..."
    source .venv/bin/activate
else
    echo "❌ 가상환경을 찾을 수 없습니다."
    echo "다음 명령어로 가상환경을 생성하세요:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  경고: .env 파일이 없습니다."
    echo "   .env.example 파일을 복사하여 .env 파일을 생성하고 API 키를 설정하세요."
    echo "   cp .env.example .env"
    echo ""
fi

# Streamlit 설치 확인
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit이 설치되지 않았습니다."
    echo "다음 명령어로 설치하세요:"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Streamlit 앱 실행
echo "✓ Streamlit 앱 실행 중..."
echo ""
streamlit run app.py