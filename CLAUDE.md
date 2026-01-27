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

### 아키텍처 패턴

- **하이브리드 아키텍처**: 함수 기반 UI 레이어 + 클래스 기반 비즈니스 로직
  - **app.py**: 함수 기반 UI 오케스트레이션 (15개 함수, 5개 섹션)
  - **components/**: 클래스 기반 비즈니스 로직 (LanguageDetector, TextAnalyzer, TranslationManager)
  - **utils.py**: 순수 함수 유틸리티 (컴포넌트에서 래핑)
- **레이어드 아키텍처**: app.py (UI) → components (비즈니스 로직) → utils (유틸리티)

## 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── utils.py                  # 유틸리티 함수 모듈
├── components/               # 클래스 기반 컴포넌트 모듈
│   ├── __init__.py
│   ├── language.py          # LanguageDetector 클래스
│   ├── text.py              # TextAnalyzer 클래스
│   ├── translation.py       # TranslationManager 클래스
│   └── ui/                  # UI 컴포넌트 (향후 확장)
│       └── __init__.py
├── requirements.txt          # Python 의존성
├── requirements-dev.txt      # 개발 환경 의존성
├── .env.example             # 환경 변수 템플릿
├── .gitignore               # Git 제외 파일 목록
├── pytest.ini               # pytest 설정 파일
├── .coveragerc              # 코드 커버리지 설정
├── tests/                   # 테스트 디렉토리
│   ├── __init__.py
│   ├── test_utils.py        # utils.py 단위 테스트
│   ├── test_language.py     # LanguageDetector 단위 테스트
│   ├── test_text.py         # TextAnalyzer 단위 테스트
│   └── test_translation.py  # TranslationManager 단위 테스트
├── htmlcov/                 # 테스트 커버리지 및 pytest 리포트
├── docs/                    # 문서 디렉토리
│   ├── product/             # 제품 요구사항 문서
│   │   └── PRD.md
│   ├── feature-execution-plan/  # 기능 명세 및 실행 계획
│   ├── templates/           # 프롬프트 템플릿
│   └── guides/              # 개발 가이드
├── .claude/                 # Claude AI 서브에이전트 및 커스텀 명령어
│   ├── commands/            # 커스텀 명령어
│   └── agents/              # 서브에이전트
├── create-labels.sh         # GitHub 레이블 생성 스크립트
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

#### 클래스 기반 컴포넌트

```python
class TranslationManager:
    """번역 작업을 관리하는 클래스

    OpenAI 클라이언트를 관리하고 번역 설정(모델, temperature)을 유지합니다.
    """

    def __init__(self, client, model: str = "gpt-4o-mini", temperature: float = 0.3):
        """
        Args:
            client: OpenAI 클라이언트 인스턴스
            model: 사용할 AI 모델 (기본 gpt-4o-mini)
            temperature: 번역 창의성 설정 (기본 0.3)
        """
        self.client = client
        self.model = model
        self.temperature = temperature

    def translate(self, text: str, source: str, target: str) -> str:
        """텍스트를 번역합니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")

        Returns:
            번역된 텍스트
        """
        # API 호출 로직
        pass
```

#### 함수 기반 유틸리티

```python
def detect_language(text: str) -> str:
    """텍스트의 언어를 감지합니다.

    Args:
        text: 분석할 텍스트

    Returns:
        감지된 언어명 ("Korean", "English", "unknown")
    """
    # 언어 감지 로직
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

## app.py 구조 가이드

### 함수 기반 모듈 설계

app.py는 **함수 기반으로 구조화**되어 있으며, 각 함수는 명확한 책임을 가지고 있습니다.

#### 전체 구조 개요

- **총 라인 수**: 427줄
- **총 함수 수**: 15개 함수 + 1개 main() 진입점
- **섹션 구분**: 5개 섹션으로 명확히 분리
- **설계 철학**: 관심사 분리(Separation of Concerns), 단일 책임 원칙(SRP)

#### 섹션별 함수 목록

##### 1. Helper Functions (3개) - 클립보드 복사 버튼

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `create_copy_button()` | 단일 복사 버튼 HTML 생성 | text_to_copy, button_label, button_key | str |
| `create_dual_copy_buttons()` | 듀얼 복사 버튼 HTML 생성 (포맷포함/텍스트만) | text_with_format, button_key_prefix | str |
| `clear_inputs()` | 세션 상태 초기화 콜백 | 없음 | None |

##### 2. Configuration Functions (5개) - 설정 및 초기화

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `initialize_page_config()` | 페이지 설정 초기화 | 없음 | None |
| `initialize_session_state()` | 세션 상태 초기화 | 없음 | None |
| `setup_api_client()` | OpenAI API 클라이언트 설정 | 없음 | OpenAI |
| `initialize_components()` | 컴포넌트 인스턴스 초기화 | 없음 | tuple[LanguageDetector, TextAnalyzer] |
| `setup_sidebar()` | 사이드바 설정 및 모델 선택 | 없음 | tuple[str, dict[str, str]] |

##### 3. UI Rendering Functions (5개) - UI 렌더링

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `show_title()` | 페이지 타이틀 표시 | 없음 | None |
| `show_info_messages()` | 정보 메시지 표시 | 없음 | None |
| `render_input_area()` | 입력 영역 렌더링 | 없음 | st.delta_generator.DeltaGenerator |
| `render_action_buttons()` | 액션 버튼 렌더링 (번역하기/지우기) | input_text, source_lang, target_lang, translation_manager | None |
| `render_translation_result()` | 번역 결과 렌더링 | 없음 | None |

##### 4. Logic Functions (2개) - 비즈니스 로직

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `update_statistics()` | 통계 업데이트 및 언어 감지 | input_text, stats_placeholder, language_detector, text_analyzer, selected_model | tuple[str, str, str] |
| `handle_translation()` | 번역 처리 로직 | input_text, source_lang, target_lang, translation_manager | None |

##### 5. Main Function (1개) - 애플리케이션 진입점

| 함수명 | 책임 | 매개변수 | 반환 타입 |
| ------ | ---- | -------- | --------- |
| `main()` | 메인 애플리케이션 흐름 조율 (9단계) | 없음 | None |

#### main() 함수 실행 흐름 (9단계)

```python
def main() -> None:
    """메인 애플리케이션 함수"""
    # 1. 페이지 설정 및 초기화
    initialize_page_config()
    initialize_session_state()

    # 2. 타이틀 표시
    show_title()

    # 3. API 클라이언트 및 컴포넌트 초기화
    client = setup_api_client()
    language_detector, text_analyzer = initialize_components()

    # 4. 사이드바 설정 및 번역 관리자 초기화
    selected_model, _ = setup_sidebar()
    translation_manager = TranslationManager(client, model=selected_model)

    # 5. 정보 메시지 표시
    show_info_messages()

    # 6. 입력 영역 렌더링
    stats_placeholder = render_input_area()

    # 7. 통계 업데이트 및 언어 감지
    input_text = st.session_state.input_text
    source_lang, target_lang, _ = update_statistics(
        input_text, stats_placeholder, language_detector, text_analyzer, selected_model
    )

    # 8. 액션 버튼 렌더링
    render_action_buttons(input_text, source_lang, target_lang, translation_manager)

    # 9. 번역 결과 표시
    render_translation_result()
```

#### 함수 기반 설계의 장점

##### 코드 품질 지표

| 지표 | 변경 전 (인라인 코드) | 변경 후 (함수 기반) | 개선률 |
| ---- | ------------------- | ------------------ | ------ |
| 함수 개수 | 3개 | 15개 | +400% |
| 최상위 레벨 코드 | 200줄 | 0줄 | -100% |
| 최대 함수 길이 | 94줄 | 38줄 | -60% |
| 테스트 가능 함수 | 2개 | 10개 | +400% |
| Docstring 커버리지 | 67% | 100% | +33% |
| 타입 힌트 적용 | 부분적 | 전체 | +100% |

##### 개선 효과

1. **가독성**: 명확한 섹션 구분으로 코드 이해 용이
2. **유지보수성**: 함수별 독립적 수정 가능
3. **테스트 용이성**: 순수 함수로 단위 테스트 작성 가능
4. **재사용성**: 설정/렌더링/로직 함수 분리
5. **확장성**: 새로운 기능 추가 시 기존 함수에 영향 최소화

#### 함수 작성 규칙

1. **명확한 책임**: 각 함수는 하나의 명확한 책임만 가짐
2. **타입 힌트 필수**: 모든 매개변수와 반환 타입에 타입 힌트 명시
3. **Docstring 작성**: 함수 목적, 매개변수, 반환값 설명
4. **섹션 주석**: 각 섹션은 주석으로 명확히 구분
5. **매개변수 명시**: 전역 변수 대신 명시적 매개변수 사용

#### 향후 확장 계획

##### Phase 2: UI 컴포넌트 클래스화

현재 `create_copy_button()`, `create_dual_copy_buttons()` 함수를 클래스로 전환 예정:

```python
# components/ui/clipboard.py (예정)
class ClipboardButton:
    """클립보드 복사 버튼 컴포넌트"""

    def __init__(self, style_config: dict = None):
        self.style_config = style_config or self._default_style()

    def create_single_button(self, text: str, label: str, key: str) -> str:
        """단일 복사 버튼 생성"""
        pass

    def create_dual_buttons(self, text: str, key_prefix: str) -> str:
        """듀얼 복사 버튼 생성"""
        pass
```

## 개발 가이드라인

### 파일 수정 시 주의사항

1. **app.py 수정 시**
   - **함수 기반 구조 유지**: 새로운 기능은 적절한 섹션에 함수로 추가
   - **섹션 구분 준수**: Helper / Configuration / UI Rendering / Logic / Main 섹션 구분
   - **main() 흐름 명확성**: main() 함수는 9단계 흐름을 유지하며 간결하게 작성
   - Streamlit 컴포넌트 구조 유지
   - 에러 핸들링 반드시 포함
   - 사용자 경험을 최우선으로 고려
   - 비즈니스 로직은 components 모듈로 분리
   - **타입 힌트 및 Docstring 필수**

2. **components/ 모듈 수정 시**
   - 단일 책임 원칙(SRP) 준수: 각 클래스는 하나의 명확한 책임만 가짐
   - 클래스에 docstring 및 모든 메서드에 상세한 설명 작성
   - 타입 힌트 명시 (예: `def method(text: str) -> str:`)
   - 새로운 클래스/메서드 추가 시 반드시 단위 테스트 작성
   - 기존 utils.py 함수를 래핑하여 재사용
   - 상태를 가진 객체는 불변성(immutability) 고려

3. **utils.py 수정 시**
   - 순수 함수(pure function)로 유지: 부작용 없이 입력에 대한 출력만 반환
   - 모든 함수에 docstring 작성
   - 타입 힌트 명시 (예: `def func(text: str) -> str:`)
   - 새로운 함수 추가 시 반드시 단위 테스트 작성

4. **requirements.txt 수정 시**
   - 버전 명시 권장 (예: `streamlit>=1.28.0`)
   - 새로운 라이브러리 추가 시 PRD.md 업데이트

5. **Markdown 문서 수정 시**
   - markdownlint 규칙 준수 필수
   - 모든 문서에 일관되게 적용

### 컴포넌트 모듈 개발 가이드

#### 모듈 구성 원칙

- **components/language.py**: 언어 감지 및 번역 방향 관리
  - `LanguageDetector` 클래스: 언어 자동 감지, 번역 방향 결정
  - 언어별 설정을 딕셔너리로 관리 (DIRECTION_CONFIG)

- **components/text.py**: 텍스트 분석 및 Markdown 처리
  - `TextAnalyzer` 클래스: 토큰 카운팅, 문자 수 계산, Markdown 처리
  - 통계 정보 생성 및 UI 표시 로직 캡슐화

- **components/translation.py**: 번역 작업 관리
  - `TranslationManager` 클래스: OpenAI 클라이언트 관리, 번역 실행
  - 모델 및 temperature 설정 관리
  - Azure OpenAI 지원 확장 준비

#### 클래스 설계 예시

```python
class LanguageDetector:
    """텍스트의 언어를 자동 감지하고 번역 방향을 결정하는 클래스"""

    # 클래스 상수: 언어별 설정을 딕셔너리로 관리
    DIRECTION_CONFIG = {
        "Korean": {
            "source": "Korean",
            "target": "English",
            "arrow": "🇰🇷 → 🇺🇸",
            "code": "ko",
            "flag": "🇰🇷"
        },
        # ... 다른 언어 설정
    }

    def __init__(self, threshold: float = 0.5):
        """초기화 메서드: 필요한 설정값 저장"""
        self.threshold = threshold

    def get_translation_direction(self, text: str) -> tuple[str, str, str]:
        """번역 방향을 결정하는 핵심 메서드

        if-elif 체인을 딕셔너리 조회로 대체하여 간결성 향상
        """
        detected = self.detect(text)
        config = self.DIRECTION_CONFIG.get(detected, self.DIRECTION_CONFIG["unknown"])
        return (config["source"], config["target"], config["arrow"])
```

#### 컴포넌트 사용 예시 (app.py)

```python
# 컴포넌트 import
from components.language import LanguageDetector
from components.text import TextAnalyzer
from components.translation import TranslationManager

# 인스턴스 생성
language_detector = LanguageDetector()
text_analyzer = TextAnalyzer()
translation_manager = TranslationManager(client, model="gpt-4o-mini")

# 사용 (기존 20줄 로직이 1줄로 간소화)
source_lang, target_lang, direction_arrow = language_detector.get_translation_direction(input_text)
stats_html = text_analyzer.format_statistics_display(input_text, direction_arrow)
result = translation_manager.translate(input_text, source_lang, target_lang)
```

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
- **현재 커버리지**: 97.98% 달성 (2026-01-27 기준)
- **핵심 함수**: 100% 커버리지 목표
- 커버리지 80% 미만 시 pytest 실패 (`pytest.ini`에 설정됨)

### 테스트 현황

#### 전체 테스트 통계 (2026-01-27 기준)

- **총 테스트 수**: 79개
- **전체 커버리지**: 97.98%
- **모듈별 커버리지**: 모든 컴포넌트 100% 달성

#### 모듈별 테스트 세부사항

##### utils.py (32개 테스트)

- `detect_language()`: 언어 감지 함수 (8개 테스트)
- `count_tokens()`: 토큰 카운팅 함수 (5개 테스트)
- `strip_markdown()`: Markdown 제거 함수 (14개 테스트)
- `translate()`: 번역 함수 (3개 Mock 테스트)
- 기타 유틸리티 함수 (2개 테스트)

##### components/language.py (16개 테스트)

- `LanguageDetector.detect()`: 언어 감지 메서드
- `LanguageDetector.get_translation_direction()`: 번역 방향 결정
- `LanguageDetector.get_language_code()`: 언어 코드 변환
- `LanguageDetector.get_language_flag()`: 플래그 이모지 반환

##### components/text.py (16개 테스트)

- `TextAnalyzer.count_tokens()`: 토큰 카운팅
- `TextAnalyzer.get_statistics()`: 통계 정보 생성
- `TextAnalyzer.strip_markdown()`: Markdown 제거
- `TextAnalyzer.has_markdown()`: Markdown 포함 여부 확인
- `TextAnalyzer.format_statistics_display()`: UI 표시용 HTML 생성

##### components/translation.py (15개 테스트)

- `TranslationManager.translate()`: 번역 수행
- `TranslationManager.set_model()`: 모델 변경
- `TranslationManager.set_temperature()`: temperature 설정
- `TranslationManager.validate_model()`: 모델 검증
- `TranslationManager.get_model_list()`: 지원 모델 목록 조회

### 컴포넌트 테스트 작성 가이드

#### 클래스 테스트 구조

```python
class TestLanguageDetector:
    """LanguageDetector 클래스 테스트"""

    def test_detect_korean(self):
        """한국어 텍스트 감지 테스트"""
        detector = LanguageDetector()
        result = detector.detect("안녕하세요")
        assert result == "Korean"

    def test_get_translation_direction_korean(self):
        """한국어 번역 방향 결정 테스트"""
        detector = LanguageDetector()
        source, target, arrow = detector.get_translation_direction("안녕하세요")
        assert source == "Korean"
        assert target == "English"
        assert arrow == "🇰🇷 → 🇺🇸"
```

#### 컴포넌트 테스트 작성 원칙

1. **각 컴포넌트마다 별도의 테스트 파일 작성**
   - `test_language.py`, `test_text.py`, `test_translation.py`

2. **클래스별 테스트 클래스 생성**
   - 테스트 클래스명: `Test[클래스명]` (예: `TestLanguageDetector`)

3. **메서드별 테스트 함수 작성**
   - 테스트 함수명: `test_[메서드명]_[시나리오]` (예: `test_detect_korean`)

4. **경계값 및 예외 상황 테스트**
   - 정상 케이스, 에러 케이스, 엣지 케이스 모두 커버

5. **Mock 객체 활용**
   - 외부 API 의존성은 Mock으로 대체하여 테스트

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

## GitHub 이슈 관리

### 레이블 생성 스크립트

이 프로젝트는 GitHub 이슈를 체계적으로 관리하기 위한 `create-labels.sh` 스크립트를 제공합니다.

#### 사전 요구사항

- **GitHub CLI (`gh`)**: 설치 및 인증 필요
  - 설치: `brew install gh` (macOS) 또는 [GitHub CLI 공식 사이트](https://cli.github.com/)
  - 인증: `gh auth login`

#### 스크립트 실행 방법

```bash
# 실행 권한 부여
chmod +x create-labels.sh

# 스크립트 실행
./create-labels.sh
```

#### 생성되는 레이블 (총 21개)

##### 1. Area (개발 영역) - 5개

- `area: frontend` - 프론트엔드 관련 작업 (파란색 #0052CC)
- `area: backend` - 백엔드 관련 작업 (보라색 #5319E7)
- `area: ui/ux` - UI/UX 디자인 관련 작업 (파란색 #1D76DB)
- `area: database` - 데이터베이스 관련 작업 (하늘색 #C5DEF5)
- `area: infrastructure` - 인프라 및 배포 관련 작업 (청록색 #006B75)

##### 2. Complexity (복잡도) - 3개

- `complexity: easy` - 쉬운 작업, 1-2시간 (초록색 #0E8A16)
- `complexity: medium` - 보통 난이도, 2-4시간 (노란색 #FBCA04)
- `complexity: hard` - 복잡한 작업, 4시간 이상 (주황색 #D93F0B)

##### 3. Type (작업 유형) - 6개

- `type: feature` - 새로운 기능 추가 (파란색 #0075CA)
- `type: bug` - 버그 수정 (빨간색 #D73A4A)
- `type: documentation` - 문서화 작업 (파란색 #0075CA)
- `type: test` - 테스트 관련 작업 (하늘색 #BFD4F2)
- `type: refactor` - 코드 리팩토링 (노란색 #FBCA04)
- `type: enhancement` - 기능 개선 (하늘색 #A2EEEF)

##### 4. Priority (우선순위) - 4개

- `priority: critical` - 긴급 처리 필요 (진한 빨간색 #B60205)
- `priority: high` - 높은 우선순위 (주황색 #D93F0B)
- `priority: medium` - 보통 우선순위 (노란색 #FBCA04)
- `priority: low` - 낮은 우선순위 (초록색 #0E8A16)

##### 5. Status (상태) - 4개

- `status: blocked` - 블로킹 이슈로 작업 중단 (주황색 #D93F0B)
- `status: in-progress` - 작업 진행 중 (파란색 #1D76DB)
- `status: review-needed` - 리뷰 필요 (노란색 #FBCA04)
- `status: ready` - 작업 준비 완료 (초록색 #0E8A16)

#### 레이블 색상 코딩

- **빨간색 계열**: 긴급/중요 (critical, bug)
- **주황색 계열**: 높은 우선순위/복잡도 (high, hard, blocked)
- **노란색 계열**: 보통 수준 (medium)
- **초록색 계열**: 낮은 우선순위/쉬운 작업 (easy, low, ready)
- **파란색 계열**: 개발 영역 및 작업 유형
- **하늘색 계열**: 문서/테스트 관련

#### 레이블 사용 예시

```bash
# 새로운 기능 이슈
Labels: type: feature, area: frontend, complexity: medium, priority: high

# 버그 수정 이슈
Labels: type: bug, area: backend, complexity: easy, priority: critical

# 문서 작업 이슈
Labels: type: documentation, complexity: easy, priority: low
```

#### 레이블 커스터마이징

`create-labels.sh` 파일을 직접 수정하여 레이블을 커스터마이징할 수 있습니다:

```bash
# 새로운 레이블 추가
gh label create "area: api" --description "API 관련 작업" --color "0052CC" --force

# 기존 레이블 삭제
gh label delete "area: database"

# 레이블 이름 변경 (기존 삭제 후 재생성 필요)
gh label delete "complexity: easy"
gh label create "complexity: simple" --description "간단한 작업" --color "0E8A16" --force
```

#### 주의사항

- `--force` 플래그: 기존 레이블이 있으면 덮어씁니다
- 레이블 삭제 시 연결된 이슈의 레이블도 함께 제거됩니다
- 색상 코드는 # 없이 6자리 HEX 코드로 입력합니다

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

마지막 업데이트: 2026-01-28 08:39

작성자: TransBot Development Team
