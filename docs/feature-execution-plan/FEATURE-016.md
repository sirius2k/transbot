# FEATURE-016: Langfuse 연동 (LLM 관찰성)

## 개요

- **기능명**: Langfuse 연동을 통한 LLM 관찰성 확보
- **상태**: 🔲 예정
- **분류**: 백엔드
- **우선순위**: P1 (높음)
- **복잡도**: Standard (4-10h)
- **분석 수준**: 부분
- **진행률**: 0%
- **예상 시간**: 8시간
- **실제 소요**: - (완료 후 기록)
- **시작일**: -
- **완료일**: -

## 기능 설명

Langfuse를 TransBot에 연동하여 LLM 사용 내역을 추적하고, 비용 분석, 품질 모니터링, 프롬프트 최적화를 위한 데이터를 수집합니다. 자체 호스팅 Langfuse 인스턴스에 연결하며, Langfuse 미연결 시에도 앱이 정상 동작하도록 구현합니다.

### 핵심 가치

- **비용 투명성**: LLM API 사용량 및 비용을 실시간으로 추적
- **품질 모니터링**: 번역 품질 문제 발생 시 원인 파악 가능
- **프롬프트 최적화**: 입력/출력 데이터 분석을 통한 프롬프트 개선
- **운영 인사이트**: 사용 패턴, 에러 발생률 등 운영 데이터 확보

## 배경 및 필요성

### 현재 문제점

1. **비용 분석 불가**: LLM 사용 내역을 추적할 수 없어 비용 분석이 어려움
2. **품질 문제 원인 파악 어려움**: 번역 품질 문제 발생 시 디버깅이 어려움
3. **프롬프트 최적화 데이터 부족**: 어떤 프롬프트가 효과적인지 데이터 기반 판단 불가

### 해결 방안

Langfuse를 통해 모든 LLM 요청을 추적하고, 다음 정보를 수집:

- **기본 정보**: 번역 시간, 사용된 AI 모델, 텍스트 길이, 응답 시간
- **비용 정보**: 입력/출력 토큰 수, 예상 비용, 누적 비용
- **품질 정보**: 프롬프트 전문, 번역 결과, 시스템 프롬프트, 에러 메시지
- **사용자 행동**: 번역 방향(영→한/한→영), 세션 정보, 재번역 여부

## 요구사항

### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| FR-16.1 | Langfuse SDK를 프로젝트에 설치하고 환경 변수 설정 | P0 |
| FR-16.2 | LangfuseObserver 클래스 구현 (추적 로직) | P0 |
| FR-16.3 | TranslationManager에 추적 로직 통합 | P0 |
| FR-16.4 | 세션 ID 생성 및 관리 (Streamlit session_state) | P0 |
| FR-16.5 | Langfuse 대시보드에서 데이터 확인 가능 | P1 |
| FR-16.6 | 에러 발생 시에도 추적 (에러 메시지 포함) | P1 |
| FR-16.7 | Langfuse 미연결 시 앱 정상 동작 (graceful degradation) | P0 |
| FR-16.8 | 네트워크 타임아웃 및 초기화 실패 처리 | P1 |

### 비기능 요구사항 (NFR)

| ID | 요구사항 | 목표 |
|----|----------|------|
| NFR-16.1 | 추적 실패 시에도 번역 기능 정상 동작 | 100% |
| NFR-16.2 | 추적 로직으로 인한 응답 시간 증가 | <100ms |
| NFR-16.3 | 코드 커버리지 | 80% 이상 |
| NFR-16.4 | 환경 변수 미설정 시 자동 비활성화 | 100% |

## 작업(Task) 분해

### Task 16.1: Langfuse SDK 설치 및 환경 설정

**설명**: Langfuse Python SDK를 설치하고 Config 클래스에 환경 변수 설정을 추가합니다.

