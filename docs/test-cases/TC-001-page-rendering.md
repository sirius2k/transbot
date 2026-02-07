# TC-001: 페이지 렌더링

- **작성일**: 2026-02-07
- **작성자**: QA Team
- **마지막 업데이트**: 2026-02-07
- **상태**: ✅ 완료
- **우선순위**: P0 (Critical)
- **예상 실행 시간**: 1분 미만

## 개요

### 테스트 목적

Streamlit 앱이 정상적으로 시작되고, 타이틀/입력 영역/사이드바 등 핵심 UI 요소가 올바르게 렌더링되는지 검증합니다. 앱의 가장 기본적인 동작을 확인하는 Smoke Test입니다.

### 테스트 범위

- **UI 렌더링**: 타이틀, 입력 필드, 버튼, 사이드바 표시 확인
- **사용자 인터랙션**: 기본 UI 요소 클릭 가능 여부 확인
- **상태 관리**: Session state 초기화 확인

### 관련 FEATURE

- FEATURE-001: 영어 ↔ 한국어 양방향 번역
- FEATURE-007: 사이드바 UI (설정 섹션)

## 전제 조건

- [ ] Streamlit 앱이 실행 중이어야 함 (`streamlit run app.py`)
- [ ] 앱이 `http://localhost:8501`에서 접근 가능해야 함
- [ ] 유효한 API 키가 `.env` 파일에 설정되어 있어야 함 (OpenAI 또는 Azure)
- [ ] 브라우저가 JavaScript를 지원해야 함

## 테스트 시나리오

### 시나리오 1: 기본 페이지 로딩 및 타이틀 표시

**Given** (전제 조건)

- Streamlit 앱이 실행 중임
- 브라우저가 앱 URL에 접근 가능함

**When** (실행 동작)

- 브라우저에서 `http://localhost:8501` 접속

**Then** (예상 결과)

- 페이지가 3초 이내에 로드됨
- 타이틀이 표시됨: "🌐 TransBot" 또는 설정된 APP_TITLE
- 페이지 탭 제목이 "TransBot"으로 표시됨
- 로딩 스피너가 사라지고 메인 화면이 표시됨

---

### 시나리오 2: 입력 영역 렌더링

**Given** (전제 조건)

- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 메인 화면을 확인함

**Then** (예상 결과)

- "원문" 레이블이 표시됨
- 텍스트 입력 필드가 렌더링됨
- Placeholder 텍스트가 표시됨: "번역할 텍스트를 입력하세요... (한국어/English 자동 감지)"
- 입력 필드가 빈 상태로 초기화됨
- 통계 정보 영역이 표시됨 (초기에는 빈 상태)

---

### 시나리오 3: 사이드바 렌더링 (OpenAI Provider)

**Given** (전제 조건)

- `.env` 파일에 `AI_PROVIDER=openai` 설정됨
- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 사이드바를 확인함

**Then** (예상 결과)

- 사이드바가 화면 왼쪽에 표시됨
- "⚙️ 설정" 헤더가 표시됨
- "AI 모델 선택" 섹션이 표시됨
- 모델 선택 드롭다운이 렌더링됨 (GPT-4o, GPT-4o Mini 등)
- "번역 옵션" 섹션이 표시됨
- Help 섹션이 표시됨

---

### 시나리오 4: 사이드바 렌더링 (Azure Provider)

**Given** (전제 조건)

- `.env` 파일에 `AI_PROVIDER=azure` 설정됨
- Azure OpenAI 관련 환경 변수가 설정됨
- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 사이드바를 확인함

**Then** (예상 결과)

- 사이드바가 화면 왼쪽에 표시됨
- "⚙️ 설정" 헤더가 표시됨
- "Azure Deployment 선택" 섹션이 표시됨
- Deployment 선택 드롭다운이 렌더링됨
- "번역 옵션" 섹션이 표시됨

---

### 시나리오 5: 액션 버튼 표시

**Given** (전제 조건)

- 페이지가 정상적으로 로드됨

**When** (실행 동작)

- 입력 영역 하단을 확인함

**Then** (예상 결과)

