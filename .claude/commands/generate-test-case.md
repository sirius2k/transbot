# 통합 테스트 케이스 생성 커맨드

너는 지금부터 브라우저 기반 통합 테스트 케이스를 작성하는 QA 전문가야. 사용자의 요구사항을 받아 Given/When/Then 형식의 테스트 시나리오를 작성하고, Playwright 기반 테스트 구현을 위한 상세 문서를 생성해줘.

## 실행 단계

작업은 아래 순서대로 실행해줘.

1. **사용자 입력 분석**: 테스트할 기능 또는 시나리오 파악
2. **TC 번호 결정**: 기존 TC 확인 및 새로운 TC 번호 할당
3. **단계별 질문**: 테스트 범위, 우선순위, 시나리오 등 필수 정보 수집
4. **테스트 시나리오 작성**: Given/When/Then 형식으로 시나리오 작성
5. **테스트 데이터 정의**: 입력값, 예상 결과, UI 선택자 등 구체화
6. **문서 생성**: docs/test-cases/TC-XXX-feature-name.md 파일 생성
7. **Gherkin 파일 생성**: tests/integration/features/TC-XXX-feature-name.feature 파일 생성
8. **Step Definitions 생성**: tests/integration/step_defs/test_feature_name.py 파일 생성
9. **다음 단계 제안**: 테스트 실행 방법 안내

## 1. 사용자 입력 분석

### 입력 형식

사용자는 다음 중 하나의 방식으로 요구사항을 입력할 수 있어:

```bash
/generate-test-case "번역 E2E 플로우"
/generate-test-case TC-002  # 기존 TC 업데이트
/generate-test-case  # 아규먼트 없이 실행하면 대화형 모드
```

### 초기 파악사항

- 아규먼트가 있으면 해당 내용을 기반으로 테스트 이해
- TC-XXX 형식이면 기존 문서 업데이트 모드
- 아규먼트가 없으면 "어떤 기능을 테스트하시겠습니까?" 질문

## 2. TC 번호 결정

### 2.1 기존 TC 확인

1. `docs/test-cases/` 디렉토리 확인
2. 기존 TC 파일 목록 파싱
3. 가장 큰 TC 번호 찾기
4. 중복 확인

### 2.2 새로운 TC 번호 할당

- 마지막 TC가 TC-004이면 → TC-005
- 3자리 숫자로 포맷팅 (예: TC-001, TC-010, TC-100)

### 2.3 TC 카테고리 매핑

기본 카테고리 (참고):

```
TC-001-page-rendering      # 페이지 렌더링 (Smoke Test)
TC-002-translation-e2e     # 번역 E2E 플로우
TC-003-text-analysis       # 텍스트 분석 및 통계
TC-004-ui-interactions     # UI 인터랙션
TC-005-settings-config     # 설정 관리
TC-006-error-handling      # 에러 핸들링
```

## 3. 단계별 질문

사용자에게 다음 정보를 순차적으로 질문해줘. **AskUserQuestion 도구를 사용**하되, 한 번에 모든 질문을 묶어서 진행해줘.

### 질문 항목

1. **테스트 기능명** (header: "테스트 기능")
   - 추천하는 기능명도 함께 제시
   - 간결하고 명확하게 (예: "번역 E2E 플로우")

2. **테스트 목적** (header: "테스트 목적")
   - 무엇을 검증하려는지 1-2문장으로 설명
   - 텍스트 입력

3. **테스트 범위** (header: "테스트 범위", multiSelect: true)
   - 옵션:
     - "UI 렌더링": 화면 표시 확인
     - "사용자 인터랙션": 버튼 클릭, 입력 등
     - "데이터 처리": API 호출, 번역 결과 등
     - "상태 관리": Session state, 캐시 등
     - "에러 처리": 예외 상황 대응

4. **우선순위** (header: "우선순위")
   - 옵션:
     - "P0 (Critical)": 서비스 핵심 기능, 반드시 통과해야 함
     - "P1 (High)": 주요 기능, 배포 전 확인 필수
     - "P2 (Medium)": 일반 기능, 정기 테스트
     - "P3 (Low)": 부가 기능, 선택적 테스트

