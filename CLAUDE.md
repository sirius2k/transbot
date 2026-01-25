# Claude AI 작업 가이드

## 프로젝트 개요

TransBot은 OpenAI GPT 모델을 활용한 영어-한국어 양방향 번역 웹 애플리케이션입니다.

### 주요 기능

- 영어 → 한국어 번역
- 한국어 → 영어 번역
- AI 모델 선택 (GPT-4o, GPT-4o Mini, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- Streamlit 기반 웹 인터페이스
- OpenAI API 연동

## 기술 스택

### 프레임워크 및 라이브러리

- **Streamlit**: 웹 UI 프레임워크
- **OpenAI API**: 다양한 GPT 모델 지원 (GPT-4o, GPT-4o Mini, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- **python-dotenv**: 환경 변수 관리
- **Python 3.x**: 메인 개발 언어

## 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── utils.py                  # 유틸리티 함수 모듈
├── requirements.txt          # Python 의존성
├── requirements-dev.txt      # 개발 환경 의존성
├── .env.example             # 환경 변수 템플릿
├── .gitignore               # Git 제외 파일 목록
├── pytest.ini               # pytest 설정 파일
├── .coveragerc              # 코드 커버리지 설정
├── tests/                   # 테스트 디렉토리
│   ├── __init__.py
│   └── test_utils.py        # utils.py 단위 테스트
├── htmlcov/                 # 테스트 커버리지 및 pytest 리포트
├── docs/                    # 문서 디렉토리
│   ├── product/             # 제품 요구사항 문서
│   │   └── PRD.md
│   ├── planning/            # 실행 계획 문서
│   ├── templates/           # 프롬프트 템플릿
│   └── guides/              # 개발 가이드
├── README.md                # 프로젝트 소개 및 사용 가이드
├── CLAUDE.md                # Claude AI 작업 가이드 (본 문서)
└── venv/                    # Python 가상환경 (Git 제외됨)
```

## 코딩 컨벤션

### Python 스타일

- **PEP 8** 스타일 가이드 준수
- 함수와 변수명: `snake_case`
- 클래스명: `PascalCase`
- 상수: `UPPER_CASE`
- 들여쓰기: 스페이스 4칸

### 주석 및 문서화

- 함수에는 docstring 작성 권장
- 복잡한 로직에는 인라인 주석 추가
- 한국어와 영어를 혼용하여 작성 가능

### 코드 예시

```python
def translate(text: str, source: str, target: str, model: str) -> str:
    """OpenAI API를 사용하여 텍스트를 번역합니다.

    Args:
        text: 번역할 텍스트
        source: 원본 언어 (예: "English", "Korean")
        target: 대상 언어 (예: "Korean", "English")
        model: 사용할 AI 모델 (예: "gpt-4o-mini", "gpt-4o")

    Returns:
        번역된 텍스트
    """
    # API 호출 로직
    pass
```

## 개발 환경 설정

### 가상환경 사용 (권장)

가상환경을 사용하면 프로젝트별로 독립적인 Python 환경을 유지할 수 있습니다.

#### 1. 가상환경 생성

```bash
python3 -m venv venv
```

#### 2. 가상환경 활성화

##### macOS/Linux

```bash
source venv/bin/activate
```

##### Windows

```bash
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

#### 3. 의존성 설치

가상환경이 활성화된 상태에서:

```bash
pip install -r requirements.txt
```

#### 4. 가상환경 비활성화

작업을 마친 후:

```bash
deactivate
```

### 가상환경 확인

- 가상환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다
- `which python` (macOS/Linux) 또는 `where python` (Windows)로 Python 경로 확인

### 주의사항

- `venv/` 디렉토리는 `.gitignore`에 포함되어 Git에 커밋되지 않습니다
- 팀원과 협업 시 `requirements.txt`를 최신 상태로 유지하세요
- 새로운 패키지 설치 후 `pip freeze > requirements.txt`로 업데이트하세요

## 개발 가이드라인

### 파일 수정 시 주의사항

1. **app.py 수정 시**
   - Streamlit 컴포넌트 구조 유지
   - 에러 핸들링 반드시 포함
   - 사용자 경험을 최우선으로 고려

2. **utils.py 수정 시**
   - 모든 함수에 docstring 작성
   - 타입 힌트 명시 (예: `def func(text: str) -> str:`)
   - 새로운 함수 추가 시 반드시 단위 테스트 작성

3. **requirements.txt 수정 시**
   - 버전 명시 권장 (예: `streamlit>=1.28.0`)
   - 새로운 라이브러리 추가 시 PRD.md 업데이트

4. **Markdown 문서 수정 시**
   - markdownlint 규칙 준수 필수
   - 모든 문서에 일관되게 적용

### Markdownlint 규칙 상세 가이드

#### MD022 - Headings should be surrounded by blank lines

**의미**: 모든 헤딩 앞뒤로 빈 줄 필요

**나쁜 예**:

```markdown
## 섹션 제목
내용이 바로 시작됨
```

**좋은 예**:

```markdown
## 섹션 제목

내용 앞에 빈 줄 추가
```

#### MD032 - Lists should be surrounded by blank lines

**의미**: 리스트 앞뒤로 빈 줄 필요

**나쁜 예**:

```markdown
설명 텍스트
- 항목 1
- 항목 2
다음 내용
```

**좋은 예**:

```markdown
설명 텍스트

- 항목 1
- 항목 2

다음 내용
```

#### MD040 - Fenced code blocks should have a language specified

**규칙**: 모든 코드 블록에 언어 지정

**예시**:

- ✅ \`\`\`python
- ✅ \`\`\`bash
- ✅ \`\`\`text
- ❌ \`\`\`

#### MD047 - Files should end with a single newline character

**규칙**: 파일 마지막에 빈 줄 하나 추가

### AI 모델 선택 구현 가이드

애플리케이션은 다양한 GPT 모델을 지원합니다. 모델 선택 기능 구현 시 다음 사항을 고려하세요:

#### 지원 모델

```python
model_options = {
    "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
    "GPT-4o (최고 품질)": "gpt-4o",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-4": "gpt-4",
    "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
}
```

#### 기본 모델 설정

- **번역 작업**: GPT-4o Mini (가성비 우수, 번역 품질 높음)
- `st.selectbox`의 `index=0`으로 기본 선택 설정

#### 모델별 특징

- **GPT-4o Mini**: 번역에 최적화, 빠른 응답, 낮은 비용
- **GPT-4o**: 최신 모델, 최고 품질
- **GPT-4 Turbo**: GPT-4의 빠른 버전
- **GPT-4**: 표준 고성능 모델
- **GPT-3.5 Turbo**: 가장 빠르고 저렴

### 새 기능 추가 시

1. PRD.md의 "향후 고려사항" 섹션 확인
2. 기존 코드 구조와 일관성 유지
3. 에러 처리 및 사용자 피드백 포함
4. **단위 테스트 작성 필수**
5. 테스트 통과 확인 후 커밋

### API 키 관리

- **절대 하드코딩 금지**
- `.env` 파일 사용 (Git 제외됨)
- 사이드바 입력 옵션 유지

## 문서 작성 가이드라인

### 문서 역할 구분

#### README.md (사용자 중심)

- **대상**: 프로젝트를 처음 접하는 사용자
- **목적**: 설치, 사용법, 문제 해결
- **포함 내용**: 시작하기, 사용 예시, 기술 스택 개요
- **톤**: 친근하고 이해하기 쉬운 설명
- **업데이트 시점**: 사용자 가이드 변경 시

#### PRD.md (제품 중심)

- **대상**: 프로덕트 매니저, 기획자
- **목적**: 제품 요구사항 정의 및 로드맵
- **포함 내용**: 기능 요구사항, 릴리스 계획, KPI
- **톤**: 공식적이고 체계적인 문서
- **업데이트 시점**: 제품 기능 변경 시 필수

#### CLAUDE.md (개발자 중심)

- **대상**: Claude AI 및 개발자
- **목적**: 개발 컨벤션, 협업 가이드
- **포함 내용**: 코딩 컨벤션, 워크플로우, 팁
- **톤**: 실용적이고 구체적인 가이드
- **업데이트 시점**: 개발 프로세스 변경 시

### 문서 간 정보 중복 방지

- **기술 스택**: README.md에는 간략히, PRD.md에는 상세히
- **프로젝트 구조**: 세 문서 모두 동일하게 유지
- **향후 계획**: PRD.md가 마스터, README.md는 요약
- **설치 방법**: README.md만 상세히 작성

### 문서 동기화가 필요한 경우

1. **프로젝트 구조 변경**
   - 파일 추가/삭제 시
   - 세 문서 모두 업데이트

2. **기능 추가/변경**
   - PRD.md 먼저 업데이트
   - README.md에 사용자 가이드 추가
   - 필요시 CLAUDE.md에 개발 가이드 추가

3. **기술 스택 변경**
   - PRD.md 상세 정보 업데이트
   - README.md 개요 업데이트
   - CLAUDE.md 코딩 컨벤션 업데이트

## 문서 작성 워크플로우

### 새 문서 작성 시

1. **문서 목적 정의**

   ```text
   - 누가 읽는가?
   - 왜 필요한가?
   - 어떤 정보를 담을 것인가?
   ```

2. **구조 계획**
   - 목차 작성
   - 주요 섹션 정의
   - 다른 문서와의 차별점 확인

3. **초안 작성**
   - markdownlint 규칙 염두에 두고 작성
   - 헤딩/리스트 주변 빈 줄 유지
   - 코드 블록에 언어 지정

4. **검토 및 수정**
   - markdownlint 검증 실행
   - 다른 문서와 정보 일관성 확인
   - 오타 및 문법 검토

### 기존 문서 수정 시

1. **변경 범위 파악**
   - 어떤 섹션을 수정할 것인가?
   - 다른 문서도 함께 수정해야 하는가?

2. **일관성 체크**
   - 프로젝트 구조 변경 시: 세 문서 모두 업데이트
   - 기능 추가 시: PRD.md → README.md 순서로 업데이트
   - 개발 프로세스 변경 시: CLAUDE.md만 업데이트

3. **검증**
   - markdownlint 규칙 준수 확인
   - 링크 유효성 검사

## 문서 품질 체크리스트

### 모든 Markdown 문서 공통

- [ ] MD022: 모든 헤딩 앞뒤에 빈 줄
- [ ] MD032: 모든 리스트 앞뒤에 빈 줄
- [ ] MD040: 모든 코드 블록에 언어 지정
- [ ] MD047: 파일 끝에 빈 줄
- [ ] 오타 및 문법 오류 없음
- [ ] 링크가 모두 유효함
- [ ] 프로젝트 구조가 최신 상태

### README.md 특화

- [ ] 설치 방법이 단계별로 명확함
- [ ] 사용 예시가 포함됨
- [ ] 문제 해결 섹션이 실용적임
- [ ] 배지(badge)가 정확함
- [ ] 사용자 친화적인 톤 유지

### PRD.md 특화

- [ ] 모든 기능 요구사항이 명확함
- [ ] 향후 계획이 최신 상태
- [ ] KPI가 측정 가능함
- [ ] 릴리스 계획이 구체적임
- [ ] 공식적인 문서 톤 유지

### CLAUDE.md 특화

- [ ] 코딩 컨벤션이 명확함
- [ ] 워크플로우가 구체적임
- [ ] 예시 코드가 포함됨
- [ ] Claude 협업 팁이 실용적임
- [ ] 실무 중심의 가이드

## 테스트 가이드

### 테스트 작성 원칙

1. **단위 테스트 작성 규칙**
   - 모든 핵심 함수는 반드시 테스트 작성
   - 테스트 파일명: `test_[모듈명].py` (예: `test_utils.py`)
   - 테스트 클래스명: `Test[기능명]` (예: `TestDetectLanguage`)
   - 테스트 함수명: `test_[테스트내용]` (예: `test_detect_korean`)

2. **테스트 케이스 작성 가이드**

   ```python
   class TestDetectLanguage:
       """언어 감지 함수 테스트"""

       def test_detect_korean(self):
           """한국어 텍스트 감지 테스트"""
           result = detect_language("안녕하세요")
           assert result == "Korean"
   ```

3. **Mock 객체 사용**

   외부 API 호출이 필요한 함수는 Mock 객체를 사용하여 테스트합니다.

   ```python
   from unittest.mock import Mock

   def test_translate_success():
       """번역 성공 테스트"""
       mock_client = Mock()
       mock_response = Mock()
       mock_response.choices = [Mock()]
       mock_response.choices[0].message.content = "번역된 텍스트"

       mock_client.chat.completions.create.return_value = mock_response

       result = translate(mock_client, "Hello", "English", "Korean", "gpt-4o")
       assert result == "번역된 텍스트"
   ```

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_utils.py

# 특정 클래스 테스트
pytest tests/test_utils.py::TestDetectLanguage

# 특정 함수 테스트
pytest tests/test_utils.py::TestDetectLanguage::test_detect_korean

# 상세 출력
pytest -v

# 커버리지와 함께 실행
pytest --cov=utils --cov-report=html
```

### 테스트 커버리지 확인

```bash
# 터미널에서 커버리지 확인
pytest --cov=utils --cov-report=term-missing

# HTML 리포트 생성
pytest --cov=utils --cov-report=html

# 리포트 열기 (macOS)
open htmlcov/index.html

# 리포트 열기 (Linux)
xdg-open htmlcov/index.html

# 리포트 열기 (Windows)
start htmlcov/index.html
```

### 커버리지 목표

- **최소 커버리지**: 80% 이상 유지
- **핵심 함수**: 100% 커버리지 목표
- 커버리지 80% 미만 시 pytest 실패 (`pytest.ini`에 설정됨)

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

## 배포 체크리스트

### 개발 환경

- [ ] 가상환경 설정 완료 (`venv/` 디렉토리 존재)
- [ ] 가상환경 활성화 확인 (프롬프트에 `(venv)` 표시)
- [ ] requirements.txt 의존성 설치 확인
- [ ] requirements-dev.txt 의존성 설치 확인 (개발 환경)

### 애플리케이션

- [ ] `.env` 파일에 유효한 API 키 설정
- [ ] 모든 AI 모델 선택 옵션 테스트 완료
- [ ] 양방향 번역 기능 테스트 (영어↔한국어)
- [ ] Markdown 포맷 보존 테스트
- [ ] 복사 버튼 동작 확인
- [ ] 지우기 버튼 동작 확인
- [ ] 에러 핸들링 동작 확인

### 테스트 및 품질

- [ ] **모든 단위 테스트 통과 확인** (`pytest`)
- [ ] **코드 커버리지 80% 이상 확인** (`pytest --cov`)
- [ ] 테스트 리포트 생성 확인 (`htmlcov/`)
- [ ] 새로운 함수에 대한 테스트 작성 완료

### 문서

- [ ] PRD.md 업데이트 (변경사항 반영)
- [ ] README.md 업데이트 (사용자 가이드)
- [ ] CLAUDE.md 업데이트 (개발 가이드)
- [ ] 모든 문서 markdownlint 규칙 준수 확인
- [ ] 모든 문서의 "최종 수정일" 업데이트 (날짜 + 시간)

### Git 및 배포

- [ ] Git 커밋 메시지 명확하게 작성
- [ ] commit-and-push 서브에이전트 사용 (권장)
- [ ] GitHub 푸시 완료 확인

## 향후 개발 방향

### Phase 2 고려사항

- 번역 히스토리 저장 (SQLite 또는 JSON)
- 즐겨찾기 기능
- 사용자 인증 시스템

### Phase 3 고려사항

- 다양한 AI 모델 지원 (Claude, Gemini 등)
- 파일 업로드 일괄 번역
- REST API 제공

## 참고 자료

### 공식 문서

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
- [Python 공식 문서](https://docs.python.org/3/)

### 유용한 리소스

- [PEP 8 스타일 가이드](https://pep8.org/)
- [Streamlit 갤러리](https://streamlit.io/gallery)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Markdownlint 규칙](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

## Claude와의 협업 팁

### 효과적인 요청 방법

1. **구체적으로 요청하기**
   - 나쁜 예: "번역 기능 개선해줘"
   - 좋은 예: "번역 결과에 복사 버튼을 추가해줘"

2. **파일 경로 명시하기**
   - 나쁜 예: "코드 수정해줘"
   - 좋은 예: "app.py의 translate 함수를 수정해줘"

3. **변경 범위 제한하기**
   - 한 번에 하나의 기능만 요청
   - 큰 변경은 여러 단계로 나누기

### 코드 리뷰 요청 시

```text
app.py의 번역 함수를 리뷰해줘. 특히 다음 사항을 확인해줘:
1. 에러 핸들링이 적절한가?
2. 성능 최적화 가능한 부분이 있는가?
3. 코드 가독성을 개선할 수 있는가?
```

### 문서 작업 요청 시

1. **새 문서 작성 요청**

   ```text
   좋은 예: "README.md 초안을 만들어줘. 사용자 친화적으로 작성하고
             설치 방법과 사용 예시를 포함해줘."

   더 좋은 예: "README.md 초안을 만들어줘. PRD.md와 중복되지 않도록
               사용자 관점에서 작성하고, markdownlint 규칙을 준수해줘."
   ```

2. **문서 수정 요청**

   ```text
   좋은 예: "PRD.md에 markdownlint 규칙을 적용해줘."

   더 좋은 예: "PRD.md를 markdownlint를 통과할 수 있도록 수정해줘.
               특히 MD022, MD032 규칙을 반영해줘."
   ```

3. **규칙 준수 요청**

   ```text
   "앞으로 PRD를 수정할 때 이 규칙을 항상 확인해줘"
   → Claude가 향후 작업에 규칙을 자동 적용
   ```

### 문서 관련 일반적인 요청 패턴

- ✅ "XXX.md 초안을 만들어줘"
- ✅ "XXX.md를 markdownlint 규칙에 맞게 수정해줘"
- ✅ "XXX.md에 YYY 섹션을 추가해줘"
- ✅ "세 문서의 프로젝트 구조를 동기화해줘"
- ❌ "문서 좀 만들어줘" (너무 모호함)
- ❌ "수정해줘" (어떤 문서, 어떤 부분인지 불명확)

### Git 커밋 및 푸시 요청 시

#### commit-and-push 서브에이전트 사용 (권장)

이 프로젝트는 `.claude/commands/commit-and-push.md` 서브에이전트를 제공합니다.

**사용 방법**:

```text
"앞으로 커밋하고 푸시할 때는 commit-and-push 서브에이전트를 사용해줘"
```

이렇게 요청하면 Claude가 자동으로:

1. 변경사항 분석
2. 적절한 커밋 메시지 생성
3. Git 커밋 실행
4. GitHub에 푸시

**커밋 메시지 형식**:

```text
[주요 변경사항에 대한 한줄 요약]

- [변경사항에 대한 세부 내용]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

#### 직접 커밋 요청 (대안)

서브에이전트를 사용하지 않는 경우:

```text
좋은 예: "지금까지의 변경사항을 커밋하고 푸시해줘"
더 좋은 예: "AI 모델 선택 기능을 추가했으니 이 변경사항을 커밋하고 푸시해줘"
```

## 문서 업데이트 정책

### 업데이트 우선순위

1. **즉시 업데이트 (Critical)**
   - 프로젝트 구조 변경
   - 보안 관련 정보 변경
   - 설치/실행 방법 변경

2. **단기 업데이트 (Important)**
   - 새로운 기능 추가
   - 기존 기능 변경
   - 개발 프로세스 변경

3. **장기 업데이트 (Nice to Have)**
   - 문서 포맷 개선
   - 예시 추가
   - 링크 업데이트

### 문서별 업데이트 기준

- **README.md**: 사용자 가이드 변경 시
- **PRD.md**: 제품 기능 변경 시 필수
- **CLAUDE.md**: 개발 프로세스 변경 시

## 버전 관리

### 커밋 메시지 컨벤션

```text
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드 설정 등
```

### 코드 커밋 예시

```bash
git commit -m "feat: 번역 결과 복사 버튼 추가"
git commit -m "fix: API 키 미입력 시 오류 처리 개선"
git commit -m "refactor: translate 함수 모듈화"
```

### 문서 커밋 메시지

#### 단일 문서 수정

```bash
git commit -m "docs(readme): 설치 방법 섹션 업데이트"
git commit -m "docs(prd): Phase 2 기능 목록 추가"
git commit -m "docs(claude): markdownlint 규칙 가이드 추가"
```

#### 여러 문서 동시 수정

```bash
git commit -m "docs: 프로젝트 구조를 세 문서에 동기화"
git commit -m "docs: markdownlint 규칙을 모든 문서에 적용"
git commit -m "docs: 기술 스택 정보 업데이트 (README, PRD, CLAUDE)"
```

### 문서 버전 관리 전략

#### 주요 변경 사항 추적

1. **README.md 변경 시**
   - 사용자에게 영향을 주는 변경사항
   - 설치/실행 방법 변경
   - 새로운 기능 사용법

2. **PRD.md 변경 시**
   - 제품 로드맵 변경
   - 새로운 요구사항 추가
   - KPI 업데이트

3. **CLAUDE.md 변경 시**
   - 개발 컨벤션 변경
   - 새로운 워크플로우 추가
   - 문서 작성 가이드라인 업데이트

#### 문서 일관성 유지

```bash
# 프로젝트 구조 변경 시 체크리스트
1. README.md의 프로젝트 구조 업데이트
2. PRD.md의 프로젝트 구조 업데이트
3. CLAUDE.md의 프로젝트 구조 업데이트
4. 세 문서 모두 동일한지 확인
5. 커밋: "docs: 프로젝트 구조 동기화"
```

## 라이선스 및 기여

이 프로젝트는 개인 학습 및 개발 목적으로 작성되었습니다.

---

**마지막 업데이트**: 2026-01-26 08:40

**작성자**: TransBot Development Team