- "🚀 번역" 버튼이 표시됨
- "🗑️ 지우기" 버튼이 표시됨
- 두 버튼이 좌우로 배치됨
- 버튼이 클릭 가능한 상태임 (disabled 아님)

## 테스트 데이터

### 입력 데이터

테스트 데이터 없음 (UI 렌더링만 확인)

### 예상 결과

| 시나리오 | 예상 결과 | 검증 방법 |
| -------- | --------- | --------- |
| 시나리오 1 | 타이틀 "🌐 TransBot" 표시 | 텍스트 존재 확인 |
| 시나리오 2 | 입력 필드 렌더링 | textarea 요소 존재 확인 |
| 시나리오 3 | 사이드바 "⚙️ 설정" 표시 | 사이드바 헤더 확인 |
| 시나리오 4 | Azure Deployment 선택 표시 | 드롭다운 존재 확인 |
| 시나리오 5 | "🚀 번역" 버튼 표시 | 버튼 요소 존재 확인 |

## UI 선택자 (Playwright 참고)

| 엘리먼트 | 선택자 | 설명 |
| -------- | ------ | ---- |
| 페이지 타이틀 | `h1:has-text("TransBot")` | 메인 타이틀 |
| 입력 필드 레이블 | `text=원문` | "원문" 레이블 |
| 입력 텍스트 영역 | `textarea[placeholder*="번역할 텍스트"]` | 메인 입력 필드 |
| 사이드바 헤더 | `text=⚙️ 설정` | 사이드바 설정 헤더 |
| 모델 선택 드롭다운 (OpenAI) | `text=AI 모델 선택` | 모델 선택 섹션 |
| Deployment 선택 (Azure) | `text=Azure Deployment 선택` | Deployment 선택 섹션 |
| 번역 버튼 | `button:has-text("🚀 번역")` | 번역 실행 버튼 |
| 지우기 버튼 | `button:has-text("🗑️ 지우기")` | 입력 초기화 버튼 |

**참고**: 향후 자동화 테스트 구현 시 앱에 `data-testid` 속성 추가를 권장합니다.

예시:

```python
st.text_area(
    "원문",
    key="input_text",
    data_testid="main-input-area"  # 추가 권장
)
```

## 실행 방법

### 수동 테스트

1. **앱 실행**

   ```bash
   streamlit run app.py
   ```

2. **브라우저 접속**
   - `http://localhost:8501` 접속

3. **시나리오 1 검증: 타이틀 확인**
   - [ ] 페이지가 3초 이내에 로드됨
   - [ ] "🌐 TransBot" 타이틀 표시
   - [ ] 브라우저 탭 제목 "TransBot" 확인

4. **시나리오 2 검증: 입력 영역 확인**
   - [ ] "원문" 레이블 표시
   - [ ] 텍스트 입력 필드 렌더링
   - [ ] Placeholder 텍스트 표시
   - [ ] 통계 영역 표시

5. **시나리오 3/4 검증: 사이드바 확인**
   - [ ] 사이드바 표시
   - [ ] "⚙️ 설정" 헤더 표시
   - [ ] 모델/Deployment 선택 드롭다운 표시
   - [ ] "번역 옵션" 섹션 표시

6. **시나리오 5 검증: 버튼 확인**
   - [ ] "🚀 번역" 버튼 표시
   - [ ] "🗑️ 지우기" 버튼 표시
   - [ ] 버튼 클릭 가능 상태 확인

### 자동 테스트 (pytest-bdd + Playwright)

#### 설치 방법

```bash
# pytest-bdd와 Playwright 설치
pip install pytest-bdd playwright pytest-playwright
playwright install
```

#### 테스트 구조

```
tests/integration/
├── features/
│   └── TC-001-page-rendering.feature  # Gherkin 시나리오
├── step_defs/
│   └── test_page_rendering.py         # Step 구현
└── conftest.py                        # Fixtures 설정
```

#### Gherkin Feature 파일 예시

**파일**: `tests/integration/features/TC-001-page-rendering.feature`

