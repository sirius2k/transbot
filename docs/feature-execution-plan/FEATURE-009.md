# FEATURE-009: 환경 변수 기반 설정 관리 시스템

## 개요

- **기능명**: 환경 변수 기반 설정 관리 시스템
- **상태**: ⏳ 진행 중 (5/8 완료)
- **분류**: 백엔드 + 프론트엔드
- **우선순위**: P1
- **진행률**: 62.5%
- **예상 시간**: 8시간
- **실제 소요**: 2시간 14분
- **시작일**: 2026-01-29

## 기능 설명

현재 하드코딩되어 있는 애플리케이션 설정 값들을 `.env` 파일로 추출하여 환경별 커스터마이징을 가능하게 합니다. 개발/운영 환경 분리, 브랜딩 커스터마이징, API 동작 제어 등을 설정 파일로 관리합니다.

## 배경 및 필요성

### 현재 문제점

- **하드코딩**: 기본 모델, temperature 등이 코드에 박혀있음
- **환경별 설정 불가**: 개발/운영 환경에서 다른 설정 사용 불가
- **재배포 필요**: 설정 변경 시 코드 수정 및 재배포 필요
- **브랜딩 제약**: 페이지 제목, 아이콘 등 UI 커스터마이징 어려움

### 기대 효과

- 코드 수정 없이 설정 변경 가능
- 환경별(dev/prod) 설정 분리
- 빠른 A/B 테스트 (모델, temperature 변경)
- 브랜딩 커스터마이징 용이
- Azure OpenAI 지원 기반 마련

## 요구사항

### 기능 요구사항

| ID | 요구사항 | 우선순위 | 현재 위치 |
| -- | -------- | -------- | -------- |
| FR-1 | 기본 AI 모델 설정 | P0 | app.py:272 (하드코딩) |
| FR-2 | Temperature 설정 | P0 | translation.py:19 (하드코딩) |
| FR-3 | API Timeout 설정 | P1 | 없음 (기본값 60초) |
| FR-4 | 언어 감지 임계값 설정 | P1 | utils.py:12 (상수) |
| FR-5 | 페이지 제목/아이콘 설정 | P2 | app.py:213-214 (하드코딩) |
| FR-6 | 최대 입력 길이 제한 | P2 | 없음 |
| FR-7 | 최대 출력 토큰 수 | P2 | 없음 |
| FR-8 | 레이아웃 모드 설정 | P3 | app.py:215 (하드코딩) |

### 비기능 요구사항

| ID | 요구사항 | 설명 |
| -- | -------- | ---- |
| NFR-1 | 하위 호환성 | 환경 변수 미설정 시 기본값 사용 |
| NFR-2 | 타입 안정성 | 환경 변수의 타입 검증 |
| NFR-3 | 명확한 에러 메시지 | 잘못된 설정값 입력 시 상세 안내 |

## 작업(Task) 분해

### Task 9.1: 설정 모듈 설계 및 구현

- **분류**: 백엔드
- **의존성**: 없음
- **작업 내용**:
  - `config.py` 모듈 생성
  - 환경 변수 로드 함수 구현
  - 타입 변환 및 검증 함수 구현
  - 기본값 정의
- **예상 파일**: `config.py` (신규)
- **예상 소요 시간**: 1.5시간

```python
# config.py 구조 예시
class Config:
    # OpenAI API 설정
    OPENAI_API_KEY: str
    OPENAI_API_TIMEOUT: int = 60
    OPENAI_MAX_RETRIES: int = 3

    # AI 모델 설정
    DEFAULT_MODEL: str = "gpt-4o-mini"
    DEFAULT_TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 4000

    # 언어 감지 설정
    LANGUAGE_DETECTION_THRESHOLD: float = 0.5

    # 애플리케이션 설정
    APP_TITLE: str = "영어-한국어 번역기"
    APP_ICON: str = "🌐"
    APP_LAYOUT: str = "centered"

    # UI 설정
    TEXT_AREA_HEIGHT: int = 200
    MAX_INPUT_LENGTH: int = 50000

    @classmethod
    def load(cls):
        """환경 변수를 로드하고 Config 객체를 반환"""
```

