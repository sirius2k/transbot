#!/bin/bash
# TransBot 가상환경 활성화 스크립트 (macOS/Linux)

set -e  # 에러 발생 시 스크립트 중단

echo "🔧 TransBot 가상환경 활성화 중..."
echo ""

# 가상환경 찾기 및 활성화
if [ -d "venv" ]; then
    echo "✓ 가상환경 발견: venv"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✓ 가상환경 발견: .venv"
    source .venv/bin/activate
else
    echo "❌ 가상환경을 찾을 수 없습니다."
    echo ""
    echo "다음 명령어로 가상환경을 생성하세요:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "✓ 가상환경이 활성화되었습니다!"
echo ""
echo "💡 팁:"
echo "  - 앱 실행: ./run.sh 또는 streamlit run app.py"
echo "  - 테스트 실행: pytest"
echo "  - 비활성화: deactivate"
echo ""