**세부 작업**:
1. `requirements.txt`에 `langfuse>=2.0.0` 추가
2. `.env.example`에 Langfuse 환경 변수 템플릿 추가:
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_HOST` (자체 호스팅 URL)
3. `config.py`의 Config 클래스에 Langfuse 설정 추가:
   - `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` 속성
   - `langfuse_enabled` 프로퍼티 (3개 환경 변수 모두 설정되었는지 확인)
4. 환경 변수 미설정 시 None 반환 (선택적 기능)

**예상 시간**: 30분

**의존성**: 없음

**테스트 범위**:
- Config 클래스에서 Langfuse 환경 변수 로드 확인
- `langfuse_enabled` 프로퍼티 동작 확인 (True/False)
- 환경 변수 미설정 시 None 반환 확인

**완료 조건**:
- [x] requirements.txt에 langfuse 추가
- [x] .env.example 업데이트
- [x] config.py에 Langfuse 설정 추가
- [x] langfuse_enabled 프로퍼티 구현
- [x] 린팅 통과

**코드 예시**:

```python
# config.py
class Config:
    # ... 기존 코드 ...

    # Langfuse 설정
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: Optional[str] = None

    @classmethod
    def load(cls) -> 'Config':
        # ... 기존 로드 코드 ...

        # Langfuse 설정
        config.LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
        config.LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
        config.LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

        return config

    @property
    def langfuse_enabled(self) -> bool:
        """Langfuse가 활성화되었는지 확인"""
        return all([
            self.LANGFUSE_PUBLIC_KEY,
            self.LANGFUSE_SECRET_KEY,
            self.LANGFUSE_HOST
        ])
```

---

### Task 16.2: LangfuseObserver 클래스 구현

**설명**: Langfuse를 통해 LLM 사용 내역을 추적하는 핵심 클래스를 구현합니다.

**세부 작업**:
1. `components/observability.py` 파일 생성
2. `LangfuseObserver` 클래스 구현:
   - `__init__()`: Langfuse 클라이언트 초기화 (lazy)
   - `track_translation()`: 번역 요청 추적 (모든 정보 전송)
   - `flush()`: pending 데이터 강제 전송
3. 추적 정보 정의:
   - Input: source_text, source_lang, target_lang
   - Output: target_text
   - Metadata: model, direction, session_id
   - Usage: input_tokens, output_tokens, total
   - Status: ERROR (에러 시) / DEFAULT
4. Langfuse 미활성화 시 no-op 동작 (클라이언트 None)
5. 모든 Langfuse 관련 코드를 try-except로 감싸기
6. `components/__init__.py`에 LangfuseObserver export 추가

**예상 시간**: 2시간

**의존성**: Task 16.1

**테스트 범위**:
- Langfuse 활성화 시 클라이언트 초기화 확인
- Langfuse 비활성화 시 no-op 동작 확인
- track_translation() 호출 시 올바른 데이터 전송 확인
- 초기화 실패 시 graceful degradation 확인

**완료 조건**:
- [ ] components/observability.py 파일 생성
- [ ] LangfuseObserver 클래스 구현
- [ ] 모든 메서드에 타입 힌트 및 docstring 작성
- [ ] 에러 핸들링 구현
- [ ] __init__.py에 export 추가
- [ ] 린팅 통과

**코드 예시**:

```python
# components/observability.py
from typing import Optional
from langfuse import Langfuse
from config import Config

class LangfuseObserver:
    """Langfuse를 통한 LLM 관찰성 추적 클래스"""

    def __init__(self, config: Config):
        """LangfuseObserver 초기화

        Args:
            config: 설정 객체
        """
        self.config = config
        self._client: Optional[Langfuse] = None
        self._init_failed = False

        if not self.config.langfuse_enabled:
            return

        try:
            self._client = Langfuse(
                public_key=config.LANGFUSE_PUBLIC_KEY,
                secret_key=config.LANGFUSE_SECRET_KEY,
                host=config.LANGFUSE_HOST,
                timeout=5  # 5초 타임아웃
            )
        except Exception as e:
            self._init_failed = True
            print(f"⚠️ Langfuse 초기화 실패 (추적 비활성화): {e}")
            self._client = None

    def track_translation(
        self,
        source_text: str,
        target_text: str,
        source_lang: str,
        target_lang: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        session_id: str,
        error: Optional[str] = None
    ) -> None:
        """번역 요청 추적"""
        if not self._client or self._init_failed:
            return

        try:
            self._client.trace(
                name="translation",
                input={
                    "source_text": source_text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                },
                output={"target_text": target_text},
                metadata={
                    "model": model,
                    "direction": f"{source_lang}→{target_lang}",
                    "session_id": session_id,
                    "latency_ms": latency_ms,
                },
                usage={
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens,
                },
                level="ERROR" if error else "DEFAULT",
                status_message=error,
            )
        except TimeoutError:
            print("⚠️ Langfuse 전송 타임아웃 (추적 건너뜀)")
        except Exception as e:
            print(f"⚠️ Langfuse 추적 실패: {type(e).__name__}: {e}")

    def flush(self) -> None:
        """Pending 데이터를 Langfuse로 전송"""
        if self._client:
            try:
                self._client.flush()
            except Exception as e:
                print(f"⚠️ Langfuse flush 실패: {e}")
