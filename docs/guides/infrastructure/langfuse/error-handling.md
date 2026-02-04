# Langfuse 에러 핸들링 가이드

Langfuse는 LLM 관찰성을 위한 선택적 기능입니다. Langfuse 초기화 또는 추적 중 에러가 발생해도 TransBot의 핵심 번역 기능은 중단되지 않아야 합니다.

이 문서는 Langfuse 에러 핸들링 설계와 4가지 주요 에러 시나리오에 대한 처리 방법을 설명합니다.

## 설계 원칙

### 1. 번역 기능 우선 (Translation First)

Langfuse는 보조 기능이며, 에러가 발생해도 번역 기능에 영향을 주지 않아야 합니다.

```python
# ❌ 잘못된 예: Langfuse 에러가 번역을 중단
if not langfuse.track():
    raise Exception("Langfuse 추적 실패")

# ✅ 올바른 예: Langfuse 에러를 무시하고 번역 계속 진행
try:
    langfuse.track()
except Exception as e:
    print(f"⚠️ Langfuse 추적 실패: {e}")
    # 번역은 계속 진행
```

### 2. Graceful Degradation

Langfuse가 비활성화되거나 실패한 경우, 모든 추적 메서드는 no-op으로 동작합니다.

```python
# LangfuseObserver의 모든 메서드는 no-op 동작 지원
if not self._client or self._init_failed:
    return  # 아무 작업도 하지 않고 즉시 반환
```

### 3. 조용한 실패 (Silent Failure)

Langfuse 에러는 콘솔에만 출력되고 사용자 UI에는 표시되지 않습니다.

```python
# 에러 메시지는 print()로 출력 (개발자 디버깅용)
print(f"⚠️ Langfuse 초기화 실패 (추적 비활성화): {e}")

# ❌ st.error()로 사용자에게 표시하지 않음
# st.error(f"Langfuse 에러: {e}")  # 사용자는 알 필요 없음
```

## 에러 핸들링 구조

### LangfuseObserver 클래스

`components/observability.py`의 `LangfuseObserver` 클래스는 다음과 같은 에러 핸들링 구조를 가집니다.

```python
class LangfuseObserver:
    def __init__(self, config: Config):
        self.config = config
        self._client: Optional[Langfuse] = None
        self._init_failed = False

        # 1. 환경 변수 미설정 시 조기 반환
        if not self.config.langfuse_enabled:
            return

        # 2. 초기화 에러 처리
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

    def track_translation(self, ...):
        # 3. 클라이언트 없거나 초기화 실패 시 no-op
        if not self._client or self._init_failed:
            return

        # 4. 추적 중 에러 처리
        try:
            self._client.trace(...)
        except TimeoutError:
            print("⚠️ Langfuse 전송 타임아웃 (추적 건너뜀)")
        except Exception as e:
            print(f"⚠️ Langfuse 추적 실패: {type(e).__name__}: {e}")
```

### Config 클래스

`config.py`의 `Config` 클래스는 Langfuse 활성화 여부를 확인하는 프로퍼티를 제공합니다.

```python
@property
def langfuse_enabled(self) -> bool:
    """Langfuse가 활성화되었는지 확인합니다.

    Returns:
        bool: 3개 환경 변수가 모두 설정된 경우 True, 그렇지 않으면 False
    """
    return all([
        self.LANGFUSE_PUBLIC_KEY,
        self.LANGFUSE_SECRET_KEY,
        self.LANGFUSE_HOST
    ])
```

## 4가지 에러 시나리오

### 시나리오 1: 환경 변수 미설정

**상황**: Langfuse 환경 변수가 설정되지 않은 경우

**원인**:

- `.env` 파일에 Langfuse 환경 변수가 주석 처리됨
- 환경 변수가 아예 정의되지 않음

**동작**:

