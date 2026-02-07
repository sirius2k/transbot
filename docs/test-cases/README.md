# 통합 테스트 케이스 (Integration Test Cases)

이 디렉토리는 TransBot의 브라우저 기반 통합 테스트 케이스 문서를 관리합니다.

## 개요

통합 테스트는 TransBot의 실제 사용자 시나리오를 검증하기 위한 E2E(End-to-End) 테스트입니다. 각 테스트 케이스는 Given/When/Then 형식으로 작성되며, 향후 Playwright를 사용한 자동화 테스트 구현의 기반이 됩니다.

## 테스트 케이스 카테고리

| TC 번호 | 기능명 | 설명 | 우선순위 | 상태 |
| ------- | ------ | ---- | -------- | ---- |
| TC-001-page-rendering | 페이지 렌더링 | 앱 기본 동작 확인 (Smoke Test) | P0 | 🔲 예정 |
| TC-002-translation-e2e | 번역 E2E 플로우 | 전체 번역 프로세스 검증 | P0 | 🔲 예정 |
| TC-003-text-analysis | 텍스트 분석 및 통계 | 언어 감지 및 카운팅 기능 검증 | P1 | 🔲 예정 |
| TC-004-ui-interactions | UI 인터랙션 | 사용자 인터페이스 동작 검증 | P1 | 🔲 예정 |
| TC-005-settings-config | 설정 관리 | 사이드바 설정 및 옵션 검증 | P2 | 🔲 예정 |
| TC-006-error-handling | 에러 핸들링 | 예외 상황 대응 검증 | P1 | 🔲 예정 |

## 문서 구조

각 테스트 케이스 문서는 다음 구조를 따릅니다:

```markdown
# TC-XXX: [기능명]

## 개요
- 테스트 목적
- 테스트 범위
- 관련 FEATURE

## 전제 조건
- 실행 전 필요한 설정

## 테스트 시나리오
- Given/When/Then 형식

## 테스트 데이터
- 입력 데이터
- 예상 결과

## UI 선택자 (Playwright 참고)
- 자동화 테스트를 위한 선택자

## 실행 방법
- 수동 테스트
- 자동 테스트 (향후)

## 주의사항
## 변경 이력
```

## 테스트 케이스 생성 방법

### 스킬 사용 (권장)

```bash
/generate-test-case "테스트할 기능명"
```

스킬이 대화형으로 필요한 정보를 수집하고 문서를 자동 생성합니다.

### 수동 작성

1. `TC-XXX-feature-name.md` 형식으로 파일 생성
2. 위 문서 구조를 따라 작성
3. Markdownlint 규칙 준수

## 우선순위 정의

| 우선순위 | 의미 | 설명 |
| -------- | ---- | ---- |
| **P0** | Critical | 서비스 핵심 기능, 반드시 통과해야 함 |
| **P1** | High | 주요 기능, 배포 전 확인 필수 |
| **P2** | Medium | 일반 기능, 정기 테스트 |
| **P3** | Low | 부가 기능, 선택적 테스트 |

## 테스트 실행 방법

### 수동 테스트

1. Streamlit 앱 실행: `streamlit run app.py`
2. 각 TC 문서의 "실행 방법" 섹션 참고
3. 시나리오별로 수동 검증

### 자동 테스트 (향후)

Playwright 기반 자동화 테스트 구현 예정:

```bash
# 전체 테스트 실행
pytest tests/integration/

# 특정 TC 실행
pytest tests/integration/test_TC_001.py

# 우선순위별 실행
pytest tests/integration/ -m P0
```

## 테스트 상태

- 🔲 예정: 테스트 케이스 문서 작성 예정
- ✅ 완료: 문서 작성 및 검증 완료
- ⏳ 진행중: 작성 중
- ⏸️ 보류: 일시적으로 보류

## 관련 문서

- [테스트 가이드](../guides/quality/testing-guide.md): 단위 테스트 가이드
- [PRD](../product/PRD.md): 제품 요구사항 정의
- [FEATURE 실행 계획](../feature-execution-plan/): 기능별 구현 계획

## 기여 방법

1. 새로운 테스트 케이스 제안: GitHub Issue 생성
2. 기존 TC 개선: PR 제출
3. 자동화 테스트 구현: Playwright 코드 작성

---

**최종 업데이트**: 2026-02-07
**관리자**: TransBot QA Team