```

---

### Task 16.3: TranslationManager에 Langfuse 추적 통합

**설명**: `TranslationManager` 클래스의 `translate()` 메서드에 Langfuse 추적 로직을 통합합니다.

**세부 작업**:
1. `TranslationManager.__init__()` 메서드 수정:
   - `LangfuseObserver` 인스턴스 생성 및 저장
2. `translate()` 메서드 수정:
   - 번역 시작 시간 기록 (`time.time()`)
   - 번역 완료 후 응답 시간 계산 (밀리초)
   - 입력/출력 토큰 수 계산 (`count_tokens()` 함수 사용)
   - 세션 ID 매개변수 추가
   - `LangfuseObserver.track_translation()` 호출 (finally 블록에서)
3. 에러 발생 시에도 추적 (에러 메시지 포함)
4. 추적 로직 실패 시에도 번역 기능 정상 동작

**예상 시간**: 1.5시간

**의존성**: Task 16.2

**테스트 범위**:
- 번역 성공 시 추적 데이터 전송 확인
- 번역 실패 시에도 에러 정보와 함께 추적 확인
- 추적 로직 실패 시 번역 기능 정상 동작 확인
- 응답 시간 측정 정확도 확인

**완료 조건**:
- [ ] TranslationManager.__init__()에 LangfuseObserver 추가
- [ ] translate() 메서드에 추적 로직 통합
- [ ] 세션 ID 매개변수 추가
- [ ] 에러 핸들링 구현 (finally 블록)
- [ ] 기존 번역 기능 정상 동작 확인
- [ ] 린팅 통과

**코드 예시**:

```python
# components/translation.py
import time
from components.observability import LangfuseObserver
from utils import count_tokens

class TranslationManager:
    def __init__(self, config: Config):
        # ... 기존 코드 ...
        self.observer = LangfuseObserver(config)

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        session_id: str  # 새 매개변수
    ) -> str:
        """번역 수행 및 추적"""
        start_time = time.time()
        input_tokens = count_tokens(text, self.model)
        error_msg = None
        result = ""

        try:
            # 기존 번역 로직
            result = self._perform_translation(text, source_lang, target_lang)
            output_tokens = count_tokens(result, self.model)
        except Exception as e:
            error_msg = str(e)
            output_tokens = 0
            raise
        finally:
            # 추적 (성공/실패 모두)
            latency_ms = (time.time() - start_time) * 1000
            try:
                self.observer.track_translation(
                    source_text=text,
                    target_text=result,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    model=self.model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                    session_id=session_id,
                    error=error_msg
                )
            except Exception as track_error:
                print(f"⚠️ 추적 실패 (번역은 성공): {track_error}")

        return result
```

---

### Task 16.4: app.py에 세션 ID 생성 및 전달

**설명**: Streamlit의 `session_state`를 사용하여 세션 ID를 생성하고, 번역 호출 시 전달합니다.

**세부 작업**:
1. `app.py`의 `main()` 함수 수정:
   - 세션 ID 생성 (최초 1회, `uuid.uuid4()` 사용)
   - `st.session_state.session_id`에 저장
2. 번역 호출 시 세션 ID 전달:
   - `translation_manager.translate()` 호출 시 `session_id` 매개변수 추가
3. 페이지 새로고침 시에도 세션 ID 유지 확인

**예상 시간**: 30분

**의존성**: Task 16.3

**테스트 범위**:
- 세션 ID가 한 번만 생성되는지 확인
- 페이지 새로고침 시 세션 ID 유지 확인
- 번역 호출 시 세션 ID가 TranslationManager에 전달되는지 확인

**완료 조건**:
- [ ] main() 함수에 세션 ID 생성 로직 추가
- [ ] translate() 호출 시 session_id 전달
- [ ] 세션 ID 생성 및 유지 확인
- [ ] 린팅 통과

**코드 예시**:

```python
# app.py
import uuid
import streamlit as st

