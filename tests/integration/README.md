# 통합 테스트 (Integration Tests)

이 디렉토리는 TransBot의 브라우저 기반 통합 테스트를 포함합니다.

## 디렉토리 구조

```
tests/integration/
├── features/              # Gherkin feature 파일
│   ├── __init__.py
│   └── TC-001-page-rendering.feature
├── step_defs/            # pytest-bdd step 정의
│   ├── __init__.py
│   └── test_page_rendering.py
├── conftest.py           # pytest fixtures
└── README.md            # 본 문서
```

## 설치

```bash
# pytest-bdd와 Playwright 설치
pip install pytest-bdd playwright pytest-playwright
playwright install
```

## 실행 방법

### 전체 테스트 실행

```bash
# 모든 feature 실행
pytest tests/integration/

# 특정 feature 실행
pytest tests/integration/features/TC-001-page-rendering.feature
```

### 시나리오 필터링

```bash
# 특정 시나리오만 실행
pytest tests/integration/features/TC-001-page-rendering.feature -k "기본 페이지"

# 여러 시나리오 실행
pytest tests/integration/features/TC-001-page-rendering.feature -k "페이지 or 입력"
```

### 상세 출력

```bash
# 상세 출력 (-v)
pytest tests/integration/features/TC-001-page-rendering.feature -v

# 매우 상세한 출력 (-vv)
pytest tests/integration/features/TC-001-page-rendering.feature -vv
```

### 리포트 생성

```bash
# HTML 리포트
pytest tests/integration/ --html=report.html --self-contained-html

# JUnit XML 리포트
pytest tests/integration/ --junitxml=report.xml
```

## 테스트 전제 조건

1. **Streamlit 앱 실행**: `streamlit run app.py`
2. **환경 변수 설정**: `.env` 파일에 API 키 설정
3. **브라우저 설치**: `playwright install`

## Gherkin Feature 작성 가이드

### 기본 구조

```gherkin
Feature: 기능명
  기능 설명

  Background:
    Given 공통 전제 조건

  Scenario: 시나리오 제목
    Given 전제 조건
    When 실행 동작
    Then 예상 결과
    And 추가 검증
```

### 작성 규칙

1. **명확성**: 비개발자도 이해할 수 있도록 작성
2. **독립성**: 각 시나리오는 독립적으로 실행 가능해야 함
3. **재사용성**: Step 정의는 여러 Feature에서 재사용 가능하도록 작성
4. **구체성**: 추상적인 표현 대신 구체적인 검증 기준 사용

### 예시

```gherkin
# 좋은 예
Then "🚀 번역" 버튼이 표시됨
And 버튼이 클릭 가능한 상태임

# 나쁜 예
Then 버튼이 잘 표시됨
And 버튼이 정상 동작함
```

## pytest-bdd Step 정의 가이드

### Step 데코레이터

- `@given`: 전제 조건 설정
- `@when`: 실행 동작
- `@then`: 예상 결과 검증

### 파라미터 사용

```python
from pytest_bdd import parsers

# 문자열 파라미터
@then(parsers.parse('타이틀 "{title}"이 표시됨'))
def title_displayed(page: Page, title: str):
    expect(page.locator("h1")).to_contain_text(title)

# 숫자 파라미터
@then(parsers.parse('페이지가 {timeout:d}초 이내에 로드됨'))
def page_loads_within_timeout(page: Page, timeout: int):
    expect(page).to_have_url("http://localhost:8501", timeout=timeout * 1000)
```

### Playwright API 활용

```python
# 요소 존재 확인
expect(page.locator("h1")).to_be_visible()

# 텍스트 포함 확인
expect(page.locator("h1")).to_contain_text("TransBot")

# 속성 확인
expect(page.locator("textarea")).to_have_attribute("placeholder", "...")

# 활성화 상태 확인
expect(page.locator("button")).to_be_enabled()

# 개수 확인
expect(page.locator("button")).to_have_count(2)
```

## 디버깅

### Headed 모드로 실행

```bash
# 브라우저 창을 띄워서 실행
pytest tests/integration/ --headed

# 느린 속도로 실행 (디버깅용)
pytest tests/integration/ --headed --slowmo=1000
```

### 스크린샷 캡처

```python
@then('페이지가 3초 이내에 로드됨')
def page_loads_quickly(page: Page):
    page.screenshot(path="debug.png")
    expect(page).to_have_url("http://localhost:8501", timeout=3000)
```

### 브레이크포인트

```python
@then('페이지가 3초 이내에 로드됨')
def page_loads_quickly(page: Page):
    import pdb; pdb.set_trace()  # 디버깅
    expect(page).to_have_url("http://localhost:8501", timeout=3000)
```

## 관련 문서

- [TC-001 테스트 케이스](../../docs/test-cases/TC-001-page-rendering.md)
- [pytest-bdd 공식 문서](https://pytest-bdd.readthedocs.io/)
- [Playwright 공식 문서](https://playwright.dev/python/)

---

**최종 업데이트**: 2026-02-07
