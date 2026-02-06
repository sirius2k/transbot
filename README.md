# TransBot 🌐

AI 기반 영어-한국어 양방향 번역 웹 애플리케이션

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)

## 📋 목차

- [소개](#소개)
- [주요 기능](#주요-기능)
- [시작하기](#시작하기)
  - [필수 요구사항](#필수-요구사항)
  - [설치 방법](#설치-방법)
  - [환경 설정](#환경-설정)
- [사용법](#사용법)
- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)
- [문제 해결](#문제-해결)
- [향후 계획](#향후-계획)
- [라이선스](#라이선스)

## 소개

TransBot은 OpenAI의 GPT-4o-mini 모델을 활용하여 빠르고 정확한 영어-한국어 번역 서비스를 제공하는 웹 애플리케이션입니다. Streamlit 기반의 직관적인 인터페이스로 누구나 쉽게 사용할 수 있습니다.

### 왜 TransBot인가?

- 🚀 **빠른 번역**: GPT-4o-mini 모델을 사용한 고품질 번역
- 🔄 **양방향 지원**: 영어→한국어, 한국어→영어 모두 지원
- 💡 **간편한 사용**: 복잡한 설정 없이 바로 사용 가능
- 🎨 **직관적인 UI**: Streamlit 기반의 깔끔한 인터페이스

## 주요 기능

- ✅ 영어 → 한국어 번역
- ✅ 한국어 → 영어 번역
- ✅ 자동 언어 감지
- ✅ 다양한 AI 모델 선택 (GPT-4o Mini, GPT-4o, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- ✅ **다양한 스타일 번역** (한국어→영어 번역 시)
  - 5가지 스타일: 자연스러운 구어체, 비즈니스 기본, 공식/문서용, 원문 유지, 간결하게
  - 짧은 텍스트 (< 3문장): AI가 자동으로 여러 스타일 생성
  - 긴 텍스트: 사용자가 원하는 스타일 선택
  - 커스텀 스타일 지침 입력 가능
  - 대안 표현 함께 보기 옵션
- ✅ Markdown 포맷 지원 및 보존
- ✅ 번역 결과 듀얼 복사 버튼 (포맷포함 / 텍스트만)
- ✅ 글자수/토큰수 실시간 표시
- ✅ 지우기 버튼 (입력 및 번역 결과 초기화)
- ✅ 실시간 번역 진행 상태 표시
- ✅ API 키 안전 관리 (환경 변수 또는 사이드바 입력)
- ✅ 에러 처리 및 사용자 친화적 메시지

## LLM 관찰성 (Langfuse)

TransBot은 Langfuse를 통해 LLM 사용 내역을 추적하고 분석할 수 있습니다.

### Langfuse 주요 기능

- **프롬프트 추적**: 모든 번역 요청 자동 로깅
- **비용 분석**: 토큰 사용량 및 비용 대시보드
- **성능 모니터링**: 응답 시간, 에러율 추적
- **세션 추적**: 사용자 세션별 번역 요청 그룹핑
- **자체 호스팅**: Docker Compose 기반 로컬 실행

### 설정 방법

1. **인프라 시작**:

   ```bash
   cd infra
   ./scripts/start.sh
   ```

2. **Langfuse 접속**: `http://localhost:3000`

3. **API 키 발급**: Settings > API Keys

4. **환경 변수 설정** (`.env` 파일):

   ```bash
   LANGFUSE_PUBLIC_KEY=pk-lf-xxx
   LANGFUSE_SECRET_KEY=sk-lf-xxx
   LANGFUSE_HOST=http://localhost:3000
   ```

자세한 설정 방법은 [Langfuse 설정 가이드](docs/guides/infrastructure/langfuse/setup.md)를 참고하세요.

### 사용 가이드

- [Langfuse 설정 가이드](docs/guides/infrastructure/langfuse/setup.md) - 설치 및 API 키 생성
- [Langfuse 사용 가이드](docs/guides/infrastructure/langfuse/usage.md) - 대시보드 사용법 및 데이터 분석
- [Langfuse 에러 핸들링](docs/guides/infrastructure/langfuse/error-handling.md) - 에러 시나리오 및 문제 해결

> **참고**: Langfuse는 선택적 기능이며, 설정하지 않아도 번역 기능은 정상 동작합니다.

## 구조화된 로깅

TransBot은 Python 표준 `logging` 모듈을 사용하여 API 호출, 에러, 사용자 행동을 체계적으로 기록합니다.

### 로깅 주요 기능

- **API 호출 추적**: 번역 요청, 응답 시간, 토큰 사용량 기록
- **에러 로깅**: 에러 유형, 메시지, 스택 트레이스 자동 저장
- **구조화된 포맷**: JSON 또는 텍스트 형식 지원
- **자동 로테이션**: 파일 크기 기반 자동 로그 백업
- **민감정보 보호**: API 키, Endpoint 자동 마스킹

### 로깅 설정 (`.env` 파일)

```bash
# 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# 로그 포맷 (json 또는 text)
LOG_FORMAT=json

# 로그 파일 경로
LOG_FILE_PATH=logs/transbot.log

# 콘솔 출력 여부
LOG_CONSOLE_OUTPUT=true
```

> **참고**: 로그 파일은 `logs/` 디렉토리에 자동 저장되며, 10MB마다 자동 로테이션됩니다.

## 시작하기

### 필수 요구사항

- Python 3.x
- OpenAI API 키 ([발급 받기](https://platform.openai.com/api-keys))
- 인터넷 연결

### 설치 방법

1. **저장소 클론**

   ```bash
   git clone https://github.com/yourusername/transbot.git
   cd transbot
   ```

2. **가상환경 생성 및 활성화** (권장)

   가상환경을 사용하면 프로젝트별로 독립적인 Python 환경을 유지할 수 있습니다.

   **macOS/Linux**

   ```bash
   # 가상환경 생성
   python -m venv venv

   # 가상환경 활성화
   source venv/bin/activate
   ```

   **Windows**

   ```bash
   # 가상환경 생성
   python -m venv venv

   # 가상환경 활성화 (Command Prompt)
   venv\Scripts\activate.bat

   # 가상환경 활성화 (PowerShell)
   venv\Scripts\Activate.ps1
   ```

   > 💡 **팁**: 가상환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.
   >
   > 가상환경을 비활성화하려면 `deactivate` 명령을 실행하세요.

3. **의존성 설치**

   **프로덕션 환경**

   ```bash
   pip install -r requirements.txt
   ```

   **개발 환경** (테스트 및 코드 품질 도구 포함)

   ```bash
   pip install -r requirements-dev.txt
   ```

### 환경 설정

1. **환경 변수 파일 생성**

   ```bash
   cp .env.example .env
   ```

2. **.env 파일에 API 키 입력**

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   > 💡 **팁**: API 키는 [OpenAI 플랫폼](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

3. **고급 환경 설정 (선택사항)**

   `.env` 파일에서 다양한 설정을 커스터마이징할 수 있습니다. 모든 설정은 선택사항이며, 설정하지 않으면 기본값이 사용됩니다.

   **OpenAI API 설정**

   ```bash
   OPENAI_API_TIMEOUT=60        # API 타임아웃 (초), 기본값: 60
   OPENAI_MAX_RETRIES=3         # API 재시도 횟수, 기본값: 3
   ```

   **AI 모델 설정**

   ```bash
   DEFAULT_MODEL=gpt-4o-mini    # 기본 AI 모델, 기본값: gpt-4o-mini
   DEFAULT_TEMPERATURE=0.3      # 번역 창의성 (0.0~1.0), 기본값: 0.3
   MAX_TOKENS=4000              # 최대 출력 토큰 수, 기본값: 4000
   ```

   **언어 감지 설정**

   ```bash
   LANGUAGE_DETECTION_THRESHOLD=0.5  # 한국어 감지 임계값 (0.0~1.0), 기본값: 0.5
   ```

   **애플리케이션 설정**

   ```bash
   APP_TITLE=영어-한국어 번역기    # 페이지 제목, 기본값: 영어-한국어 번역기
   APP_ICON=🌐                   # 페이지 아이콘, 기본값: 🌐
   APP_LAYOUT=centered           # 레이아웃 모드 (centered/wide), 기본값: centered
   ```

   **UI 설정**

   ```bash
   TEXT_AREA_HEIGHT=200         # 텍스트 영역 높이 (픽셀), 기본값: 200
   MAX_INPUT_LENGTH=50000       # 최대 입력 길이 (문자 수), 기본값: 50000
   ```

   **Azure OpenAI Service 설정 (선택사항)**

   OpenAI API 대신 Azure OpenAI Service를 사용할 수 있습니다.

   ```bash
   # AI Provider 선택 (openai 또는 azure)
   AI_PROVIDER=azure

   # Azure OpenAI 필수 설정
   AZURE_OPENAI_API_KEY=your_azure_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Azure Deployment 매핑
   # 형식: "모델명:deployment명,모델명:deployment명"
   AZURE_DEPLOYMENTS=gpt-4o:my-gpt4o-deployment,gpt-4o-mini:my-mini-deployment
   ```

   > 💡 **Azure 사용 시 주의사항**:
   > - `AZURE_OPENAI_API_KEY`와 `AZURE_OPENAI_ENDPOINT`는 필수입니다
   > - `AZURE_DEPLOYMENTS`에 Azure Portal에서 생성한 deployment 이름을 매핑해야 합니다
   > - Azure Portal의 "Keys and Endpoint" 섹션에서 필요한 정보를 확인할 수 있습니다

   **지원하는 AI 모델**
   - `gpt-4o`: 최고 품질
   - `gpt-4o-mini`: 가성비 우수 (권장)
   - `gpt-4-turbo`: 빠른 응답
   - `gpt-4`: 안정적 성능
   - `gpt-3.5-turbo`: 가장 빠름

   **지원하는 레이아웃 모드**
   - `centered`: 가운데 정렬 (기본)
   - `wide`: 전체 너비 사용

   > 💡 **팁**: 자세한 설정 옵션은 [.env.example](.env.example) 파일을 참고하세요.

## 사용법

### 1. 애플리케이션 실행

```bash
streamlit run app.py
```

실행하면 브라우저가 자동으로 열리며 `http://localhost:8501`에서 애플리케이션에 접근할 수 있습니다.

### 2. API 키 설정 (선택)

환경 변수로 API 키를 설정하지 않은 경우, 사이드바에서 직접 입력할 수 있습니다.

### 3. 번역하기

1. **AI 모델을 선택합니다**
   - GPT-4o Mini (추천 - 가성비): 기본 선택, 빠르고 비용 효율적
   - GPT-4o (최고 품질): 최신 모델, 가장 높은 번역 품질
   - GPT-4 Turbo: 빠른 응답 속도
   - GPT-4: 안정적인 성능
   - GPT-3.5 Turbo (빠름): 가장 빠른 응답

2. **번역 방향을 선택합니다** (영어 → 한국어 또는 한국어 → 영어)

3. **원문 텍스트를 입력합니다**

4. **"번역하기" 버튼을 클릭합니다**

5. **번역 결과를 확인합니다**

### 사용 예시

#### 영어 → 한국어 번역

```text
입력: Hello, how are you today?
출력: 안녕하세요, 오늘 어떻게 지내세요?
```

#### 한국어 → 영어 번역

```text
입력: 오늘 날씨가 정말 좋네요.
출력: The weather is really nice today.
```

## 프로젝트 구조

```text
transbot/
├── app.py                    # 메인 애플리케이션 파일
├── config.py                 # 설정 관리 모듈
├── utils.py                  # 유틸리티 함수 모듈
├── components/               # 클래스 기반 컴포넌트 모듈
│   ├── __init__.py
│   ├── language.py          # LanguageDetector 클래스
│   ├── text.py              # TextAnalyzer 클래스
│   ├── translation.py       # TranslationManager 클래스
│   └── ui/                  # UI 컴포넌트 (향후 확장)
│       └── __init__.py
├── requirements.txt          # Python 의존성 목록
├── requirements-dev.txt      # 개발 환경 의존성
├── .env.example             # 환경 변수 템플릿
├── .gitignore               # Git 제외 파일 목록
├── pytest.ini               # pytest 설정 파일
├── .coveragerc              # 코드 커버리지 설정
├── tests/                   # 테스트 디렉토리
│   ├── __init__.py
│   ├── test_config.py       # Config 클래스 단위 테스트
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
│   └── guides/              # 개발 가이드 (계층적 구조)
│       ├── development/     # 개발 가이드
│       ├── infrastructure/  # 인프라 가이드
│       ├── quality/         # 품질 가이드
│       ├── workflows/       # 워크플로우 가이드
│       └── general/         # 범용 가이드 (참고용)
├── infra/                   # 인프라 관리 (Docker Compose)
│   ├── docker-compose.yml   # 서비스 통합 구성
│   ├── .env.infra.example   # 인프라 환경 변수 템플릿
│   ├── README.md            # 인프라 사용 가이드
│   ├── services/            # 서비스별 설정 (Langfuse, PostgreSQL, Redis)
│   ├── scripts/             # 관리 스크립트 (start, stop, logs 등)
│   └── volumes/             # 데이터 영속화 (Git 제외)
├── .claude/                 # Claude AI 서브에이전트 및 커스텀 명령어
│   ├── commands/            # 커스텀 명령어
│   └── agents/              # 서브에이전트
├── create-labels.sh         # GitHub 레이블 생성 스크립트
├── CLAUDE.md                # Claude AI 작업 가이드
└── README.md                # 프로젝트 소개 문서 (본 문서)
```

## 로컬 개발 환경

TransBot은 Docker Compose 기반 로컬 개발 인프라를 제공합니다.

### 포함된 서비스

- **PostgreSQL** (포트 5432): 번역 히스토리 및 사용자 데이터 저장
- **Langfuse** (포트 3000): LLM 관찰성 플랫폼 (프롬프트 추적, 비용 분석)
- **Redis** (포트 6379): 캐싱 및 세션 관리

### 인프라 시작

```bash
cd infra
./scripts/start.sh
```

서비스가 시작되면:

1. **Langfuse** 접속: `http://localhost:3000`
2. 계정 생성 및 프로젝트 생성
3. API 키를 TransBot `.env` 파일에 추가

자세한 사용법은 [infra/README.md](infra/README.md)를 참고하세요.

## 기술 스택

### 프론트엔드

- **Streamlit** 1.28.0+: 웹 인터페이스 프레임워크

### 백엔드/API

- **OpenAI API** 1.0.0+: GPT-4o-mini 모델 기반 번역 엔진
- **Azure OpenAI Service**: Microsoft Azure에서 제공하는 OpenAI API (선택사항)
- **Python** 3.x: 메인 개발 언어
- **tiktoken**: 토큰 카운팅 라이브러리

### 아키텍처

- **클래스 기반 컴포넌트 설계**: 관심사 분리 및 재사용성을 위한 모듈화 구조
  - `LanguageDetector`: 언어 감지 및 번역 방향 관리
  - `TextAnalyzer`: 텍스트 분석 및 통계 생성
  - `TranslationManager`: 번역 작업 관리 및 OpenAI 클라이언트 처리

### 환경 관리

- **python-dotenv** 1.0.0+: 환경 변수 관리

### 테스트 및 품질 관리

- **pytest** 7.4.0+: 테스트 프레임워크
- **pytest-cov** 4.1.0+: 코드 커버리지 측정
- **pytest-html** 4.1.0+: HTML 테스트 리포트 생성
- **pytest-mock** 3.12.0+: Mock 객체 지원
- **코드 커버리지**: 99% 달성 (목표: 80% 이상)
- **총 테스트 수**: 105개 (config + utils + components 통합)

### AI 모델

- **GPT-4o Mini** (기본): 번역 성능과 비용 효율성의 균형
- **GPT-4o**: 최고 품질의 번역 결과
- **GPT-4 Turbo**: 빠른 응답 속도와 우수한 성능
- **GPT-4**: 안정적이고 신뢰할 수 있는 번역
- **GPT-3.5 Turbo**: 가장 빠르고 경제적인 옵션

## 테스트

### 테스트 실행

프로젝트는 pytest를 사용한 단위 테스트를 포함하고 있습니다.

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_utils.py

# 커버리지 리포트와 함께 실행
pytest --cov=utils --cov-report=html
```

### 테스트 리포트 확인

테스트 실행 후 `htmlcov/` 폴더에 다음 리포트가 생성됩니다:

- **index.html**: 코드 커버리지 리포트
- **pytest-report.html**: pytest 테스트 결과 리포트

```bash
# macOS/Linux
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### 커버리지 목표

- 최소 커버리지: **80%** 이상 유지
- 현재 커버리지: **99%** 달성 (2026-01-30 기준)
- 모든 핵심 함수 및 클래스에 대한 단위 테스트 작성 필수

## 문제 해결

### API 키 오류

**증상**: "OpenAI API 키를 입력해주세요." 경고 메시지

**해결 방법**:

1. `.env` 파일이 존재하는지 확인
2. `.env` 파일에 올바른 API 키가 입력되어 있는지 확인
3. API 키 앞뒤에 공백이나 따옴표가 없는지 확인

### 번역 오류

**증상**: "번역 중 오류가 발생했습니다" 에러 메시지

**원인 및 해결 방법**:

- **API 한도 초과**: OpenAI 계정의 사용량 한도를 확인하세요
- **네트워크 연결**: 인터넷 연결 상태를 확인하세요
- **API 키 유효성**: API 키가 유효하고 활성화되어 있는지 확인하세요

### 의존성 설치 오류

**증상**: `pip install` 실행 시 오류 발생

**해결 방법**:

```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 재설치
pip install --upgrade pip
pip install -r requirements.txt
```

## 향후 계획

### Phase 2

- [x] 다양한 AI 모델 선택 옵션 (GPT-4o Mini, GPT-4o, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- [ ] 번역 히스토리 저장 기능
- [ ] 즐겨찾기 기능
- [ ] 번역 결과 복사 버튼

### Phase 3

- [ ] 파일 업로드를 통한 일괄 번역
- [ ] 다국어 지원 확장 (중국어, 일본어 등)
- [ ] 번역 스타일 선택 (격식체/비격식체)
- [ ] REST API 제공

자세한 내용은 [PRD.md](docs/product/PRD.md)를 참고하세요.

## 기여하기

이 프로젝트에 기여하고 싶으시다면 다음 절차를 따라주세요:

1. Fork 하기
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따라주세요.

## 개발 가이드

개발자를 위한 자세한 가이드는 [CLAUDE.md](CLAUDE.md)를 참고하세요.

### 가이드 구조

- **[개발 가이드](docs/guides/development/)** - 코딩 컨벤션, app.py 구조, 컴포넌트 모듈
- **[인프라 가이드](docs/guides/infrastructure/)** - 환경 설정, Config 관리, Azure OpenAI
- **[품질 가이드](docs/guides/quality/)** - 테스트 작성, 커버리지 관리
- **[워크플로우 가이드](docs/guides/workflows/)** - 문서 작성, GitHub 이슈, 작업 시간 추적

## 관련 문서

- [PRD.md](docs/product/PRD.md) - 제품 요구사항 문서
- [CLAUDE.md](CLAUDE.md) - Claude AI 작업 가이드 (통합 인덱스)
- [개발 가이드](docs/guides/) - 계층적 개발 가이드 모음

## 라이선스

이 프로젝트는 개인 학습 및 개발 목적으로 작성되었습니다.

## 지원

문제가 발생하거나 질문이 있으시면 Issue를 생성해주세요.

---

Made with ❤️ by TransBot Team

Last Updated: 2026-02-04