def main():
    """메인 함수"""
    # ... 기존 코드 ...

    # 세션 ID 생성 (최초 1회)
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # ... 번역 로직 ...

    if st.button("번역", type="primary", use_container_width=True):
        # 번역 호출 시 세션 ID 전달
        result = translation_manager.translate(
            text=user_input,
            source_lang=source_lang,
            target_lang=target_lang,
            session_id=st.session_state.session_id  # 세션 ID 전달
        )
```

---

### Task 16.5: Langfuse 대시보드 연결 및 데이터 검증

**설명**: 자체 호스팅 Langfuse 인스턴스에 실제로 연결하고, 추적 데이터가 정상적으로 표시되는지 검증합니다.

**세부 작업**:
1. 자체 호스팅 Langfuse 인스턴스 설정 (Docker 등)
2. Langfuse 대시보드에서 API 키 생성
3. TransBot `.env` 파일에 Langfuse 환경 변수 설정
4. TransBot 실행 및 테스트 번역 수행:
   - 영어 → 한국어 번역
   - 한국어 → 영어 번역
   - 에러 케이스 (빈 텍스트, API 키 제거 등)
5. Langfuse 대시보드에서 추적 데이터 확인:
   - Trace 목록에 "translation" 표시
   - Input/Output 데이터 정상 표시
   - Metadata (model, direction, session_id) 표시
   - Usage (토큰 수) 표시
   - 응답 시간 (latency_ms) 표시
   - 에러 케이스에서 ERROR 레벨 표시

**예상 시간**: 1시간

**의존성**: Task 16.4

**테스트 범위**:
- Langfuse 대시보드에서 모든 추적 데이터 확인
- 에러 케이스 추적 확인
- 세션 ID가 동일한 번역들이 그룹핑되는지 확인

**완료 조건**:
- [ ] Langfuse 인스턴스 설정 완료
- [ ] API 키 생성 및 .env 설정
- [ ] 테스트 번역 수행 (정상/에러)
- [ ] 대시보드에서 모든 데이터 확인
- [ ] 스크린샷 또는 확인 로그 첨부

---

### Task 16.6: 에러 핸들링 강화

**설명**: Langfuse 연결 실패, 네트워크 오류 등의 상황에서도 TransBot이 정상 동작하도록 에러 핸들링을 강화합니다.

**세부 작업**:
1. `LangfuseObserver.__init__()` 에러 핸들링:
   - 초기화 실패 시 `_init_failed = True` 설정
   - 에러 로그 출력 (사용자에게는 표시 안 함)
2. `track_translation()` 에러 핸들링:
   - TimeoutError 별도 처리
   - 모든 Exception catch 및 로그 출력
3. 다음 시나리오 테스트:
   - Langfuse 환경 변수 미설정 → 앱 정상 동작
   - 잘못된 API 키 → 앱 정상 동작
   - Langfuse 서버 다운 → 앱 정상 동작
   - 네트워크 끊김 → 앱 정상 동작

**예상 시간**: 1시간

**의존성**: Task 16.2, 16.3

**테스트 범위**:
- 모든 에러 시나리오에서 번역 기능 정상 동작 확인
- 에러 로그 출력 확인
- 사용자에게 에러 메시지가 표시되지 않는지 확인

**완료 조건**:
- [ ] 모든 에러 시나리오 테스트
- [ ] 각 시나리오에서 번역 기능 정상 동작 확인
- [ ] 에러 로깅 확인
- [ ] 린팅 통과

---

### Task 16.7: 단위 테스트 작성

**설명**: `LangfuseObserver` 클래스의 단위 테스트를 작성합니다.

**세부 작업**:
1. `tests/test_observability.py` 파일 생성
2. 다음 테스트 케이스 작성:
   - `test_langfuse_observer_init_success`: Langfuse 활성화 시 초기화 성공
   - `test_langfuse_observer_disabled`: Langfuse 비활성화 시 no-op 동작
   - `test_track_translation_success`: 추적 성공
   - `test_track_translation_with_error`: 에러 포함 추적
   - `test_langfuse_init_failure`: 초기화 실패 시 graceful degradation
   - `test_track_translation_failure`: 추적 실패 시 no-op
3. `unittest.mock`을 사용하여 Langfuse 클라이언트 Mock
4. 실제 네트워크 호출 없이 테스트
5. pytest fixture 활용 (mock_config)

**예상 시간**: 1.5시간

**의존성**: Task 16.2

**테스트 범위**:
- 모든 LangfuseObserver 메서드
- 정상/에러 케이스 모두 커버
- 코드 커버리지 80% 이상

**완료 조건**:
- [ ] tests/test_observability.py 파일 생성
- [ ] 6개 이상 테스트 케이스 작성
- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 80% 이상
- [ ] 린팅 통과

**코드 예시**:

```python
# tests/test_observability.py
import pytest
from unittest.mock import Mock, patch
from components.observability import LangfuseObserver
from config import Config

