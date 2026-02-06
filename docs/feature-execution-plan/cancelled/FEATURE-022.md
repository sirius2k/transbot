# FEATURE-022: Langfuse V3 업그레이드

## 개요

- **기능명**: Langfuse V3 업그레이드
- **상태**: ❌ 취소 (V2 유지)
- **분류**: 인프라
- **우선순위**: ~~P1 (높음)~~ → P3 (낮음)
- **복잡도**: ~~Simple (1-3h)~~ → Complex (8h+)
- **분석 수준**: 없음
- **진행률**: 0% (롤백 완료)
- **예상 시간**: 1-2시간
- **실제 소요**: 약 3시간 (조사 + 시도 + 롤백)
- **시작일**: 2026-02-05
- **취소일**: 2026-02-05

## ⚠️ 취소 사유

**V3 업그레이드가 취소되고 V2를 계속 사용하기로 결정했습니다.**

### 취소 이유

1. **ClickHouse 필수 요구사항**
   - Langfuse V3는 ClickHouse를 **필수**로 요구합니다 (선택 사항이 아님)
   - 공식 문서 확인 결과: "CLICKHOUSE_URL is not configured" 에러 발생
   - ClickHouse 없이는 V3 실행 불가능

2. **macOS 호환성 문제**
   - ClickHouse가 macOS Docker에서 권한 오류 발생 (`get_mempolicy: Operation not permitted`)
   - 로컬 개발 환경에서 안정적 실행 불가

3. **프로젝트 규모 불일치**
   - TransBot은 소규모 프로젝트 (개인 개발 도구)
   - ClickHouse는 대용량 이벤트 처리용 OLAP 데이터베이스 (초당 수백 건 처리)
   - PostgreSQL만으로 충분한 규모에 불필요한 인프라 추가

4. **복잡도 증가**
   - ClickHouse 추가로 인프라 관리 복잡도 증가
   - 운영 및 유지보수 부담 증가
   - 로컬 개발 환경 설정 어려움

### 결론

**Langfuse V2를 계속 사용하는 것이 TransBot의 현재 규모와 목적에 적합합니다.**

- V2는 안정적이고 검증된 버전
- PostgreSQL만으로 충분한 성능
- 간단한 인프라 관리
- macOS 로컬 개발 환경에서 안정적 동작

V3 업그레이드는 다음 조건이 충족될 때 재고려할 수 있습니다:
- TransBot이 대규모 트래픽을 처리해야 할 때
- 프로덕션 배포 환경이 Linux로 전환될 때
- ClickHouse 관리 리소스가 확보될 때

## 기능 설명 (참고용)

Langfuse를 V2에서 V3으로 업그레이드하여 최신 기능을 적용하고 기술 부채를 해소합니다.

### 목표

- Langfuse V2 → V3 업그레이드
- 최신 보안 패치 적용
- 성능 개선 및 새로운 기능 활용
- 운영 안정성 확보

### 배경

- 현재 Langfuse V2 사용 중 (`requirements.txt`: `langfuse>=2.0.0,<3.0.0`)
- V3는 ClickHouse 기반 분석 기능 추가 (선택적)
- docker-compose.yml에 ClickHouse 설정이 이미 준비되어 있음 (주석 처리)

## 작업(Task) 분해

### Task 1: Langfuse V3 브레이킹 체인지 조사

**분류**: 조사

**작업 내용**:

1. Langfuse V2 → V3 마이그레이션 가이드 확인
2. 브레이킹 체인지 목록 정리
3. Python SDK API 변경사항 확인
4. 환경 변수 변경사항 확인

**예상 파일**:

- 없음 (웹 검색 또는 공식 문서 확인)

**의존성**: 없음

### Task 2: Python 패키지 업데이트

**분류**: 인프라

**작업 내용**:

1. `requirements.txt` 수정: `langfuse>=2.0.0,<3.0.0` → `langfuse>=3.0.0,<4.0.0`
2. 가상환경에서 패키지 업데이트: `pip install -r requirements.txt`
3. 의존성 충돌 확인 및 해결

**예상 파일**:

- `requirements.txt`

**의존성**: Task 1

