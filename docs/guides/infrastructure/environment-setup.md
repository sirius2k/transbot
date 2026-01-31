# 개발 환경 설정

TransBot 프로젝트의 개발 환경 설정 방법을 안내합니다.

## 가상환경 사용 (권장)

가상환경을 사용하면 프로젝트별로 독립적인 Python 환경을 유지할 수 있습니다.

### 1. 가상환경 생성

```bash
python3 -m venv venv
```

### 2. 가상환경 활성화

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

### 3. 의존성 설치

가상환경이 활성화된 상태에서:

```bash
pip install -r requirements.txt
```

### 4. 가상환경 비활성화

작업을 마친 후:

```bash
deactivate
```

## 가상환경 확인

- 가상환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다
- `which python` (macOS/Linux) 또는 `where python` (Windows)로 Python 경로 확인

## 주의사항

- `venv/` 디렉토리는 `.gitignore`에 포함되어 Git에 커밋되지 않습니다
- 팀원과 협업 시 `requirements.txt`를 최신 상태로 유지하세요
- 새로운 패키지 설치 후 `pip freeze > requirements.txt`로 업데이트하세요

## 문제 해결 가이드

### 자주 발생하는 이슈

#### OpenAI API 오류

```python
try:
    result = translate(input_text, source_lang, target_lang, selected_model)
except Exception as e:
    st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
```

#### Streamlit 세션 상태 관리

```python
# 세션 상태 초기화
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
```

### 디버깅 팁

- `streamlit run app.py --logger.level=debug` 명령으로 디버그 모드 실행
- 브라우저 콘솔에서 네트워크 요청 확인
- OpenAI API 사용량 대시보드 모니터링

---

마지막 업데이트: 2026-01-31