@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.LANGFUSE_PUBLIC_KEY = "pk-test"
    config.LANGFUSE_SECRET_KEY = "sk-test"
    config.LANGFUSE_HOST = "http://localhost:3000"
    config.langfuse_enabled = True
    return config

@patch('components.observability.Langfuse')
def test_langfuse_observer_init_success(mock_langfuse, mock_config):
    """Langfuse 초기화 성공 테스트"""
    observer = LangfuseObserver(mock_config)
    assert observer._client is not None
    mock_langfuse.assert_called_once()

def test_langfuse_observer_disabled():
    """Langfuse 비활성화 시 no-op 테스트"""
    config = Mock(spec=Config)
    config.langfuse_enabled = False
    observer = LangfuseObserver(config)
    assert observer._client is None

    # track_translation 호출해도 에러 없음
    observer.track_translation(
        source_text="Hello",
        target_text="안녕하세요",
        source_lang="en",
        target_lang="ko",
        model="gpt-4o",
        input_tokens=10,
        output_tokens=15,
        latency_ms=500,
        session_id="test-session"
    )

@patch('components.observability.Langfuse')
def test_track_translation_success(mock_langfuse, mock_config):
    """추적 성공 테스트"""
    observer = LangfuseObserver(mock_config)
    mock_client = Mock()
    observer._client = mock_client

    observer.track_translation(
        source_text="Hello",
        target_text="안녕하세요",
        source_lang="en",
        target_lang="ko",
        model="gpt-4o",
        input_tokens=10,
        output_tokens=15,
        latency_ms=500,
        session_id="test-session"
    )

    mock_client.trace.assert_called_once()
```

---

### Task 16.8: 문서화

**설명**: Langfuse 연동 사용법을 문서화합니다.

**세부 작업**:
1. `docs/guides/infrastructure/langfuse/` 폴더 생성
2. `setup.md` 작성:
   - Langfuse 자체 호스팅 설치 방법 (Docker Compose)
   - API 키 생성 방법
   - TransBot 환경 변수 설정
3. `usage.md` 작성:
   - Langfuse 대시보드 접속 방법
   - 추적 데이터 확인 방법
   - 유용한 필터 및 검색 방법
4. `README.md` 업데이트:
   - Langfuse 관찰성 기능 소개 추가
5. `CLAUDE.md` 업데이트:
   - Langfuse 개발 가이드 추가
   - components/observability.py 설명 추가

**예상 시간**: 1.5시간

**의존성**: Task 16.5 (검증 완료 후)

**테스트 범위**:
- 문서를 따라 Langfuse를 설정할 수 있는지 확인
- 모든 링크 정상 작동 확인
- Markdownlint 규칙 준수 확인

**완료 조건**:
- [ ] docs/guides/infrastructure/langfuse/setup.md 작성
- [ ] docs/guides/infrastructure/langfuse/usage.md 작성
- [ ] README.md 업데이트
- [ ] CLAUDE.md 업데이트
- [ ] Markdownlint 통과

## 작업 흐름도

```text
Task 16.1 (환경 설정)
    ↓
Task 16.2 (LangfuseObserver 구현) ────────────┐
    ↓                                        ↓
Task 16.3 (TranslationManager 통합)   Task 16.7 (단위 테스트)
    ↓                                        ↓
Task 16.4 (세션 ID 생성)               Task 16.6 (에러 핸들링)
    ↓
Task 16.5 (대시보드 검증)
    ↓
