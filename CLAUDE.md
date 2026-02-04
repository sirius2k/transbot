# Claude AI 작업 가이드

## 📚 가이드 인덱스

### 개발 가이드 (Development)

- [코딩 컨벤션](docs/guides/development/coding-conventions.md) - Python 스타일, Docstring 작성 규칙
- [app.py 구조 가이드](docs/guides/development/app-structure.md) - 함수 기반 설계, 섹션별 함수 목록
- [컴포넌트 모듈 개발](docs/guides/development/components-guide.md) - LanguageDetector, TextAnalyzer, TranslationManager
- [리팩토링 히스토리](docs/guides/development/refactoring-history.md) - 과거 리팩토링 기록

### 인프라 가이드 (Infrastructure)

- [개발 환경 설정](docs/guides/infrastructure/environment-setup.md) - 가상환경, 의존성 설치
- [설정 관리](docs/guides/infrastructure/config-management.md) - Config 클래스 사용법
- [Azure OpenAI 설정](docs/guides/infrastructure/azure-openai/setup.md) - Azure vs OpenAI 비교, 환경 변수 설정
- [Azure Deployment 매핑](docs/guides/infrastructure/azure-openai/deployment.md) - Deployment 매핑, 테스트 작성
- [Azure 에러 핸들링](docs/guides/infrastructure/azure-openai/error-handling.md) - 에러 시나리오 및 처리 방법
- [Langfuse 설정](docs/guides/infrastructure/langfuse/setup.md) - Langfuse v2 설치, API 키 생성
- [Langfuse 사용](docs/guides/infrastructure/langfuse/usage.md) - 대시보드 사용법, 추적 데이터 확인
- [Langfuse 에러 핸들링](docs/guides/infrastructure/langfuse/error-handling.md) - 에러 시나리오 및 처리 방법

### 품질 가이드 (Quality)

- [테스트 가이드](docs/guides/quality/testing-guide.md) - 단위 테스트, 커버리지, Mock 사용법

### 워크플로우 가이드 (Workflows)

- [문서 작성 가이드](docs/guides/workflows/documentation.md) - Markdown 규칙, 문서 역할 구분
- [GitHub 이슈 관리](docs/guides/workflows/github-issues.md) - 레이블 생성, 이슈 관리
- [작업 시간 추적](docs/guides/workflows/time-tracking.md) - 작업 분류, 로그 작성법
- [FEATURE 완료 워크플로우](docs/guides/workflows/feature-completion.md) - FEATURE 완료 시 문서 업데이트 절차

### 범용 가이드 (General) - 참고용

- [Claude 기반 개발 프로젝트 가이드라인](docs/guides/general/claude-development-guide.md) - 모든 Claude 프로젝트 적용 가능
- [가이드 작성 사고 과정 (CoT)](docs/guides/general/claude-development-guide-cot.md) - 메타 문서

> **참고**: 범용 가이드는 TransBot에 특화되지 않은 일반적인 Claude 협업 베스트 프랙티스입니다. TransBot 개발 시에는 위의 프로젝트 특화 가이드를 우선 사용하세요.

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
  - **utils.py**: 순수 텍스트 처리 유틸리티 (언어 감지, 토큰 카운팅, Markdown 처리)
- **레이어드 아키텍처**: app.py (UI) → components (비즈니스 로직) → utils (텍스트 처리 유틸리티)
- **단일 책임 원칙 (SRP)**: 각 모듈은 명확한 하나의 책임을 가짐
  - utils.py: 순수 텍스트 처리만 담당 (API 호출 없음)
  - TranslationManager: OpenAI API 번역 전담

