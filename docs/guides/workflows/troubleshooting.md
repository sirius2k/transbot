# 문제 해결 가이드 (Troubleshooting)

TransBot 개발 및 사용 중 발생할 수 있는 일반적인 문제와 해결 방법을 안내합니다.

## 목차

- [API 키 관련 문제](#api-키-관련-문제)
- [Langfuse 연결 문제](#langfuse-연결-문제)
- [테스트 실패 시](#테스트-실패-시)
- [가상환경 문제](#가상환경-문제)
- [자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)

---

## API 키 관련 문제

### 증상 1: OPENAI_API_KEY not found

**원인**: `.env` 파일이 없거나 환경 변수 미설정

**해결책**:

1. `.env` 파일이 존재하는지 확인

   ```bash
   ls -la .env
   ```

2. `.env.example`을 복사하여 `.env` 생성

   ```bash
   cp .env.example .env
   ```

3. `.env` 파일에 유효한 API 키 설정

   ```bash
   OPENAI_API_KEY=sk-...
   ```

4. Streamlit 재실행

   ```bash
   streamlit run app.py
   ```

**관련 가이드**: [환경 설정 가이드](../infrastructure/environment-setup.md)

---

### 증상 2: API 키가 있는데도 인증 실패

**원인**: API 키 형식 오류 또는 만료

**해결책**:

1. API 키 형식 확인
   - OpenAI: `sk-...` 형식
   - Azure: 32자 문자열
2. OpenAI 대시보드에서 키 유효성 확인
3. 필요 시 새 키 발급
4. `.env` 파일 업데이트 후 재실행

---

## Langfuse 연결 문제

### 증상 1: Langfuse 대시보드에 추적 데이터가 표시되지 않음

**원인**: Langfuse 서버 미실행 또는 환경 변수 오류

**해결책**:

1. Langfuse 인프라 상태 확인

   ```bash
   cd infra && ./scripts/health-check.sh
   ```

2. 출력 예시:

   ```text
   ✅ Langfuse: Running
   ✅ PostgreSQL: Running
   ✅ Redis: Running
   ```

3. 서비스가 실행되지 않은 경우:

   ```bash
   ./scripts/start.sh
   ```

4. `.env` 파일의 Langfuse 환경 변수 확인

   ```bash
   cat .env | grep LANGFUSE
   ```

5. 콘솔에서 Langfuse 에러 로그 확인
   - "Langfuse 초기화 실패" → API 키 오류
   - "Langfuse 서버 연결 실패" → 서버 다운

**관련 가이드**: [Langfuse 에러 핸들링](../infrastructure/langfuse/error-handling.md)

---

### 증상 2: Langfuse 서비스가 시작되지 않음

**원인**: 포트 충돌 또는 Docker 문제

**해결책**:

1. 포트 3000 사용 중인 프로세스 확인

   ```bash
   lsof -i :3000
   ```

2. 포트 사용 중이면 프로세스 종료 또는 포트 변경

3. Docker 상태 확인

   ```bash
   docker ps
   ```

4. 필요 시 Docker 재시작

   ```bash
   docker restart $(docker ps -q)
   ```

5. Langfuse 인프라 재시작

   ```bash
   cd infra && ./scripts/stop.sh && ./scripts/start.sh
   ```

---

## 테스트 실패 시

### 증상 1: pytest 실행 시 테스트 실패

**원인**: 환경 변수 미설정, 의존성 오류, 코드 버그

**해결책**:

1. 테스트 가이드 참고
   - [테스트 가이드](../quality/testing-guide.md)

2. 환경 변수 설정 확인 (특히 API 키)

   ```bash
   source venv/bin/activate
   export OPENAI_API_KEY=sk-...
   ```

3. 의존성 재설치

   ```bash
   pip install -r requirements-dev.txt
   ```

4. 특정 테스트만 실행 (디버깅)

   ```bash
   pytest tests/test_utils.py::test_detect_language -v
   ```

5. 가상환경 재생성 (최후 수단)

   ```bash
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

---

### 증상 2: 커버리지 80% 미달

**원인**: 테스트 케이스 부족, 엣지 케이스 미포함

**해결책**:

1. 커버리지 리포트 확인

   ```bash
   pytest --cov=utils --cov=app --cov=components --cov-report=html
   open htmlcov/index.html
   ```

2. 미커버된 라인 확인 (빨간색으로 표시)

3. 엣지 케이스 테스트 추가
   - 빈 문자열
   - 매우 긴 문자열
   - 특수 문자
   - None 값

4. test-runner 에이전트 활용 (자동 테스트 작성)

   ```text
   Claude에게 "test-runner 에이전트를 사용해서 테스트 커버리지를 90%까지 올려줘"
   ```

**관련 가이드**: [테스트 가이드](../quality/testing-guide.md)

---

## 가상환경 문제

### 증상: 가상환경 활성화 실패

**원인**: 가상환경 경로 오류, Python 버전 불일치

**해결책**:

1. 가상환경 경로 확인

   ```bash
   ls -la venv/
   ```

2. 가상환경이 없으면 생성

   ```bash
   python3 -m venv venv
   ```

3. 활성화 (macOS/Linux)

   ```bash
   source venv/bin/activate
   ```

4. 활성화 (Windows)

   ```bash
   venv\Scripts\activate.bat
   ```

5. 프롬프트에 `(venv)` 표시 확인

---

## 자주 묻는 질문 (FAQ)

### Q1: test-runner 에이전트는 언제 사용하나요?

**A**: Python 코드 변경 후 자동으로 실행되지만, 수동으로 실행할 수도 있습니다.

```text
Claude에게 "test-runner 에이전트를 사용해서 테스트를 실행해줘"
```

---

### Q2: docs-sync-guardian 에이전트는 어떻게 작동하나요?

**A**: 코드나 기능 변경 후 자동으로 README, PRD, CLAUDE.md를 동기화합니다. 수동 실행도 가능합니다.

```text
Claude에게 "docs-sync-guardian 에이전트를 사용해서 문서를 동기화해줘"
```

---

### Q3: FEATURE 문서의 "분석 수준"은 무엇인가요?

**A**: resolve-issue 스킬이 코드베이스를 얼마나 분석할지 결정하는 메타데이터입니다.

- **완료**: 아키텍처 + 코드 예시 포함 → 5분, 10k 토큰
- **부분**: 기본 요구사항 + 간단 예시 → 15분, 15k 토큰
- **없음**: Task 분해만 → 30분, 30k 토큰

---

### Q4: Quick Win과 FEATURE의 차이는?

**A**:

- **Quick Win**: 2시간 미만의 간단한 개선 (QW-01, QW-02 ...)
- **FEATURE**: 2시간 이상의 복잡한 기능 (FEATURE-001, FEATURE-002 ...)

---

### Q5: WORKLOG는 필수인가요?

**A**: 예, 2시간 이상의 FEATURE 개발 시 필수입니다. 시간 예측 정확도 향상에 필수적입니다.

**관련 가이드**: [작업 시간 추적](time-tracking.md)

---

## 추가 도움말

더 자세한 정보는 다음 가이드를 참고하세요:

- [개발 환경 설정](../infrastructure/environment-setup.md)
- [테스트 가이드](../quality/testing-guide.md)
- [Langfuse 에러 핸들링](../infrastructure/langfuse/error-handling.md)
- [작업 시간 추적](time-tracking.md)

---

**최종 수정일**: 2026-02-05

**작성자**: TransBot Development Team