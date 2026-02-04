# Langfuse 설정 가이드

Langfuse는 LLM 애플리케이션을 위한 오픈소스 관찰성 플랫폼입니다. TransBot에서 Langfuse를 사용하면 번역 요청을 추적하고, 비용을 분석하며, 번역 품질을 모니터링할 수 있습니다.

이 가이드는 Langfuse v2를 자체 호스팅 방식으로 설치하고 TransBot과 연동하는 방법을 설명합니다.

## 개요

### Langfuse란?

Langfuse는 다음과 같은 기능을 제공하는 LLM 관찰성 플랫폼입니다:

- **프롬프트 추적**: OpenAI API 호출을 자동으로 로깅
- **비용 분석**: 토큰 사용량 및 비용 대시보드
- **성능 모니터링**: 응답 시간, 에러율 추적
- **세션 추적**: 사용자 세션별 LLM 호출 그룹핑
- **프롬프트 버전 관리**: 프롬프트 변경 이력 관리

### 왜 자체 호스팅인가?

TransBot은 Langfuse를 자체 호스팅 방식으로 사용합니다.

**장점**:

- 데이터 프라이버시: 모든 데이터가 로컬에 저장됨
- 비용 절감: 클라우드 서비스 비용 없음
- 완전한 제어: 설정 및 데이터 관리 자유

**단점**:

- 인프라 관리 필요: Docker Compose 설정 및 관리
- 업그레이드 수동: 버전 업그레이드를 직접 수행

### Langfuse v2 vs v3

TransBot은 현재 Langfuse v2를 사용합니다.

| 특징 | v2 (Stable) | v3 (Latest) |
| --- | --- | --- |
| **데이터베이스** | PostgreSQL | PostgreSQL + ClickHouse |
| **성능** | 중소 규모 적합 | 대용량 처리 최적화 |
| **설치 복잡도** | 간단 | 추가 ClickHouse 필요 |
| **안정성** | 매우 안정적 | 안정화 진행 중 |

> **참고**: v3는 대용량 이벤트 처리를 위해 ClickHouse를 추가로 요구하지만, TransBot의 현재 규모에서는 v2로 충분합니다. v3 업그레이드는 향후 고려될 예정입니다.

## Langfuse 자체 호스팅 설치 (Docker Compose)

TransBot은 Docker Compose 기반 인프라를 제공하며, Langfuse가 포함되어 있습니다.

### 1단계: 인프라 환경 변수 설정

```bash
cd infra
cp .env.infra.example .env.infra
```

`.env.infra` 파일을 열어 다음 환경 변수를 설정하세요:

```bash
# PostgreSQL 설정 (Langfuse 메타데이터 저장)
POSTGRES_DB=transbot
POSTGRES_USER=transbot_user
POSTGRES_PASSWORD=your_secure_password_here  # 강력한 비밀번호로 변경

# Langfuse 설정
LANGFUSE_URL=http://localhost:3000
LANGFUSE_SECRET=random-string-at-least-32-characters-long  # 최소 32자 이상
LANGFUSE_SALT=another-random-string-for-salt  # 랜덤 문자열
LANGFUSE_PORT=3000

# Redis 설정 (캐싱)
REDIS_PASSWORD=your_redis_password_here  # 강력한 비밀번호로 변경
REDIS_PORT=6379
```

> **보안 팁**: `LANGFUSE_SECRET`과 `LANGFUSE_SALT`는 다음 명령으로 생성할 수 있습니다:
>
> ```bash
> openssl rand -hex 32
> ```

### 2단계: 인프라 서비스 시작

```bash
cd infra
./scripts/start.sh
```

이 스크립트는 다음 서비스를 시작합니다:

- **PostgreSQL** (포트 5432): Langfuse 메타데이터 및 이벤트 저장
- **Langfuse** (포트 3000): LLM 관찰성 대시보드
- **Redis** (포트 6379): 캐싱 및 세션 관리

### 3단계: 서비스 상태 확인

```bash
cd infra
./scripts/health-check.sh
```

정상적으로 시작되면 다음과 같은 출력이 나타납니다:

```text
================================================================================
TransBot 인프라 헬스 체크
================================================================================

PostgreSQL: ✓ 정상 (포트 5432)
Langfuse: ✓ 정상 (포트 3000)
Redis: ✓ 정상 (포트 6379)

모든 서비스가 정상 동작 중입니다.
```

### 4단계: Langfuse 대시보드 접속

브라우저에서 `http://localhost:3000`에 접속합니다.

처음 접속 시 계정 생성 화면이 나타납니다.

## API 키 생성

Langfuse 대시보드에서 API 키를 생성하여 TransBot과 연동합니다.

### 1단계: Langfuse 계정 생성

1. `http://localhost:3000` 접속
2. **Sign Up** 클릭
3. 이메일, 이름, 비밀번호 입력
4. **Create Account** 클릭

### 2단계: 프로젝트 생성

1. 로그인 후 **New Project** 클릭
2. 프로젝트 이름 입력 (예: `TransBot`)
3. **Create** 클릭