1. `Config.langfuse_enabled`가 `False` 반환
2. `LangfuseObserver.__init__()`에서 조기 반환
3. `LangfuseObserver._client`는 `None`으로 유지
4. 모든 추적 메서드는 no-op으로 동작

**에러 로그**: 없음 (정상적인 비활성화 상태)

**테스트 방법**:

```bash
# .env 파일에서 Langfuse 환경 변수 주석 처리
# LANGFUSE_PUBLIC_KEY=pk-...
# LANGFUSE_SECRET_KEY=sk-...
# LANGFUSE_HOST=http://localhost:3000

# 앱 실행
streamlit run app.py

# 번역 기능 정상 동작 확인
```

**예상 결과**:

- 번역 기능 정상 동작
- Langfuse 추적 없음
- 에러 메시지 없음

### 시나리오 2: 잘못된 API 키

**상황**: Langfuse API 키가 잘못 설정된 경우

**원인**:

- Public Key 또는 Secret Key가 잘못됨
- API 키가 만료됨
- API 키가 삭제됨

**동작**:

1. `Config.langfuse_enabled`가 `True` 반환
2. `LangfuseObserver.__init__()`에서 클라이언트 초기화 시도
3. 초기화는 성공할 수 있음 (인증은 나중에 실패)
4. `track_translation()` 호출 시 인증 에러 발생
5. 에러가 catch되어 콘솔에 출력
6. 번역 기능은 계속 진행

**에러 로그 예시**:

```text
⚠️ Langfuse 추적 실패: HTTPError: 401 Unauthorized
```

**테스트 방법**:

```bash
# .env 파일에 잘못된 API 키 설정
LANGFUSE_PUBLIC_KEY=pk-invalid-key
LANGFUSE_SECRET_KEY=sk-invalid-key
LANGFUSE_HOST=http://localhost:3000

# 앱 실행
streamlit run app.py

# 번역 수행 후 콘솔 로그 확인
```

**예상 결과**:

- 번역 기능 정상 동작
- 콘솔에 인증 에러 메시지 출력
- UI에는 에러 표시 없음

**문제 해결**:

1. Langfuse 대시보드에서 API 키 확인
2. 올바른 API 키를 `.env` 파일에 입력
3. 앱 재시작

### 시나리오 3: Langfuse 서버 다운

**상황**: Langfuse 서버가 실행되지 않거나 응답하지 않는 경우

**원인**:

- Langfuse Docker 컨테이너가 중지됨
- Langfuse 서버가 크래시됨
- 네트워크 연결 끊김

**동작**:

1. `Config.langfuse_enabled`가 `True` 반환
2. `LangfuseObserver.__init__()`에서 클라이언트 초기화 시도
3. 초기화는 성공할 수 있음 (연결은 나중에 실패)
4. `track_translation()` 호출 시 연결 에러 발생
5. 에러가 catch되어 콘솔에 출력
6. 번역 기능은 계속 진행

**에러 로그 예시**:

```text
⚠️ Langfuse 추적 실패: ConnectionError: Failed to connect to Langfuse
```

**테스트 방법**:

```bash
# Langfuse 컨테이너 중지
docker-compose -f infra/docker-compose.yml stop langfuse

# 앱 실행
streamlit run app.py

# 번역 수행 후 콘솔 로그 확인

# Langfuse 컨테이너 재시작
docker-compose -f infra/docker-compose.yml start langfuse
```

**예상 결과**:

- 번역 기능 정상 동작
- 콘솔에 연결 에러 메시지 출력
- UI에는 에러 표시 없음

**문제 해결**:

1. Langfuse 컨테이너 상태 확인:
   ```bash
   docker ps | grep langfuse
   ```

2. Langfuse 컨테이너 재시작:
   ```bash
   cd infra
   ./scripts/start.sh
   ```

3. Langfuse 헬스 체크:
   ```bash
   cd infra
   ./scripts/health-check.sh
   ```

### 시나리오 4: 네트워크 타임아웃