### Task 9.2: .env.example 업데이트

- **분류**: 설정
- **의존성**: Task 9.1
- **작업 내용**:
  - 모든 설정 가능한 환경 변수 추가
  - 주석으로 설명 및 기본값 명시
  - 카테고리별 섹션 구분
- **예상 파일**: `.env.example`
- **예상 소요 시간**: 30분

### Task 9.3: TranslationManager에 설정 적용

- **분류**: 백엔드
- **의존성**: Task 9.1
- **작업 내용**:
  - `__init__` 파라미터를 config에서 로드
  - timeout, max_retries 지원 추가
  - max_tokens 제한 적용
- **예상 파일**: `components/translation.py`
- **예상 소요 시간**: 1시간

### Task 9.4: app.py에 설정 적용

- **분류**: 백엔드 + 프론트엔드
- **의존성**: Task 9.1, Task 9.3
- **작업 내용**:
  - config 모듈 import
  - 페이지 제목/아이콘을 config에서 로드
  - 레이아웃 모드를 config에서 로드
  - 기본 모델을 config에서 로드
  - 텍스트 영역 높이를 config에서 로드
- **예상 파일**: `app.py`
- **예상 소요 시간**: 1시간

### Task 9.5: utils.py에 설정 적용

- **분류**: 백엔드
- **의존성**: Task 9.1
- **작업 내용**:
  - 언어 감지 임계값을 config에서 로드
  - 상수 제거, config 사용으로 변경
- **예상 파일**: `utils.py`
- **예상 소요 시간**: 30분

### Task 9.6: 입력 길이 검증 구현

- **분류**: 백엔드 + 프론트엔드
- **의존성**: Task 9.1, Task 9.4
- **작업 내용**:
  - MAX_INPUT_LENGTH 초과 시 경고 표시
  - UI에 현재 길이 / 최대 길이 표시
  - 입력 제한 적용
- **예상 파일**: `app.py`
- **예상 소요 시간**: 45분

### Task 9.7: 단위 테스트 작성

- **분류**: 테스트
- **의존성**: Task 9.1 ~ Task 9.6
- **작업 내용**:
  - `Config` 클래스 테스트
    - 환경 변수 로드 테스트
    - 기본값 적용 테스트
    - 타입 변환 테스트
    - 잘못된 값 검증 테스트
  - 통합 테스트 (config 적용 후 동작 확인)
- **예상 파일**: `tests/test_config.py` (신규)
- **예상 소요 시간**: 1.5시간

### Task 9.8: 문서 업데이트

- **분류**: 문서
- **의존성**: Task 9.1 ~ Task 9.7
- **작업 내용**:
  - README.md: 환경 변수 설정 가이드 추가
  - CLAUDE.md: 설정 관리 개발 가이드 추가
  - PRD.md: 완료된 기능에 설정 관리 추가
- **예상 파일**: `README.md`, `CLAUDE.md`, `PRD.md`
- **예상 소요 시간**: 1시간

## 작업 흐름도

```text
Task 9.1 (설정 모듈 설계)
    │
    ├──→ Task 9.2 (.env.example 업데이트)
    │
    ├──→ Task 9.3 (TranslationManager)
    │       │
    │       └──→ Task 9.4 (app.py 적용)
    │               │
    │               ├──→ Task 9.5 (utils.py 적용)
    │               │
    │               └──→ Task 9.6 (입력 길이 검증)
    │
    └──→ Task 9.7 (단위 테스트)
            │
            └──→ Task 9.8 (문서 업데이트)
```

## 설정 항목 상세

### 우선순위별 설정 항목

#### Phase 1 (필수 - P0~P1)