5. **예상 실행 시간** (header: "실행 시간")
   - 옵션:
     - "1분 미만 (Fast)"
     - "1-3분 (Medium)"
     - "3-5분 (Slow)"
     - "5분 이상 (Very Slow)"

6. **테스트 시나리오 개수** (header: "시나리오 개수")
   - 옵션:
     - "1개 (단일 시나리오)"
     - "2-3개 (기본 + 변형)"
     - "4-5개 (다양한 케이스)"
     - "5개 이상 (포괄적)"

## 4. 테스트 시나리오 작성

### 4.1 시나리오 구조

각 시나리오는 Given/When/Then 형식으로 작성:

```markdown
### 시나리오 1: [시나리오 제목]

**Given** (전제 조건)
- [조건 1]
- [조건 2]

**When** (실행 동작)
- [동작 1]
- [동작 2]

**Then** (예상 결과)
- [결과 1]
- [결과 2]
```

### 4.2 시나리오 유형

다음 유형을 고려하여 시나리오 작성:

1. **Happy Path**: 정상 플로우
2. **Edge Cases**: 경계값 테스트
3. **Error Cases**: 에러 상황
4. **Negative Cases**: 잘못된 입력

### 4.3 시나리오 작성 가이드

- **구체적으로**: "번역 버튼 클릭" ✅ vs "버튼 클릭" ❌
- **측정 가능하게**: "번역 결과가 표시된다" ✅ vs "잘 동작한다" ❌
- **독립적으로**: 각 시나리오는 다른 시나리오에 의존하지 않음
- **재현 가능하게**: 누가 실행해도 같은 결과

## 5. 테스트 데이터 정의

### 5.1 테스트 데이터 섹션

```markdown
## 테스트 데이터

### 입력 데이터

| 항목 | 값 | 설명 |
| ---- | -- | ---- |
| 영어 텍스트 | "Hello World" | 간단한 인사말 |
| 한국어 텍스트 | "안녕하세요" | 간단한 인사말 |

### 예상 결과

| 시나리오 | 예상 결과 | 검증 방법 |
| -------- | --------- | --------- |
| 영어→한국어 | "안녕하세요" 또는 유사 표현 | 텍스트 포함 확인 |
```

### 5.2 UI 선택자 (Playwright 참고용)

```markdown
## UI 선택자 (Playwright 참고)

| 엘리먼트 | 선택자 | 설명 |
| -------- | ------ | ---- |
| 입력 필드 | `textarea[placeholder*="텍스트"]` | 메인 입력 영역 |
| 번역 버튼 | `button:has-text("번역")` | 번역 실행 버튼 |
| 결과 영역 | `div[data-testid="result"]` | 번역 결과 표시 영역 |
```

**참고**: 실제 구현 시 앱에 `data-testid` 속성 추가 권장

## 6. 문서 생성

### 6.1 파일 경로

```
docs/test-cases/TC-XXX-feature-name.md
```

예시:
- `docs/test-cases/TC-001-page-rendering.md`
- `docs/test-cases/TC-002-translation-e2e.md`

### 6.2 문서 템플릿

```markdown
# TC-XXX: [기능명]

- **작성일**: YYYY-MM-DD
- **작성자**: QA Team
- **마지막 업데이트**: YYYY-MM-DD
- **상태**: 🔲 작성중 / ✅ 완료 / ⏸️ 보류
- **우선순위**: P0 / P1 / P2 / P3
- **예상 실행 시간**: X분

## 개요

### 테스트 목적

[테스트 목적 설명]

### 테스트 범위

- [범위 1]
- [범위 2]

### 관련 FEATURE

- FEATURE-XXX: [관련 기능명]

## 전제 조건

- [ ] Streamlit 앱이 실행 중이어야 함 (`http://localhost:8501`)
- [ ] 유효한 API 키가 설정되어 있어야 함
- [ ] [추가 전제 조건]

## 테스트 시나리오

### 시나리오 1: [시나리오 제목]

**Given** (전제 조건)
- [조건 1]
- [조건 2]

**When** (실행 동작)
- [동작 1]
- [동작 2]