Task 16.8 (문서화)
```

### 병렬 작업 가능

- Task 16.6 (에러 핸들링)과 Task 16.7 (단위 테스트)는 병렬 수행 가능
- Task 16.5 (대시보드 검증) 후 Task 16.8 (문서화) 독립 수행

## 진행 현황

| Task | 상태 | 담당자 | 시작일 | 완료일 | 소요 시간 |
|------|------|--------|--------|--------|-----------|
| 16.1 | ✅ 완료 | Claude | 2026-02-03 | 2026-02-03 | ~30m |
| 16.2 | 🔲 예정 | - | - | - | - |
| 16.3 | 🔲 예정 | - | - | - | - |
| 16.4 | 🔲 예정 | - | - | - | - |
| 16.5 | 🔲 예정 | - | - | - | - |
| 16.6 | 🔲 예정 | - | - | - | - |
| 16.7 | 🔲 예정 | - | - | - | - |
| 16.8 | 🔲 예정 | - | - | - | - |

## 완료 기준

### 기능 완료 기준

- [ ] Langfuse SDK 설치 및 환경 설정 완료
- [ ] LangfuseObserver 클래스 구현 완료
- [ ] TranslationManager에 추적 로직 통합 완료
- [ ] 세션 ID 생성 및 관리 완료
- [ ] Langfuse 대시보드에서 모든 추적 데이터 확인 가능
- [ ] Langfuse 미연결 시 앱 정상 동작 확인
- [ ] 모든 에러 시나리오 테스트 통과

### 품질 기준

- [ ] 코드 커버리지 80% 이상
- [ ] 모든 테스트 통과
- [ ] 린팅 통과
- [ ] Markdownlint 통과 (문서)

### 문서화 기준

- [ ] Langfuse 설치 및 설정 가이드 작성
- [ ] Langfuse 사용법 가이드 작성
- [ ] README.md 및 CLAUDE.md 업데이트

## 테스트 계획

### 단위 테스트

| 테스트 케이스 | 시나리오 | 예상 결과 |
|--------------|----------|-----------|
| test_langfuse_observer_init_success | Langfuse 활성화 시 초기화 | 클라이언트 생성 성공 |
| test_langfuse_observer_disabled | Langfuse 비활성화 | no-op 동작 |
| test_track_translation_success | 정상 추적 | trace 호출 확인 |
| test_track_translation_with_error | 에러 포함 추적 | ERROR 레벨로 추적 |
| test_langfuse_init_failure | 초기화 실패 | graceful degradation |
| test_track_translation_failure | 추적 실패 | no-op, 에러 로그만 |

### 통합 테스트

| 테스트 케이스 | 시나리오 | 예상 결과 |
|--------------|----------|-----------|
| 정상 번역 + 추적 | 영어 → 한국어 번역 | Langfuse 대시보드에 추적 데이터 표시 |
| 에러 번역 + 추적 | API 키 제거 후 번역 | ERROR 레벨로 추적 |
| Langfuse 미연결 | 환경 변수 미설정 | 번역 기능 정상 동작 |
| 네트워크 타임아웃 | Langfuse 서버 다운 | 번역 기능 정상 동작 |

## 리스크 및 대응 방안

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|-----------|
| Langfuse 버전 호환성 문제 | 중 | 최신 안정 버전 사용, 버전 고정 |
| 네트워크 지연으로 인한 성능 저하 | 중 | 타임아웃 설정 (5초), 비동기 전송 |
| 추적 데이터 과다 저장 | 낮 | Langfuse 데이터 보관 정책 설정 |
| 환경 변수 누락으로 인한 혼란 | 낮 | .env.example에 명확한 주석 추가 |

## 참고 자료

### 외부 문서

- [Langfuse 공식 문서](https://langfuse.com/docs)
- [Langfuse Python SDK](https://github.com/langfuse/langfuse-python)
- [Langfuse Self-Hosting Guide](https://langfuse.com/docs/deployment/self-host)

### 내부 문서

- [config.py 설명](../../guides/infrastructure/config-management.md)
- [TranslationManager 설명](../../guides/development/components-guide.md)
- [테스트 가이드](../../guides/quality/testing-guide.md)

---

**작성일**: 2026-02-02
**최종 수정일**: 2026-02-02
**작성자**: TransBot Development Team