```bash
# OpenAI API 설정
OPENAI_API_KEY=your_key
OPENAI_API_TIMEOUT=60
OPENAI_MAX_RETRIES=3

# AI 모델 설정
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.3

# 언어 감지 설정
LANGUAGE_DETECTION_THRESHOLD=0.5
```

#### Phase 2 (고급 기능 - P2)

```bash
# 입력/출력 제한
MAX_INPUT_LENGTH=50000
MAX_TOKENS=4000

# 애플리케이션 설정
APP_TITLE=영어-한국어 번역기
APP_ICON=🌐
```

#### Phase 3 (커스터마이징 - P3)

```bash
# UI 설정
APP_LAYOUT=centered
TEXT_AREA_HEIGHT=200

# 고급 설정
ENABLE_DEBUG_MODE=false
LOG_LEVEL=INFO
```

## 완료 기준

- [ ] `config.py` 모듈 구현 완료
- [ ] `.env.example`에 모든 설정 항목 추가
- [ ] 모든 하드코딩된 설정값을 config로 이전
- [ ] 환경 변수 미설정 시 기본값 정상 동작
- [ ] 잘못된 설정값 입력 시 명확한 에러 메시지
- [ ] 모든 단위 테스트 통과 (최소 15개 테스트)
- [ ] 문서 업데이트 완료 (README, CLAUDE, PRD)

## 테스트 계획

### 테스트 케이스

| ID | 테스트 시나리오 | 예상 결과 |
| -- | --------------- | --------- |
| TC-1 | 환경 변수 전체 설정 | 모든 값이 config에 반영됨 |
| TC-2 | 환경 변수 미설정 | 기본값으로 정상 동작 |
| TC-3 | 잘못된 타입 입력 (temperature="abc") | ValueError 발생 및 명확한 메시지 |
| TC-4 | 범위 초과 값 (temperature=2.0) | ValueError 발생 |
| TC-5 | DEFAULT_MODEL 변경 | UI 기본 선택 모델 변경 확인 |
| TC-6 | APP_TITLE/ICON 변경 | 페이지 제목/아이콘 변경 확인 |
| TC-7 | MAX_INPUT_LENGTH 초과 | 경고 메시지 표시 |
| TC-8 | API_TIMEOUT 적용 | OpenAI API 호출 시 timeout 적용 |

### 단위 테스트

```python
# tests/test_config.py

def test_config_load_from_env():
    """환경 변수에서 설정 로드 테스트"""
    os.environ['DEFAULT_MODEL'] = 'gpt-4'
    config = Config.load()
    assert config.DEFAULT_MODEL == 'gpt-4'

def test_config_default_values():
    """기본값 적용 테스트"""
    config = Config.load()
    assert config.DEFAULT_MODEL == 'gpt-4o-mini'
    assert config.DEFAULT_TEMPERATURE == 0.3

def test_config_type_conversion():
    """타입 변환 테스트"""
    os.environ['DEFAULT_TEMPERATURE'] = '0.5'
    config = Config.load()
    assert isinstance(config.DEFAULT_TEMPERATURE, float)
    assert config.DEFAULT_TEMPERATURE == 0.5

def test_config_invalid_temperature():
    """잘못된 temperature 값 검증"""
    os.environ['DEFAULT_TEMPERATURE'] = '2.0'
    with pytest.raises(ValueError, match="0.0에서 1.0 사이"):
        Config.load()

def test_config_invalid_type():
    """잘못된 타입 검증"""
    os.environ['OPENAI_API_TIMEOUT'] = 'abc'
    with pytest.raises(ValueError, match="정수여야 합니다"):
        Config.load()
```

## 리스크 및 고려사항

| 리스크 | 영향도 | 대응 방안 |
| ------ | ------ | --------- |
| 기존 사용자 혼란 | 중 | 하위 호환성 유지, 기본값으로 동작 |
| 설정값 오타 | 중 | 타입 검증 및 명확한 에러 메시지 |
| 환경 변수 누락 | 낮 | 기본값 제공 |
| 보안 (API 키) | 높 | .env를 .gitignore에 유지 |