## 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── utils.py                  # 유틸리티 함수 모듈
├── logger.py                 # 로깅 설정 모듈 (JSONFormatter, setup_logging)
├── config.py                 # 설정 관리 모듈
├── components/               # 클래스 기반 컴포넌트 모듈
│   ├── __init__.py
│   ├── language.py          # LanguageDetector 클래스
│   ├── text.py              # TextAnalyzer 클래스
│   ├── translation.py       # TranslationManager 클래스
│   ├── observability.py     # LangfuseObserver 클래스 (LLM 관찰성)
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
│   ├── feature-execution-log/   # 작업 시간 로그
│   ├── templates/           # 프롬프트 템플릿
│   └── guides/              # 개발 가이드
│       ├── development/     # 개발 가이드
│       ├── infrastructure/  # 인프라 가이드
│       ├── quality/         # 품질 가이드
│       └── workflows/       # 워크플로우 가이드
├── infra/                   # 인프라 관리 (Docker Compose)
│   ├── docker-compose.yml   # 서비스 통합 구성
│   ├── .env.infra.example   # 인프라 환경 변수 템플릿
│   ├── README.md            # 인프라 사용 가이드
│   ├── services/            # 서비스별 설정
│   │   ├── langfuse/        # Langfuse (LLM 관찰성)
│   │   ├── postgres/        # PostgreSQL (데이터베이스)
│   │   └── redis/           # Redis (캐싱)
│   ├── scripts/             # 관리 스크립트
│   │   ├── start.sh         # 서비스 시작
│   │   ├── stop.sh          # 서비스 종료
│   │   ├── logs.sh          # 로그 확인
│   │   ├── health-check.sh  # 헬스 체크
│   │   └── reset.sh         # 데이터 초기화
│   └── volumes/             # 데이터 영속화 (Git 제외)
├── .claude/                 # Claude AI 서브에이전트 및 커스텀 명령어
│   ├── commands/            # 커스텀 명령어
│   └── agents/              # 서브에이전트
├── create-labels.sh         # GitHub 레이블 생성 스크립트
├── README.md                # 프로젝트 소개 및 사용 가이드
├── CLAUDE.md                # Claude AI 작업 가이드 (본 문서)
└── venv/                    # Python 가상환경 (Git 제외됨)
```

## 빠른 시작 (Quick Start)

### 1. 개발 환경 설정

자세한 내용은 [개발 환경 설정 가이드](docs/guides/infrastructure/environment-setup.md)를 참고하세요.

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate.bat  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 코딩 컨벤션 확인

- [코딩 컨벤션 가이드](docs/guides/development/coding-conventions.md) 참고
- **PEP 8** 스타일 가이드 준수
- 함수와 변수명: `snake_case`, 클래스명: `PascalCase`, 상수: `UPPER_CASE`

### 3. 테스트 작성 및 실행

- [테스트 가이드](docs/guides/quality/testing-guide.md) 참고
- 모든 핵심 함수는 반드시 테스트 작성
- 최소 커버리지: 80% 이상 유지

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=utils --cov-report=html
```

## 개발 가이드라인

### 로깅 시스템 사용

TransBot은 Python 표준 `logging` 모듈을 사용합니다. 새로운 기능 추가 시 적절한 로깅을 포함하세요.

**로거 가져오기**:

```python
import logging

logger = logging.getLogger("transbot.module_name")
```

**로깅 레벨 사용**:

- `DEBUG`: 디버깅 정보 (개발 환경)
- `INFO`: 정상 동작 (API 호출, 작업 완료)
- `WARNING`: 주의 필요 (입력 길이 80% 초과)
- `ERROR`: 에러 발생 (API 실패)
- `CRITICAL`: 치명적 오류 (설정 로드 실패)

**로깅 예시**:

```python
# API 호출 시작
logger.info("API 호출 시작", extra={
    "model": "gpt-4o-mini",
    "input_length": 150
})

# 에러 로깅
logger.error("API 호출 실패", extra={
    "error_type": "TimeoutError"
}, exc_info=True)
```

**주의사항**:

- 민감정보(API 키)는 로깅하지 않음
- extra 필드로 구조화된 데이터 전달
- 에러 발생 시 `exc_info=True` 사용

### 파일 수정 시 주의사항

#### app.py 수정 시

자세한 내용은 [app.py 구조 가이드](docs/guides/development/app-structure.md)를 참고하세요.