```gherkin
Feature: 페이지 렌더링
  Streamlit 앱의 기본 UI 요소가 정상적으로 렌더링되는지 확인하는 Smoke Test

  Background:
    Given Streamlit 앱이 "http://localhost:8501"에서 실행 중

  Scenario: 기본 페이지 로딩 및 타이틀 표시
    When 브라우저에서 앱에 접속
    Then 페이지가 3초 이내에 로드됨
    And 타이틀 "TransBot"이 표시됨
    And 브라우저 탭 제목이 "TransBot"으로 표시됨
    And 로딩 스피너가 사라지고 메인 화면이 표시됨

  Scenario: 입력 영역 렌더링
    Given 페이지가 정상적으로 로드됨
    When 메인 화면을 확인
    Then "원문" 레이블이 표시됨
    And 텍스트 입력 필드가 렌더링됨
    And Placeholder "번역할 텍스트를 입력하세요"가 표시됨
    And 입력 필드가 빈 상태로 초기화됨
    And 통계 정보 영역이 표시됨

  Scenario: 사이드바 렌더링 (OpenAI Provider)
    Given ".env" 파일에 "AI_PROVIDER=openai" 설정됨
    And 페이지가 정상적으로 로드됨
    When 사이드바를 확인
    Then 사이드바가 화면 왼쪽에 표시됨
    And "⚙️ 설정" 헤더가 표시됨
    And "AI 모델 선택" 섹션이 표시됨
    And 모델 선택 드롭다운이 렌더링됨
    And "번역 옵션" 섹션이 표시됨
    And Help 섹션이 표시됨

  Scenario: 액션 버튼 표시
    Given 페이지가 정상적으로 로드됨
    When 입력 영역 하단을 확인
    Then "🚀 번역" 버튼이 표시됨
    And "🗑️ 지우기" 버튼이 표시됨
    And 두 버튼이 좌우로 배치됨
    And 버튼이 클릭 가능한 상태임
```

#### pytest-bdd Step 정의 예시

**파일**: `tests/integration/step_defs/test_page_rendering.py`