### 3단계: API 키 발급

1. 왼쪽 사이드바에서 **Settings** 클릭
2. **API Keys** 탭 선택
3. **Create New Key** 클릭
4. 키 이름 입력 (예: `TransBot Development`)
5. **Create** 클릭

API 키가 생성되면 다음 두 개의 키가 표시됩니다:

- **Public Key** (pk-lf-xxx): 클라이언트에서 사용
- **Secret Key** (sk-lf-xxx): 서버에서 사용 (비밀 유지 필수)

> **경고**: Secret Key는 한 번만 표시됩니다. 반드시 복사하여 안전한 곳에 저장하세요.

### 4단계: API 키 복사

1. **Public Key** 복사 (클립보드 아이콘 클릭)
2. **Secret Key** 복사 (클립보드 아이콘 클릭)

## TransBot 환경 변수 설정

API 키를 TransBot의 `.env` 파일에 추가합니다.

### 1단계: .env 파일 열기

TransBot 프로젝트 루트의 `.env` 파일을 엽니다.

```bash
cd ..  # infra 디렉토리에서 프로젝트 루트로 이동
vim .env  # 또는 선호하는 텍스트 에디터 사용
```

### 2단계: Langfuse 환경 변수 추가

`.env` 파일 하단에 다음 내용을 추가합니다:

```bash
# ============================================================================
# Langfuse 설정 (LLM 관찰성)
# ============================================================================
#
# Langfuse를 사용하여 LLM 사용 내역을 추적하고 비용 분석, 품질 모니터링을 수행할 수 있습니다.
# 자체 호스팅 Langfuse 인스턴스를 사용하며, 설정하지 않으면 추적이 비활성화됩니다.

# Langfuse Public Key
# Langfuse 대시보드의 Settings > API Keys에서 발급받은 Public Key를 입력하세요.
LANGFUSE_PUBLIC_KEY=pk-lf-xxx  # 복사한 Public Key로 교체

# Langfuse Secret Key
# Langfuse 대시보드의 Settings > API Keys에서 발급받은 Secret Key를 입력하세요.
LANGFUSE_SECRET_KEY=sk-lf-xxx  # 복사한 Secret Key로 교체

# Langfuse Host URL
# 자체 호스팅 Langfuse 인스턴스의 URL을 입력하세요.
# 로컬 개발: http://localhost:3000
LANGFUSE_HOST=http://localhost:3000
```

### 3단계: 환경 변수 예시

올바르게 설정된 예시:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-018b7508-6b0a-414a-a476-4d9762e6edfc
LANGFUSE_SECRET_KEY=sk-lf-882990c0-669b-487c-bd32-e3b4f7fa63d7
LANGFUSE_HOST=http://localhost:3000
```

> **주의**: 실제 API 키는 위의 예시와 다른 형식이며, Langfuse 대시보드에서 발급받은 키를 사용해야 합니다.

## 연결 확인

TransBot과 Langfuse가 정상적으로 연결되었는지 확인합니다.

### 1단계: TransBot 실행

```bash
# 프로젝트 루트에서 실행
streamlit run app.py
```

### 2단계: 번역 수행

1. 브라우저에서 `http://localhost:8501` 접속
2. AI 모델 선택 (예: GPT-4o Mini)
3. 번역 방향 선택 (예: 영어 → 한국어)
4. 원문 텍스트 입력 (예: `Hello, how are you?`)
5. **번역하기** 버튼 클릭

### 3단계: Langfuse 대시보드 확인

1. 브라우저에서 `http://localhost:3000` 접속
2. 왼쪽 사이드바에서 **Traces** 클릭
3. 방금 수행한 번역 요청이 표시되는지 확인

정상적으로 연동되면 다음 정보를 확인할 수 있습니다:

- **Name**: `translation`
- **Input**: 원문 텍스트 및 번역 방향
- **Output**: 번역된 텍스트
- **Metadata**: 사용된 AI 모델, 응답 시간
- **Usage**: 입력/출력 토큰 수

### 4단계: 에러 확인

Langfuse 연결에 문제가 있는 경우, 터미널에 다음과 같은 메시지가 표시됩니다:

```text
⚠️ Langfuse 초기화 실패 (추적 비활성화): <에러 메시지>
```

또는

```text
⚠️ Langfuse 추적 실패: <에러 타입>: <에러 메시지>
```

> **참고**: Langfuse 에러가 발생해도 번역 기능은 정상 동작합니다. Langfuse는 선택적 기능이며, 실패 시 자동으로 비활성화됩니다.

## 트러블슈팅

### 문제 1: Langfuse 대시보드에 접속할 수 없음

**증상**: `http://localhost:3000`에 접속 시 "연결할 수 없음" 오류

**원인 및 해결 방법**:

1. **Langfuse 컨테이너 상태 확인**:

   ```bash
   docker ps | grep langfuse
   ```

   컨테이너가 실행 중이 아니면:

   ```bash
   cd infra
   ./scripts/start.sh
   ```