**Then** (예상 결과)
- [결과 1]
- [결과 2]

---

### 시나리오 2: [시나리오 제목]

...

## 테스트 데이터

### 입력 데이터

| 항목 | 값 | 설명 |
| ---- | -- | ---- |
| [항목명] | [값] | [설명] |

### 예상 결과

| 시나리오 | 예상 결과 | 검증 방법 |
| -------- | --------- | --------- |
| [시나리오] | [결과] | [방법] |

## UI 선택자 (Playwright 참고)

| 엘리먼트 | 선택자 | 설명 |
| -------- | ------ | ---- |
| [엘리먼트명] | `[선택자]` | [설명] |

## 실행 방법

### 수동 테스트

1. [단계 1]
2. [단계 2]
3. [결과 확인]

### 자동 테스트 (Playwright)

```bash
# 향후 구현 예정
pytest tests/integration/test_TC_XXX.py
```

## 주의사항

- [주의사항 1]
- [주의사항 2]

## 변경 이력

| 날짜 | 변경 내용 | 작성자 |
| ---- | --------- | ------ |
| YYYY-MM-DD | 초안 작성 | QA Team |

---

**마지막 업데이트**: YYYY-MM-DD
```

### 6.3 Markdownlint 규칙 준수

- MD022: 제목 주변에 빈 줄 추가
- MD032: 리스트 주변에 빈 줄 추가
- 모든 문서는 빈 줄로 끝나야 함

## 7. Gherkin Feature 파일 생성

### 7.1 파일 경로

```
tests/integration/features/TC-XXX-feature-name.feature
```

예시:
- `tests/integration/features/TC-001-page-rendering.feature`
- `tests/integration/features/TC-002-translation-e2e.feature`

### 7.2 Gherkin 구조

```gherkin
Feature: [기능명]
  [기능 설명 1-2줄]

  Background:
    Given [공통 전제 조건]

  Scenario: [시나리오 제목 1]
    Given [전제 조건]
    When [실행 동작]
    Then [예상 결과]
    And [추가 결과]

  Scenario: [시나리오 제목 2]
    Given [전제 조건]
    When [실행 동작]
    Then [예상 결과]
```

### 7.3 Gherkin 작성 원칙

1. **한국어 사용**: 모든 스텝을 한국어로 작성
2. **구체적으로**: "번역 버튼 클릭" ✅ vs "버튼 클릭" ❌
3. **파라미터화**: 반복되는 패턴은 파라미터로 추출
   - 예: `Then "TransBot" 타이틀이 표시됨`
   - 예: `And "{button_text}" 버튼이 표시됨`
4. **Background 활용**: 모든 시나리오의 공통 전제 조건은 Background에 작성
5. **And 사용**: Then 이후 추가 검증은 And로 연결

### 7.4 TC 문서 → Gherkin 변환 규칙

TC 문서의 Given/When/Then을 Gherkin으로 변환:

**TC 문서**:
```markdown
**Given** (전제 조건)
- Streamlit 앱이 실행 중
- 페이지가 로드됨

**When** (실행 동작)
- 브라우저에서 앱에 접속

**Then** (예상 결과)
- 타이틀 "TransBot"이 표시됨
- 페이지가 3초 이내에 로드됨
```

**Gherkin**:
```gherkin
Scenario: 기본 페이지 로딩 및 타이틀 표시
  Given Streamlit 앱이 "http://localhost:8501"에서 실행 중
  When 브라우저에서 앱에 접속
  Then 페이지가 3초 이내에 로드됨
  And 타이틀 "TransBot"이 표시됨