- **함수 기반 구조 유지**: 새로운 기능은 적절한 섹션에 함수로 추가
- **섹션 구분 준수**: Helper / Configuration / UI Rendering / Logic / Main 섹션 구분
- **main() 흐름 명확성**: main() 함수는 9단계 흐름을 유지하며 간결하게 작성
- 에러 핸들링 반드시 포함
- **타입 힌트 및 Docstring 필수**

#### components/ 모듈 수정 시

자세한 내용은 [컴포넌트 모듈 개발 가이드](docs/guides/development/components-guide.md)를 참고하세요.

- 단일 책임 원칙(SRP) 준수: 각 클래스는 하나의 명확한 책임만 가짐
- 클래스에 docstring 및 모든 메서드에 상세한 설명 작성
- 타입 힌트 명시 (예: `def method(text: str) -> str:`)
- 새로운 클래스/메서드 추가 시 반드시 단위 테스트 작성

#### components/observability.py 수정 시

Langfuse 관찰성 모듈을 수정할 때는 다음 사항을 준수하세요:

- **번역 기능 우선**: Langfuse 에러가 번역 기능을 중단해서는 안 됨
- **Graceful Degradation**: Langfuse 실패 시 모든 메서드는 no-op으로 동작
- **조용한 실패**: 에러는 콘솔에만 출력, UI에는 표시하지 않음
- **에러 핸들링**: 모든 Langfuse 호출을 try-except로 감싸기

자세한 내용은 [Langfuse 에러 핸들링 가이드](docs/guides/infrastructure/langfuse/error-handling.md)를 참고하세요.

#### utils.py 수정 시

- 순수 함수(pure function)로 유지: 부작용 없이 입력에 대한 출력만 반환
- 모든 함수에 docstring 작성
- 타입 힌트 명시 (예: `def func(text: str) -> str:`)
- 새로운 함수 추가 시 반드시 단위 테스트 작성

## Claude와의 협업 팁

### 효과적인 요청 방법

#### 1. 구체적으로 요청하기

- 나쁜 예: "번역 기능 개선해줘"
- 좋은 예: "번역 결과에 복사 버튼을 추가해줘"

#### 2. 파일 경로 명시하기

- 나쁜 예: "코드 수정해줘"
- 좋은 예: "app.py의 translate 함수를 수정해줘"

#### 3. 변경 범위 제한하기

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

자세한 내용은 [문서 작성 가이드](docs/guides/workflows/documentation.md)를 참고하세요.

#### 1. 새 문서 작성 요청

```text
좋은 예: "README.md 초안을 만들어줘. 사용자 친화적으로 작성하고
          설치 방법과 사용 예시를 포함해줘."

더 좋은 예: "README.md 초안을 만들어줘. PRD.md와 중복되지 않도록
            사용자 관점에서 작성하고, markdownlint 규칙을 준수해줘."
```

#### 2. 문서 수정 요청

```text
좋은 예: "PRD.md에 markdownlint 규칙을 적용해줘."

더 좋은 예: "PRD.md를 markdownlint를 통과할 수 있도록 수정해줘.
            특히 MD022, MD032 규칙을 반영해줘."
```

#### 3. 규칙 준수 요청

```text
"앞으로 PRD를 수정할 때 이 규칙을 항상 확인해줘"
→ Claude가 향후 작업에 규칙을 자동 적용
```

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

### LLM 관찰성 (Langfuse)

- [ ] Langfuse 인프라 시작 (`infra/scripts/start.sh`)
- [ ] Langfuse 대시보드 접속 (`http://localhost:3000`)
- [ ] API 키 발급 (Settings > API Keys)
- [ ] `.env` 파일에 Langfuse 환경 변수 설정
- [ ] 번역 수행 후 Langfuse에 추적 데이터 표시 확인
- [ ] 에러 핸들링 테스트 (API 키 오류, 서버 다운 등)

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

## 라이선스 및 기여

이 프로젝트는 개인 학습 및 개발 목적으로 작성되었습니다.

---

마지막 업데이트: 2026-02-04

작성자: TransBot Development Team