2. **Langfuse 로그 확인**:

   ```bash
   docker logs transbot-langfuse --tail 50
   ```

3. **포트 충돌 확인**:

   다른 서비스가 포트 3000을 사용 중인 경우 `.env.infra`에서 포트 변경:

   ```bash
   LANGFUSE_PORT=3001
   ```

### 문제 2: TransBot에서 Langfuse 추적이 동작하지 않음

**증상**: 번역은 되지만 Langfuse 대시보드에 추적 데이터가 나타나지 않음

**원인 및 해결 방법**:

1. **환경 변수 확인**:

   ```bash
   python3 -c "
   from config import Config
   c = Config.load()
   print(f'LANGFUSE_PUBLIC_KEY: {c.LANGFUSE_PUBLIC_KEY}')
   print(f'LANGFUSE_SECRET_KEY: {c.LANGFUSE_SECRET_KEY}')
   print(f'LANGFUSE_HOST: {c.LANGFUSE_HOST}')
   print(f'langfuse_enabled: {c.langfuse_enabled}')
   "
   ```

   `langfuse_enabled`가 `True`인지 확인하세요.

2. **API 키 확인**:

   Langfuse 대시보드의 **Settings > API Keys**에서 API 키가 일치하는지 확인하세요.

3. **Langfuse 서버 확인**:

   ```bash
   curl http://localhost:3000/api/health
   ```

   정상적으로 응답하는지 확인하세요.

4. **TransBot 재시작**:

   환경 변수를 변경한 후에는 TransBot을 재시작해야 합니다.

   ```bash
   # Ctrl+C로 TransBot 중지
   streamlit run app.py
   ```

### 문제 3: 잘못된 API 키 에러

**증상**: 콘솔에 `401 Unauthorized` 에러 표시

**원인**: Public Key 또는 Secret Key가 잘못됨

**해결 방법**:

1. Langfuse 대시보드에서 새 API 키 생성
2. `.env` 파일에 새 키 입력
3. TransBot 재시작

### 문제 4: PostgreSQL 연결 실패

**증상**: Langfuse 컨테이너가 시작되지 않고 "database connection failed" 에러

**원인**: PostgreSQL이 준비되지 않음

**해결 방법**:

1. **PostgreSQL 상태 확인**:

   ```bash
   docker ps | grep postgres
   ```

2. **PostgreSQL 헬스 체크**:

   ```bash
   docker exec transbot-postgres pg_isready -U transbot_user
   ```

3. **서비스 재시작**:

   ```bash
   cd infra
   ./scripts/stop.sh
   ./scripts/start.sh
   ```

## Langfuse 비활성화

Langfuse를 사용하지 않으려면 환경 변수를 주석 처리하거나 삭제하면 됩니다.

### 방법 1: 환경 변수 주석 처리

`.env` 파일에서 Langfuse 환경 변수를 주석 처리:

```bash
# LANGFUSE_PUBLIC_KEY=pk-lf-xxx
# LANGFUSE_SECRET_KEY=sk-lf-xxx
# LANGFUSE_HOST=http://localhost:3000
```

### 방법 2: 환경 변수 삭제

`.env` 파일에서 Langfuse 관련 섹션을 완전히 삭제합니다.

### 확인

TransBot을 재시작하면 Langfuse 추적이 비활성화되고, 번역 기능은 정상 동작합니다.

## 프로덕션 배포 고려사항

로컬 개발이 아닌 프로덕션 환경에 배포할 때는 다음 사항을 고려하세요.

### 1. HTTPS 사용

프로덕션에서는 HTTPS를 사용하여 API 키를 안전하게 전송하세요.

```bash
LANGFUSE_HOST=https://langfuse.yourdomain.com
```

### 2. 방화벽 설정

Langfuse 포트(3000)를 외부에서 접근할 수 있도록 방화벽 설정을 조정하세요.

### 3. 데이터베이스 백업

PostgreSQL 데이터베이스를 주기적으로 백업하세요.

```bash
cd infra
docker-compose exec postgres pg_dump -U transbot_user transbot > backup.sql
```

### 4. 환경 변수 보안

프로덕션 환경에서는 환경 변수를 암호화하거나 시크릿 관리 도구(예: AWS Secrets Manager)를 사용하세요.

## 다음 단계

- [Langfuse 사용 가이드](usage.md) - Langfuse 대시보드 사용법 및 추적 데이터 확인
- [Langfuse 에러 핸들링 가이드](error-handling.md) - 에러 시나리오 및 문제 해결 방법
- [인프라 가이드](../../../infra/README.md) - Docker Compose 기반 인프라 사용법

## 관련 문서

- [Langfuse 공식 문서](https://langfuse.com/docs)
- [Langfuse Self-Hosting 가이드](https://langfuse.com/docs/deployment/self-host)
- [Langfuse Python SDK](https://github.com/langfuse/langfuse-python)

---

**작성일**: 2026-02-04
**최종 수정일**: 2026-02-04
**작성자**: TransBot Development Team