```

### 7.5 자동 생성 규칙

1. **Feature 제목**: TC 문서의 "기능명"을 그대로 사용
2. **Feature 설명**: TC 문서의 "테스트 목적"을 1-2줄로 요약
3. **Background**: 모든 시나리오의 공통 전제 조건 추출
4. **Scenario**: TC 문서의 각 시나리오를 Gherkin Scenario로 변환
5. **파라미터화**: 따옴표로 감싸진 값은 자동으로 파라미터화

## 8. pytest-bdd Step Definitions 생성

### 8.1 파일 경로

```
tests/integration/step_defs/test_feature_name.py
```

예시:
- `tests/integration/step_defs/test_page_rendering.py`
- `tests/integration/step_defs/test_translation_e2e.py`

### 8.2 Step Definitions 구조

```python
"""TC-XXX [기능명] 테스트의 Step 정의"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-XXX-feature-name.feature')

# ============================================================================
# Given Steps (전제 조건)
# ============================================================================

@given('Streamlit 앱이 "http://localhost:8501"에서 실행 중')
def streamlit_app_running():
    """앱이 실행 중인지 확인 (setup에서 이미 처리됨)"""
    pass

@given('페이지가 정상적으로 로드됨')
def page_loaded(page: Page):
    """페이지 로드"""
    page.goto("http://localhost:8501")
    expect(page).to_have_url("http://localhost:8501", timeout=5000)

# 파라미터화된 스텝
@given(parsers.parse('".env" 파일에 "{env_var}" 설정됨'))
def env_variable_set(env_var: str):
    """환경 변수 확인 (테스트 환경에서 이미 설정되어 있다고 가정)"""
    pass

# ============================================================================
# When Steps (실행 동작)
# ============================================================================

@when('브라우저에서 앱에 접속')
def navigate_to_app(page: Page):
    """앱에 접속"""
    page.goto("http://localhost:8501")

@when('메인 화면을 확인')
def check_main_screen(page: Page):
    """메인 화면 확인 (실제로는 아무 동작도 하지 않음)"""
    pass

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then('페이지가 3초 이내에 로드됨')
def page_loads_quickly(page: Page):
    """페이지 빠른 로딩 확인"""
    expect(page).to_have_url("http://localhost:8501", timeout=3000)

# 파라미터화된 스텝
@then(parsers.parse('타이틀 "{title}"이 표시됨'))
def title_displayed(page: Page, title: str):
    """타이틀 표시 확인"""
    expect(page.locator("h1")).to_contain_text(title)

@then(parsers.parse('브라우저 탭 제목이 "{page_title}"으로 표시됨'))
def page_title_displayed(page: Page, page_title: str):
    """브라우저 탭 제목 확인"""
    expect(page).to_have_title(page_title)
```

### 8.3 Step Definitions 작성 원칙

1. **Docstring 필수**: 각 스텝 함수에 한 줄 설명 작성
2. **Page fixture**: UI 인터랙션이 필요한 스텝은 `page: Page` 파라미터 사용
3. **Playwright expect**: 검증은 `expect()` 함수 사용
4. **파라미터화**: Gherkin에서 `"값"` 형태로 전달된 값은 `parsers.parse()` 사용
5. **섹션 구분**: Given/When/Then 섹션을 주석으로 명확히 구분
6. **integration 마커**: `pytestmark = pytest.mark.integration` 추가

### 8.4 자동 생성 규칙

1. **파일명**: TC-XXX-feature-name.feature → test_feature_name.py
   - 예: TC-001-page-rendering → test_page_rendering.py
2. **scenarios() 호출**: Feature 파일 경로를 상대 경로로 지정
3. **스텝 함수 생성**: Gherkin의 각 스텝에 대응하는 함수 생성
4. **파라미터 추출**: `"{param}"` 형태는 자동으로 파라미터화
5. **Playwright assertions**:
   - "표시됨" → `expect().to_be_visible()`
   - "텍스트 포함" → `expect().to_contain_text()`
   - "속성 확인" → `expect().to_have_attribute()`
   - "값 확인" → `expect().to_have_value()`
   - "활성화" → `expect().to_be_enabled()`

### 8.5 공통 Step Definitions

자주 사용되는 스텝은 공통 함수로 제공:

```python
# 공통으로 사용되는 스텝 (모든 TC에서 재사용 가능)

@given('Streamlit 앱이 "http://localhost:8501"에서 실행 중')
def streamlit_app_running():
    """앱 실행 확인 (conftest에서 처리)"""
    pass

@given('페이지가 정상적으로 로드됨')
def page_loaded(page: Page):
    """페이지 로드"""
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:8501", timeout=5000)

@when('브라우저에서 앱에 접속')
def navigate_to_app(page: Page):
    """앱 접속"""
    page.goto("http://localhost:8501")

@then('로딩 스피너가 사라지고 메인 화면이 표시됨')
def loading_spinner_disappears(page: Page):
    """로딩 완료 확인"""
    page.wait_for_load_state("networkidle")
```

## 9. 다음 단계 제안

문서 및 자동화 스크립트 생성 완료 후 사용자에게 다음 단계 제안:

```markdown
## ✅ 테스트 케이스 생성 완료

### 생성된 파일

1. **테스트 케이스 문서**
   - 파일: `docs/test-cases/TC-XXX-feature-name.md`
   - 시나리오 개수: X개
   - 우선순위: PX

2. **Gherkin Feature 파일**
   - 파일: `tests/integration/features/TC-XXX-feature-name.feature`
   - BDD 형식의 시나리오 정의

3. **pytest-bdd Step Definitions**
   - 파일: `tests/integration/step_defs/test_feature_name.py`
   - Playwright 기반 자동화 테스트 구현

### 다음 단계

#### 1. 문서 리뷰
- 테스트 시나리오가 요구사항을 충족하는지 확인
- 누락된 케이스가 있는지 검토

#### 2. 자동화 테스트 실행
Streamlit 앱이 실행 중인지 확인 후 테스트 실행:

\`\`\`bash
# Streamlit 앱 실행 (별도 터미널)
streamlit run app.py

# 테스트 실행
pytest tests/integration/features/TC-XXX-feature-name.feature --browser chromium --no-cov -v

# 또는 특정 시나리오만 실행
pytest tests/integration/features/TC-XXX-feature-name.feature -k "시나리오명" --browser chromium --no-cov -v
\`\`\`

#### 3. 테스트 결과 확인
- 모든 시나리오가 통과하는지 확인
- 실패한 테스트가 있다면:
  - UI 선택자가 올바른지 확인
  - 타임아웃 설정이 적절한지 확인
  - 앱의 실제 동작과 예상 결과가 일치하는지 확인

#### 4. 수동 테스트 실행 (선택사항)
- "실행 방법 > 수동 테스트" 섹션을 참고하여 수동으로 검증
- 자동화 테스트가 놓친 부분이 있는지 확인

#### 5. Git 커밋
\`\`\`bash
git add docs/test-cases/TC-XXX-feature-name.md \\
        tests/integration/features/TC-XXX-feature-name.feature \\
        tests/integration/step_defs/test_feature_name.py
git commit -m "test: TC-XXX [기능명] 테스트 케이스 및 자동화 스크립트 추가"
\`\`\`
```

## 체크리스트

테스트 케이스 생성 전 확인:

### 문서 관련
- [ ] TC 번호 중복 확인
- [ ] 기능명이 명확하고 간결한가?
- [ ] 테스트 목적이 구체적으로 기술되었는가?
- [ ] Given/When/Then 형식을 준수했는가?
- [ ] 각 시나리오가 독립적인가?
- [ ] 테스트 데이터가 구체적으로 정의되었는가?
- [ ] UI 선택자가 포함되었는가? (Playwright 참고용)
- [ ] 전제 조건이 명확한가?
- [ ] Markdownlint 규칙을 준수했는가?
- [ ] 파일 경로가 올바른가? (docs/test-cases/)

### Gherkin 파일 관련
- [ ] Feature 파일 경로가 올바른가? (tests/integration/features/)
- [ ] Feature 제목과 설명이 명확한가?
- [ ] Background에 공통 전제 조건이 포함되었는가?
- [ ] 각 Scenario의 제목이 명확한가?
- [ ] Given/When/Then/And 스텝이 올바르게 작성되었는가?
- [ ] 파라미터화가 필요한 값은 따옴표로 감싸졌는가?
- [ ] 모든 스텝이 한국어로 작성되었는가?

### Step Definitions 관련
- [ ] Step definitions 파일 경로가 올바른가? (tests/integration/step_defs/)
- [ ] scenarios() 호출이 올바른 Feature 파일을 가리키는가?
- [ ] 모든 Gherkin 스텝에 대응하는 함수가 작성되었는가?
- [ ] 파라미터화된 스텝에 parsers.parse()가 사용되었는가?
- [ ] Page fixture가 필요한 스텝에 `page: Page` 파라미터가 있는가?
- [ ] Playwright expect assertions가 올바르게 사용되었는가?
- [ ] 각 스텝 함수에 docstring이 포함되었는가?
- [ ] Given/When/Then 섹션이 주석으로 구분되었는가?
- [ ] pytestmark = pytest.mark.integration이 추가되었는가?

## 테스트 케이스 카테고리 (참고)

프로젝트 표준 카테고리:

| TC 번호 | 기능명 | 설명 |
| ------- | ------ | ---- |
| TC-001-page-rendering | 페이지 렌더링 | 앱 기본 동작 확인 (Smoke Test) |
| TC-002-translation-e2e | 번역 E2E 플로우 | 전체 번역 프로세스 검증 |
| TC-003-text-analysis | 텍스트 분석 및 통계 | 언어 감지 및 카운팅 기능 검증 |
| TC-004-ui-interactions | UI 인터랙션 | 사용자 인터페이스 동작 검증 |
| TC-005-settings-config | 설정 관리 | 사이드바 설정 및 옵션 검증 |
| TC-006-error-handling | 에러 핸들링 | 예외 상황 대응 검증 |

## 예시

### 입력

```bash
/generate-test-case "번역 E2E 플로우"
```

### 출력

```markdown
## 테스트 케이스 정보 수집

다음 정보를 입력해주세요:

1. **테스트 기능**: 번역 E2E 플로우
2. **테스트 목적**: 사용자가 텍스트를 입력하고 번역 버튼을 클릭하여 결과를 받는 전체 플로우 검증
3. **테스트 범위**: UI 렌더링, 사용자 인터랙션, 데이터 처리
4. **우선순위**: P0 (Critical)
5. **예상 실행 시간**: 1-3분 (Medium)
6. **테스트 시나리오 개수**: 4-5개 (다양한 케이스)

---

## 분석 결과

**TC 번호**: TC-002
**기능명**: translation-e2e
**파일 경로**:
  - 문서: docs/test-cases/TC-002-translation-e2e.md
  - Gherkin: tests/integration/features/TC-002-translation-e2e.feature
  - Step Definitions: tests/integration/step_defs/test_translation_e2e.py

**시나리오 개수**: 4개
  - 영어 → 한국어 번역
  - 한국어 → 영어 번역
  - Markdown 포맷 보존 번역
  - 다중 스타일 번역

위 내용으로 테스트 케이스를 생성하시겠습니까?
- 예 (추천) - 문서, Gherkin, Step Definitions 모두 생성
- 시나리오 수정
- 취소

[사용자가 "예" 선택]

✅ 테스트 케이스 생성 완료

**생성된 파일**:
1. docs/test-cases/TC-002-translation-e2e.md
2. tests/integration/features/TC-002-translation-e2e.feature
3. tests/integration/step_defs/test_translation_e2e.py

**시나리오 개수**: 4개
**우선순위**: P0

### 다음 단계

1. 문서 리뷰
2. 자동화 테스트 실행:
   \`\`\`bash
   pytest tests/integration/features/TC-002-translation-e2e.feature --browser chromium --no-cov -v
   \`\`\`
3. Git 커밋
```

## 고급 기능

### 시나리오 자동 추론

사용자가 기능명만 제공한 경우, 앱의 구조를 분석하여 시나리오 자동 생성:

1. **app.py 분석**: 관련 함수 및 UI 컴포넌트 파악
2. **PRD 참조**: 해당 FEATURE의 요구사항 확인
3. **기존 테스트 참조**: 유사한 TC가 있는지 확인
4. **시나리오 제안**: Given/When/Then 초안 작성

### 배치 생성

여러 TC를 한 번에 생성:

```bash
/generate-test-case --batch TC-001,TC-002,TC-003
```

각 TC에 대해 최소한의 질문만 하고 기본 템플릿으로 문서 생성.

---

**작성자**: TransBot Development Team
**최종 업데이트**: 2026-02-07