```python
"""TC-001 페이지 렌더링 테스트의 Step 정의"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

# Feature 파일 로드
scenarios('../features/TC-001-page-rendering.feature')

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

@when('사이드바를 확인')
def check_sidebar(page: Page):
    """사이드바 확인 (실제로는 아무 동작도 하지 않음)"""
    pass

@when('입력 영역 하단을 확인')
def check_action_buttons_area(page: Page):
    """입력 영역 하단 확인"""
    pass

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then('페이지가 3초 이내에 로드됨')
def page_loads_quickly(page: Page):
    """페이지 빠른 로딩 확인"""
    expect(page).to_have_url("http://localhost:8501", timeout=3000)

@then(parsers.parse('타이틀 "{title}"이 표시됨'))
def title_displayed(page: Page, title: str):
    """타이틀 표시 확인"""
    expect(page.locator("h1")).to_contain_text(title)

@then(parsers.parse('브라우저 탭 제목이 "{page_title}"으로 표시됨'))
def page_title_displayed(page: Page, page_title: str):
    """브라우저 탭 제목 확인"""
    expect(page).to_have_title(page_title)

@then('로딩 스피너가 사라지고 메인 화면이 표시됨')
def loading_spinner_disappears(page: Page):
    """로딩 완료 확인"""
    # Streamlit 로딩 스피너가 사라질 때까지 대기
    page.wait_for_load_state("networkidle")

@then(parsers.parse('"{label}" 레이블이 표시됨'))
def label_displayed(page: Page, label: str):
    """레이블 표시 확인"""
    expect(page.locator(f"text={label}")).to_be_visible()

@then('텍스트 입력 필드가 렌더링됨')
def input_field_rendered(page: Page):
    """입력 필드 렌더링 확인"""
    expect(page.locator("textarea")).to_be_visible()

@then(parsers.parse('Placeholder "{placeholder}"가 표시됨'))
def placeholder_displayed(page: Page, placeholder: str):
    """Placeholder 표시 확인"""
    input_field = page.locator("textarea")
    expect(input_field).to_have_attribute("placeholder", f"{placeholder}")

@then('입력 필드가 빈 상태로 초기화됨')
def input_field_empty(page: Page):
    """입력 필드 빈 상태 확인"""
    input_field = page.locator("textarea")
    expect(input_field).to_have_value("")

@then('통계 정보 영역이 표시됨')
def stats_area_visible(page: Page):
    """통계 영역 표시 확인"""
    # 통계 영역은 초기에 빈 상태일 수 있음
    pass

@then('사이드바가 화면 왼쪽에 표시됨')
def sidebar_visible(page: Page):
    """사이드바 표시 확인"""
    # Streamlit 사이드바 확인
    expect(page.locator('[data-testid="stSidebar"]')).to_be_visible()

@then(parsers.parse('"{header}" 헤더가 표시됨'))
def header_displayed(page: Page, header: str):
    """헤더 표시 확인"""
    expect(page.locator(f"text={header}")).to_be_visible()

@then(parsers.parse('"{section}" 섹션이 표시됨'))
def section_displayed(page: Page, section: str):
    """섹션 표시 확인"""
    expect(page.locator(f"text={section}")).to_be_visible()

@then('모델 선택 드롭다운이 렌더링됨')
def model_dropdown_rendered(page: Page):
    """모델 선택 드롭다운 확인"""
    # Streamlit selectbox 확인
    expect(page.locator('[data-baseweb="select"]')).to_be_visible()

@then('Help 섹션이 표시됨')
def help_section_visible(page: Page):
    """Help 섹션 표시 확인"""
    expect(page.locator("text=Help")).to_be_visible()

@then(parsers.parse('"{button_text}" 버튼이 표시됨'))
def button_displayed(page: Page, button_text: str):
    """버튼 표시 확인"""
    expect(page.locator(f"button:has-text('{button_text}')")).to_be_visible()

@then('두 버튼이 좌우로 배치됨')
def buttons_layout(page: Page):
    """버튼 레이아웃 확인"""
    # 두 버튼이 존재하는지 확인
    buttons = page.locator("button")
    expect(buttons).to_have_count(2, minimum=True)

@then('버튼이 클릭 가능한 상태임')
def buttons_enabled(page: Page):
    """버튼 활성화 상태 확인"""
    translate_btn = page.locator("button:has-text('🚀 번역')")
    expect(translate_btn).to_be_enabled()
```

#### conftest.py 설정 예시

**파일**: `tests/integration/conftest.py`

```python
"""pytest-bdd + Playwright fixtures"""
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """브라우저 컨텍스트 설정

    pytest-playwright가 제공하는 browser_context_args를 확장하여
    기본 뷰포트 크기를 설정합니다.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

# pytest-playwright가 제공하는 page fixture를 사용
# 별도의 page fixture 재정의 불필요
```

#### 실행 방법

```bash
# 전체 feature 실행
pytest tests/integration/features/TC-001-page-rendering.feature

# 특정 시나리오만 실행
pytest tests/integration/features/TC-001-page-rendering.feature -k "기본 페이지"

# 상세 출력
pytest tests/integration/features/TC-001-page-rendering.feature -v

# HTML 리포트 생성
pytest tests/integration/features/TC-001-page-rendering.feature --html=report.html
```

## 주의사항

- **로딩 시간**: 초기 로딩 시 Streamlit 초기화로 인해 2-3초 소요될 수 있음
- **캐시**: 이전 테스트의 세션 상태가 남아있을 수 있으므로, 필요시 브라우저 캐시 삭제
- **포트 충돌**: 8501 포트가 이미 사용 중이면 다른 포트로 실행됨 (8502, 8503 등)
- **API 키**: OpenAI/Azure API 키가 없으면 경고 메시지가 표시될 수 있으나, 페이지 렌더링은 정상 작동해야 함
- **Provider 설정**: 환경 변수 `AI_PROVIDER` 값에 따라 사이드바 내용이 달라짐

## 변경 이력

| 날짜 | 변경 내용 | 작성자 |
| ---- | --------- | ------ |
| 2026-02-07 | 초안 작성 | QA Team |
| 2026-02-07 | pytest-bdd + Playwright 자동화 테스트 섹션 추가 | QA Team |

---

**마지막 업데이트**: 2026-02-07