**상황**: Langfuse 서버 응답이 매우 느리거나 네트워크가 불안정한 경우

**원인**:

- 잘못된 LANGFUSE_HOST URL 설정
- 네트워크 지연
- 방화벽 차단
- DNS 해석 실패

**동작**:

1. `Config.langfuse_enabled`가 `True` 반환
2. `LangfuseObserver.__init__()`에서 클라이언트 초기화 시도
3. `timeout=5` 설정으로 5초 후 타임아웃
4. 초기화 에러 또는 추적 중 타임아웃 에러 발생
5. 에러가 catch되어 콘솔에 출력
6. 번역 기능은 계속 진행

**에러 로그 예시**:

```text
⚠️ Langfuse 초기화 실패 (추적 비활성화): TimeoutError
```

또는

```text
⚠️ Langfuse 전송 타임아웃 (추적 건너뜀)
```

**테스트 방법**:

```bash
# .env 파일에 존재하지 않는 URL 설정
LANGFUSE_PUBLIC_KEY=pk-test-key
LANGFUSE_SECRET_KEY=sk-test-key
LANGFUSE_HOST=http://192.0.2.1:3000  # TEST-NET-1 (존재하지 않는 IP)

# 앱 실행
streamlit run app.py

# 번역 수행 후 콘솔 로그 확인
```

**예상 결과**:

- 번역 기능 정상 동작
- 콘솔에 타임아웃 에러 메시지 출력
- UI에는 에러 표시 없음

**문제 해결**:

1. LANGFUSE_HOST URL 확인:
   ```bash
   curl http://localhost:3000/api/health
   ```

2. 올바른 URL을 `.env` 파일에 입력:
   ```bash
   # 로컬 개발
   LANGFUSE_HOST=http://localhost:3000

   # 프로덕션
   LANGFUSE_HOST=https://langfuse.yourdomain.com
   ```

3. 방화벽 및 네트워크 설정 확인

## 자동화된 테스트

4가지 에러 시나리오를 자동으로 테스트하는 스크립트를 제공합니다.

### 테스트 실행

```bash
# 프로젝트 루트에서 실행
python3 tests/manual/test_error_scenarios.py
```

### 테스트 출력 예시

```text
================================================================================
Langfuse 에러 핸들링 테스트 시작
================================================================================

================================================================================
시나리오 1: 환경 변수 미설정 테스트
================================================================================

✓ 환경 변수 백업 완료: /path/to/.env.backup
✓ 환경 변수 파일 수정 완료
ℹ LANGFUSE_PUBLIC_KEY: None
ℹ LANGFUSE_SECRET_KEY: None
ℹ LANGFUSE_HOST: None
ℹ langfuse_enabled: False
✓ Config.langfuse_enabled가 False로 설정됨
✓ LangfuseObserver._client가 None으로 설정됨
✓ LangfuseObserver._init_failed가 False임 (초기화 실패 없음)
ℹ track_translation 호출 테스트 (no-op 동작 확인)...
✓ track_translation이 에러 없이 실행됨 (no-op)
✓ 시나리오 1 테스트 통과!
✓ 환경 변수 복원 완료: /path/to/.env

[... 시나리오 2, 3, 4 출력 ...]

================================================================================
테스트 결과 요약
================================================================================

✓ 시나리오 1: 환경 변수 미설정: 통과
✓ 시나리오 2: 잘못된 API 키: 통과
✓ 시나리오 3: Langfuse 서버 다운: 통과
✓ 시나리오 4: 네트워크 타임아웃: 통과

총 4/4 시나리오 통과
✓ 모든 테스트 통과!
```

### 테스트 내부 동작

1. **환경 변수 백업**: 테스트 시작 전 `.env` 파일을 `.env.backup`으로 백업
2. **환경 변수 수정**: 각 시나리오에 맞게 `.env` 파일 수정
3. **모듈 재로드**: `config` 및 `components.observability` 모듈 재로드
4. **시나리오 테스트**: Config 로드, LangfuseObserver 초기화, track_translation 호출
5. **결과 검증**: 예상 동작과 실제 동작 비교
6. **환경 변수 복원**: 테스트 완료 후 `.env` 파일 복원

