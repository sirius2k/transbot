# TransBot Infrastructure

TransBot의 로컬 개발 환경을 위한 Docker 기반 인프라 설정입니다.

## 📋 목차

- [서비스 구성](#서비스-구성)
- [빠른 시작](#빠른-시작)
- [상세 사용법](#상세-사용법)
- [서비스별 설정](#서비스별-설정)
- [트러블슈팅](#트러블슈팅)

## 서비스 구성

### 포함된 서비스

| 서비스 | 버전 | 이미지 | 포트 | 용도 |
| -------- | -------- | -------- | ------ | ------ |
| **PostgreSQL** | 15 | `postgres:15-alpine` | 5432 | 데이터베이스 (번역 히스토리, 사용자 데이터, Langfuse 메타데이터) |
| **Langfuse** | 2 (Stable) | `langfuse/langfuse:2` | 3000 | LLM 관찰성 플랫폼 (프롬프트 추적, 비용 분석, 품질 모니터링) |
| **Redis** | 7 | `redis:7-alpine` | 6379 | 캐싱 및 세션 관리 |

> **참고**: Langfuse v3는 ClickHouse를 추가로 요구하지만, 현재는 안정성을 위해 v2를 사용합니다. v3 업그레이드는 향후 고려될 예정입니다.

### 디렉토리 구조

```text
infra/
├── docker-compose.yml          # 통합 Docker Compose 설정
├── .env.infra.example          # 환경 변수 템플릿
├── .env.infra                  # 실제 환경 변수 (gitignore)
├── README.md                   # 본 문서
│
├── services/                   # 서비스별 설정
│   ├── langfuse/
│   ├── postgres/
│   │   └── init.sql            # DB 초기화 스크립트
│   └── redis/
│
├── scripts/                    # 관리 스크립트
│   ├── start.sh                # 서비스 시작
│   ├── stop.sh                 # 서비스 종료
│   ├── restart.sh              # 재시작
│   ├── logs.sh                 # 로그 확인
│   ├── reset.sh                # 데이터 초기화
│   └── health-check.sh         # 헬스 체크
│
└── volumes/                    # 데이터 영속화 (gitignore)
    ├── postgres/
    ├── langfuse/
    └── redis/
```

## 빠른 시작

### 1. 환경 변수 설정

```bash
cd infra
cp .env.infra.example .env.infra
```

`.env.infra` 파일을 열어 비밀번호를 설정하세요:

```bash
# 최소 변경 필요 항목
POSTGRES_PASSWORD=your_secure_password
LANGFUSE_SECRET=random-string-at-least-32-characters
LANGFUSE_SALT=another-random-string
REDIS_PASSWORD=your_redis_password
```

### 2. 서비스 시작

```bash
./scripts/start.sh
```

### 3. Langfuse 설정

1. 브라우저에서 `http://localhost:3000` 접속
2. 계정 생성 및 로그인
3. 새 프로젝트 생성
4. API 키 복사: Settings → API Keys
5. TransBot `.env` 파일에 추가:

```bash
# TransBot 루트의 .env 파일에 추가
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=http://localhost:3000
```

### 4. TransBot 실행

```bash
cd ..  # 프로젝트 루트로 이동
streamlit run app.py
```

## 상세 사용법

### 전체 서비스 관리

```bash
# 모든 서비스 시작
./scripts/start.sh

# 모든 서비스 종료
./scripts/stop.sh

# 로그 확인
./scripts/logs.sh          # 전체 로그
./scripts/logs.sh -f       # 실시간 로그 (tail -f)

# 헬스 체크
./scripts/health-check.sh

# 데이터 초기화 (⚠️ 모든 데이터 삭제)
./scripts/reset.sh
```

### 개별 서비스 관리

```bash
# 특정 서비스만 시작
./scripts/start.sh postgres
./scripts/start.sh langfuse
./scripts/start.sh redis

# 특정 서비스만 종료
./scripts/stop.sh postgres

# 특정 서비스 로그 확인
./scripts/logs.sh postgres
./scripts/logs.sh langfuse -f
```

### Docker Compose 직접 사용

```bash
# 서비스 상태 확인
docker-compose ps

# 특정 서비스 재시작
docker-compose restart langfuse

# 서비스 스케일링 (Redis 3개 인스턴스)
docker-compose up -d --scale redis=3

# 컨테이너 접속
docker-compose exec postgres psql -U transbot_user -d transbot
docker-compose exec redis redis-cli -a your_redis_password
```

## 서비스별 설정

### PostgreSQL

#### 버전 정보

현재 **PostgreSQL 15 (Alpine)** 를 사용합니다.

- **이미지**: `postgres:15-alpine`
- **용도**:
  - TransBot 애플리케이션 데이터 (번역 히스토리, 사용자 정보 등)
  - Langfuse 메타데이터 및 이벤트 저장
- **선택 이유**: Alpine 이미지는 경량화되어 있어 로컬 개발에 적합하며, PostgreSQL 15는 안정적인 LTS 버전입니다.

#### 데이터베이스 접속

```bash
# Docker 컨테이너 내부에서
docker-compose exec postgres psql -U transbot_user -d transbot

# 호스트에서 직접 (psql 설치 필요)
PGPASSWORD=your_password psql -h localhost -U transbot_user -d transbot
```

#### 스키마 확인

```sql
-- 테이블 목록
\dt transbot.*

-- 스키마 정보
\dn+
```

#### 백업 및 복원

```bash
# 백업
docker-compose exec postgres pg_dump -U transbot_user transbot > backup.sql

# 복원
cat backup.sql | docker-compose exec -T postgres psql -U transbot_user -d transbot
```

### Langfuse

#### 버전 정보

현재 **Langfuse v2 (Stable)** 를 사용합니다.

- **이미지**: `langfuse/langfuse:2`
- **데이터베이스**: PostgreSQL 15 (메타데이터 및 이벤트 저장)
- **v3와의 차이점**: v3는 ClickHouse를 추가로 요구하지만, v2는 PostgreSQL만으로 동작하여 설정이 간단하고 안정적입니다.

#### 주요 기능

- **프롬프트 추적**: OpenAI API 호출 자동 로깅
- **비용 분석**: 토큰 사용량 및 비용 대시보드
- **성능 모니터링**: 응답 시간, 에러율 추적
- **프롬프트 버전 관리**: 프롬프트 변경 이력 관리
- **세션 추적**: 사용자 세션별 LLM 호출 그룹핑

#### TransBot 통합

```python
# app.py에서 Langfuse 초기화 (향후 구현)
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# 번역 요청 추적
trace = langfuse.trace(name="translation")
```

### Redis

#### 버전 정보

현재 **Redis 7 (Alpine)** 를 사용합니다.

- **이미지**: `redis:7-alpine`
- **용도**: 캐싱, 세션 관리, 임시 데이터 저장
- **영속성**: AOF (Append Only File) 모드로 데이터 영속성 보장
- **선택 이유**: Redis 7은 최신 안정 버전이며, Alpine 이미지로 경량화되어 있습니다.

#### Redis CLI 접속

```bash
docker-compose exec redis redis-cli -a your_redis_password
```

#### 기본 명령어

```redis
# 키 목록 확인
KEYS *

# 특정 키 조회
GET my_key

# 캐시 플러시
FLUSHALL
```

## 트러블슈팅

### 포트 충돌

다른 서비스가 같은 포트를 사용 중인 경우 `.env.infra`에서 포트 변경:

```bash
POSTGRES_PORT=5433  # 기본 5432 대신
LANGFUSE_PORT=3001  # 기본 3000 대신
REDIS_PORT=6380     # 기본 6379 대신
```

### 서비스가 시작되지 않음

```bash
# 로그 확인
./scripts/logs.sh

# 컨테이너 상태 확인
docker-compose ps

# 강제 재시작
docker-compose down
docker-compose up -d
```

### 데이터베이스 연결 실패

```bash
# PostgreSQL 헬스 체크
docker-compose exec postgres pg_isready -U transbot_user

# 연결 테스트
docker-compose exec postgres psql -U transbot_user -d transbot -c "SELECT 1;"
```

### Langfuse가 시작되지 않음

Langfuse는 PostgreSQL에 의존하므로 PostgreSQL이 먼저 준비되어야 합니다.

```bash
# PostgreSQL이 준비될 때까지 대기
./scripts/health-check.sh

# Langfuse 로그 확인
./scripts/logs.sh langfuse -f
```

### 볼륨 권한 문제

```bash
# 볼륨 삭제 후 재생성
docker-compose down -v
./scripts/start.sh
```

## 프로덕션 배포

현재 설정은 로컬 개발 전용입니다. 프로덕션 환경에서는:

1. **보안 강화**
   - 강력한 비밀번호 사용
   - 환경 변수 암호화
   - 네트워크 분리

2. **데이터 백업**
   - 자동 백업 스크립트 설정
   - 원격 저장소에 백업 보관

3. **모니터링**
   - Prometheus + Grafana 추가
   - 알림 설정

4. **스케일링**
   - PostgreSQL 복제본 구성
   - Redis Cluster 구성
   - 로드 밸런서 추가

## 버전 업그레이드

### Langfuse v2 → v3 업그레이드 (향후 계획)

Langfuse v3로 업그레이드하려면 ClickHouse를 추가로 설치해야 합니다.

#### v3의 주요 변경사항

- **ClickHouse 요구**: 분석 데이터베이스로 ClickHouse 추가
- **성능 향상**: 대용량 이벤트 처리 성능 개선
- **고급 분석**: 더 복잡한 쿼리 및 대시보드 지원

#### 업그레이드 준비

1. `docker-compose.yml`에서 ClickHouse 주석 해제
2. `.env.infra`에 ClickHouse 환경 변수 설정
3. Langfuse 이미지를 `langfuse/langfuse:3`으로 변경
4. 데이터 마이그레이션 실행

> **참고**: 현재는 안정성과 단순성을 위해 v2를 사용합니다. v3 업그레이드는 프로젝트가 성숙해진 후 고려될 예정입니다.

## 참고 자료

### 공식 문서

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [PostgreSQL 15 문서](https://www.postgresql.org/docs/15/)
- [Langfuse v2 문서](https://langfuse.com/docs)
- [Langfuse v3 업그레이드 가이드](https://langfuse.com/docs/deployment/self-host#langfuse-v3)
- [Redis 7 문서](https://redis.io/docs/about/redis-7-0/)

### Docker Hub

- [postgres:15-alpine](https://hub.docker.com/_/postgres)
- [langfuse/langfuse:2](https://hub.docker.com/r/langfuse/langfuse)
- [redis:7-alpine](https://hub.docker.com/_/redis)
- [clickhouse/clickhouse-server:24-alpine](https://hub.docker.com/r/clickhouse/clickhouse-server) (v3 전용)

---

**작성일**: 2026-02-03
**최종 수정일**: 2026-02-04
**작성자**: TransBot Development Team