### Task 3: Docker 이미지 업데이트

**분류**: 인프라

**작업 내용**:

1. `infra/docker-compose.yml` 수정
   - Langfuse 이미지: `langfuse/langfuse:2` → `langfuse/langfuse:3`
   - ClickHouse 서비스 활성화 여부 결정 (선택적)
2. `.env.infra.example` 업데이트 (필요 시)
3. Docker 컨테이너 재시작: `infra/scripts/stop.sh && infra/scripts/start.sh`

**예상 파일**:

- `infra/docker-compose.yml`
- `infra/.env.infra.example` (필요 시)

**의존성**: Task 1

### Task 4: 코드 수정 (브레이킹 체인지 대응)

**분류**: 코드

**작업 내용**:

1. `components/observability.py` 수정 (필요 시)
   - API 변경사항 반영
   - 데코레이터 또는 컨텍스트 사용법 업데이트
2. `app.py` 수정 (필요 시)
3. 에러 핸들링 코드 확인

**예상 파일**:

- `components/observability.py`
- `app.py` (필요 시)

**의존성**: Task 1, Task 2

### Task 5: 테스트 실행 및 검증

**분류**: 테스트

**작업 내용**:

1. 단위 테스트 실행: `pytest`
2. Langfuse 대시보드 접속 확인: `http://localhost:3000`
3. 번역 수행 후 Langfuse에 추적 데이터 표시 확인
4. 에러 핸들링 테스트 (API 키 오류, 서버 다운 등)
5. 성능 및 안정성 확인

**예상 파일**:

- 없음 (테스트 실행)

**의존성**: Task 2, Task 3, Task 4

### Task 6: 문서 업데이트

**분류**: 문서

**작업 내용**:

1. `docs/guides/infrastructure/langfuse/setup.md` 업데이트
   - "Langfuse v2" → "Langfuse v3"로 변경
   - V3 특화 설정 추가 (ClickHouse 등)
2. `CLAUDE.md` 업데이트 (필요 시)
3. `README.md` 업데이트 (필요 시)
4. Troubleshooting 가이드 업데이트 (필요 시)

**예상 파일**:

- `docs/guides/infrastructure/langfuse/setup.md`
- `CLAUDE.md` (필요 시)
- `README.md` (필요 시)

**의존성**: Task 5

## 롤백 완료 기준

- [x] V3 업그레이드 시도 및 문제 발견
  - [x] ClickHouse 필수 요구사항 확인
  - [x] macOS 권한 문제 확인
- [x] Git 롤백 완료 (`git reset --hard HEAD~1`)
- [x] ClickHouse 컨테이너 제거
- [x] Langfuse V3 컨테이너 제거
- [x] ClickHouse volume 제거
- [x] Langfuse V2 패키지 재설치 (2.60.10)
- [x] FEATURE-022 문서 업데이트 (취소 사유 기록)
- [ ] 변경사항 커밋 및 푸시

## 참고 사항

### ClickHouse 사용 여부

Langfuse V3는 ClickHouse를 분석 데이터베이스로 사용할 수 있습니다 (선택적).

**ClickHouse를 사용하는 경우**:

- 대량의 트레이스 데이터 분석에 유리
- `docker-compose.yml`의 ClickHouse 서비스 주석 해제
- 환경 변수 추가 설정 필요

**ClickHouse를 사용하지 않는 경우**:

- PostgreSQL만으로 충분 (소규모 프로젝트)
- 추가 설정 불필요
- 기존 설정 그대로 사용

**권장**: TransBot은 소규모 프로젝트이므로 **ClickHouse 없이 PostgreSQL만 사용**하는 것을 권장합니다.

### 롤백 계획

업그레이드 중 문제 발생 시:

1. `requirements.txt`: `langfuse>=2.0.0,<3.0.0`로 복원
2. `docker-compose.yml`: `langfuse/langfuse:2`로 복원
3. Docker 재시작: `infra/scripts/stop.sh && infra/scripts/start.sh`
4. 가상환경 패키지 재설치: `pip install -r requirements.txt`

---

**작성일**: 2026-02-05
**작성자**: Claude Sonnet 4.5