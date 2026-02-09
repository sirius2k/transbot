# TransBot 실행 계획 (Execution Plan)

이 폴더는 PRD에 명시된 기능들의 실행 계획을 담고 있습니다.

## Phase 1.5 완료된 기능 목록

| FEATURE | 기능명 | 상태 | 분류 |
|---------|--------|------|------|
| [FEATURE-001](FEATURE-001.md) | 영어 ↔ 한국어 양방향 번역 | ✅ 완료 | BE + FE |
| [FEATURE-002](FEATURE-002.md) | 자동 언어 감지 | ✅ 완료 | BE + FE |
| [FEATURE-003](FEATURE-003.md) | 다양한 AI 모델 선택 | ✅ 완료 | BE + FE |
| [FEATURE-004](FEATURE-004.md) | 글자수/토큰수 실시간 표시 | ✅ 완료 | BE + FE |
| [FEATURE-005](FEATURE-005.md) | Markdown 포맷 지원 및 보존 | ✅ 완료 | BE + FE |
| [FEATURE-006](FEATURE-006.md) | 번역 결과 듀얼 복사 버튼 | ✅ 완료 | FE |
| [FEATURE-007](FEATURE-007.md) | 사이드바 UI (설정 섹션) | ✅ 완료 | FE |

## Phase 2 계획 중 기능 목록

| FEATURE                       | 기능명                             | 상태        | 분류     | 우선순위 |
| ----------------------------- | ---------------------------------- | ----------- | -------- | -------- |
| [FEATURE-009](FEATURE-009.md) | 환경 변수 기반 설정 관리 시스템    | 🔲 계획 중  | BE + FE  | P1       |
| [FEATURE-008](FEATURE-008.md) | Azure OpenAI Service 지원          | 🔲 계획 중  | BE + FE  | P1       |

## 기능 간 의존성 다이어그램

```text
FEATURE-001 (핵심 번역)
    │
    ├──→ FEATURE-002 (자동 언어 감지)
    │
    ├──→ FEATURE-003 (모델 선택)
    │       │
    │       └──→ FEATURE-009 (설정 관리) ← config.py 기반 인프라
    │               │
    │               └──→ FEATURE-008 (Azure OpenAI 지원) ← Provider 선택 확장
    │
    ├──→ FEATURE-004 (글자수/토큰 표시)
    │
    ├──→ FEATURE-005 (Markdown 지원)
    │         │
    │         └──→ FEATURE-006 (복사 버튼)
    │
    └──→ FEATURE-007 (사이드바 UI)
              │
              ├── API 키 입력
              ├── 모델 선택 (FEATURE-003)
              ├── 설정 관리 (FEATURE-009)
              ├── Provider 선택 (FEATURE-008)
              └── 번역 설정 (FEATURE-002)
```

## 작업 분류

### 백엔드 (BE)

- OpenAI API 연동
- 번역 프롬프트 설계
- 언어 감지 알고리즘
- 글자수/토큰수 계산
- Markdown 보존 로직

### 프론트엔드 (FE)

- Streamlit UI 컴포넌트
- 사이드바 레이아웃
- 복사 버튼 기능
- 실시간 카운터 표시
- 결과 렌더링

## 총 작업(Task) 수

| FEATURE     | Task 수 |
| ----------- | ------- |
| FEATURE-001 | 5       |
| FEATURE-002 | 4       |
| FEATURE-003 | 4       |
| FEATURE-004 | 4       |
| FEATURE-005 | 4       |
| FEATURE-006 | 5       |
| FEATURE-007 | 6       |
| FEATURE-009 | 8       |
| FEATURE-008 | 8       |
| **총합**    | **48**  |

## 문서 유형

### FEATURE-XXX.md

- 2시간 이상 소요되는 주요 기능
- 여러 파일 수정 필요
- Task 분해 필요
- Simple/Standard/Complex 템플릿 사용

### MINOR-XXX.md

- 1-2시간 이내 완료 가능한 간단한 개선사항 (Quick Wins)
- 단일 파일 수정
- Task 분해 불필요
- Quick Wins 초경량 템플릿 사용 (3개 섹션만)

## 실행 계획 생성 방법

```bash
# 자동 판단 (PRD 위치 및 소요 시간 기반)
execution-plan MINOR-006  # MINOR-006 자동 생성 (마이너 개선사항 테이블에 있는 경우)
execution-plan FEATURE-023  # FEATURE-023 자동 생성 (주요 기능 테이블에 있는 경우)
```

**자동 판단 로직**:

1. PRD.md에서 입력 번호 검색
2. "마이너 개선사항 (Quick Wins)" 테이블 → MINOR-XXX.md
3. "주요 기능 (FEATURE)" 테이블 → FEATURE-XXX.md
4. 소요 시간 기반: 1-2h → Quick Wins, 2-3h → Simple, 4-10h → Standard, 10h+ → Complex

## 파일 구조

```text
feature-execution-plan/
├── README.md           # 이 파일 (전체 요약)
├── FEATURE-001.md      # 영어 ↔ 한국어 양방향 번역
├── FEATURE-002.md      # 자동 언어 감지
├── FEATURE-003.md      # 다양한 AI 모델 선택
├── FEATURE-004.md      # 글자수/토큰수 실시간 표시
├── FEATURE-005.md      # Markdown 포맷 지원 및 보존
├── FEATURE-006.md      # 번역 결과 듀얼 복사 버튼
├── FEATURE-007.md      # 사이드바 UI (설정 섹션)
├── FEATURE-008.md      # Azure OpenAI Service 지원
├── FEATURE-009.md      # 환경 변수 기반 설정 관리 시스템
├── MINOR-001.md        # 지우기 버튼 (Quick Win)
├── MINOR-002.md        # 콘솔 로깅 간소화 (Quick Win)
└── ...
```

---

**생성일**: 2026년 1월 25일
**최종 수정일**: 2026년 1월 29일