## 모니터링 및 디버깅

### 에러 로그 확인

Langfuse 에러는 콘솔에 다음 형식으로 출력됩니다.

```text
⚠️ Langfuse 초기화 실패 (추적 비활성화): <에러 메시지>
⚠️ Langfuse 추적 실패: <에러 타입>: <에러 메시지>
⚠️ Langfuse 전송 타임아웃 (추적 건너뜀)
⚠️ Langfuse flush 실패: <에러 메시지>
```

### 디버깅 체크리스트

Langfuse 추적이 동작하지 않을 때 다음 사항을 확인하세요.

#### 1. 환경 변수 확인

```bash
# Config 확인
python3 -c "
from config import Config
c = Config.load()
print(f'LANGFUSE_PUBLIC_KEY: {c.LANGFUSE_PUBLIC_KEY}')
print(f'LANGFUSE_SECRET_KEY: {c.LANGFUSE_SECRET_KEY}')
print(f'LANGFUSE_HOST: {c.LANGFUSE_HOST}')
print(f'langfuse_enabled: {c.langfuse_enabled}')
"
```

#### 2. Langfuse 서버 확인

```bash
# Langfuse 컨테이너 상태 확인
docker ps | grep langfuse

# Langfuse 헬스 체크
curl http://localhost:3000/api/health

# Langfuse 로그 확인
docker logs transbot-langfuse --tail 50
```

#### 3. 네트워크 연결 확인

```bash
# 로컬 Langfuse 연결 테스트
curl -I http://localhost:3000

# DNS 확인 (프로덕션)
nslookup langfuse.yourdomain.com
```

#### 4. API 키 확인

1. Langfuse 대시보드 접속: `http://localhost:3000`
2. Settings > API Keys 메뉴 확인
3. Public Key와 Secret Key가 `.env` 파일과 일치하는지 확인

## 프로덕션 권장사항

### 1. Langfuse 서버 모니터링

프로덕션 환경에서는 Langfuse 서버의 상태를 주기적으로 모니터링하세요.

```bash
# Cron 작업으로 헬스 체크 실행
*/5 * * * * curl -f http://localhost:3000/api/health || echo "Langfuse down" | mail -s "Alert" admin@example.com
```

### 2. 타임아웃 조정

네트워크 환경에 따라 타임아웃을 조정할 수 있습니다.

```python
# components/observability.py
self._client = Langfuse(
    public_key=config.LANGFUSE_PUBLIC_KEY,
    secret_key=config.LANGFUSE_SECRET_KEY,
    host=config.LANGFUSE_HOST,
    timeout=10  # 프로덕션에서는 10초로 증가
)
```

### 3. 로그 수집

에러 로그를 수집하여 모니터링 시스템에 전송하세요.

```python
import logging

logger = logging.getLogger(__name__)

# print() 대신 logger.warning() 사용
logger.warning(f"Langfuse 초기화 실패 (추적 비활성화): {e}")
```

### 4. 재시도 로직 (선택사항)

중요한 추적의 경우 재시도 로직을 추가할 수 있습니다.

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def track_with_retry(self, ...):
    self._client.trace(...)
```

## 관련 문서

- [Langfuse 공식 문서](https://langfuse.com/docs)
- [Langfuse Python SDK](https://github.com/langfuse/langfuse-python)
- [TransBot 인프라 가이드](../README.md)
- [개발 환경 설정](../environment-setup.md)

## 버전 정보

- **Langfuse 버전**: v2 (Stable)
- **Langfuse Python SDK**: langfuse>=2.0.0
- **마지막 업데이트**: 2026-02-04
- **작성자**: TransBot Development Team