## Azure OpenAI 지원과의 관계

이 기능은 **Azure OpenAI 지원(FEATURE-008)의 기반**이 됩니다:

- `AI_PROVIDER` 설정 → config.py에서 관리
- `AZURE_*` 환경 변수 → config.py에서 로드
- Provider별 클라이언트 생성 → config 값에 따라 분기

**권장 순서**: FEATURE-009 완료 → FEATURE-008 구현

## 참고 자료

- [The Twelve-Factor App - Config](https://12factor.net/config)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [pydantic - Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

## 진행 현황

### Task별 완료 상태

| Task | 제목 | 상태 | 예상 시간 | 실제 시간 | 완료일 | 커밋 | 이슈 |
| ---- | ---- | ---- | --------- | --------- | ------ | ---- | ---- |
| 9.1 | 설정 모듈 설계 및 구현 | ✅ 완료 | 1.5h | 1.5h | 2026-01-29 | [4157051](https://github.com/sirius2k/transbot/commit/4157051) | [#2](https://github.com/sirius2k/transbot/issues/2) |
| 9.2 | .env.example 업데이트 | ✅ 완료 | 30m | 30m | 2026-01-29 | [c9430f9](https://github.com/sirius2k/transbot/commit/c9430f9) | [#3](https://github.com/sirius2k/transbot/issues/3) |
| 9.3 | TranslationManager 적용 | ✅ 완료 | 1h | 2m | 2026-01-29 | [930e3e3](https://github.com/sirius2k/transbot/commit/930e3e3) | [#4](https://github.com/sirius2k/transbot/issues/4) |
<!-- Task 9.3: 시작 2026-01-29 20:44, 종료 2026-01-29 20:46, 실제 2분 -->
| 9.4 | app.py에 설정 적용 | ✅ 완료 | 1h | 11m | 2026-01-30 | [9424dfc](https://github.com/sirius2k/transbot/commit/9424dfc) | [#5](https://github.com/sirius2k/transbot/issues/5) |
<!-- Task 9.4: 시작 2026-01-29 20:49, 종료 2026-01-30 00:00, 실제 작업 11분 -->
| 9.5 | utils.py에 설정 적용 | ✅ 완료 | 30m | 1m | 2026-01-30 | [616e733](https://github.com/sirius2k/transbot/commit/616e733) | [#6](https://github.com/sirius2k/transbot/issues/6) |
<!-- Task 9.5: 시작 2026-01-30 00:05, 종료 2026-01-30 00:06, 실제 작업 1분 -->
| 9.6 | 입력 길이 검증 구현 | 🔲 대기 | 45m | - | - | - | [#7](https://github.com/sirius2k/transbot/issues/7) |
| 9.7 | 단위 테스트 작성 | 🔲 대기 | 1.5h | - | - | - | [#8](https://github.com/sirius2k/transbot/issues/8) |
| 9.8 | 문서 업데이트 | 🔲 대기 | 1h | - | - | - | [#9](https://github.com/sirius2k/transbot/issues/9) |

### 전체 진행률

- **예상 총 시간**: 8시간
- **실제 소요 시간**: 2시간 14분
- **진행률**: 62.5% (5/8 완료)
- **남은 시간**: 3시간 15분 (예상)
- **완료 예정일**: 2026-01-30 (예상)

### 주요 마일스톤

- ✅ **Phase 1 완료**: 핵심 인프라 (Task 9.1 완료)
- 🔲 **Phase 2 진행 중**: 코드베이스 적용 (Task 9.2-9.5)
- 🔲 **Phase 3 대기**: 고급 기능 (Task 9.6)
- 🔲 **Phase 4 대기**: 검증 및 문서화 (Task 9.7-9.8)

---

**작성일**: 2026년 1월 29일
**최종 수정일**: 2026년 1월 30일 00:06
**작성자**: TransBot Development Team
