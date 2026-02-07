"""TC-004 UI 인터랙션 테스트의 Step 정의"""
import pytest
import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-004-ui-interactions.feature')

# ============================================================================
# Given Steps (전제 조건) - TC-002, TC-003에서 재사용
# ============================================================================

@given('Streamlit 앱이 "http://localhost:8501"에서 실행 중')
def streamlit_app_running():
    """앱이 실행 중인지 확인 (setup에서 이미 처리됨)"""
    pass

@given('페이지가 정상적으로 로드됨')
def page_loaded(page: Page):
    """페이지 로드"""
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    # URL 끝의 슬래시(/) 포함하여 검증
    expect(page).to_have_url(re.compile(r"http://localhost:8501/?"), timeout=5000)

@given('사이드바가 열려 있음')
def sidebar_opened(page: Page):
    """사이드바 열기"""
    # 사이드바가 닫혀있으면 열기
    sidebar_button = page.locator('[data-testid="collapsedControl"]')
    if sidebar_button.is_visible():
        sidebar_button.click()
        page.wait_for_timeout(500)

# ============================================================================
# When Steps (실행 동작)
# ============================================================================

@when(parsers.parse('사용자가 "{text}" 텍스트를 입력'))
def user_enters_text(page: Page, text: str):
    """텍스트 입력"""
    input_field = page.locator("textarea").first
    input_field.fill(text)
    # 통계 업데이트를 위해 잠시 대기
    page.wait_for_timeout(1000)

@when(parsers.parse('"{button_text}" 버튼을 클릭'))
def click_button(page: Page, button_text: str):
    """버튼 클릭"""
    button = page.locator(f"button:has-text('{button_text}')").first
    button.click()
    # 페이지 리렌더링을 위해 대기
    page.wait_for_timeout(1500)

@when('메인 화면을 확인')
def check_main_screen(page: Page):
    """메인 화면 확인 (실제로는 아무 동작도 하지 않음)"""
    pass

@when(parsers.parse('"{checkbox_text}" 체크박스를 선택'))
def select_checkbox(page: Page, checkbox_text: str):
    """체크박스 선택"""
    # Streamlit 체크박스는 label을 클릭해야 함 (input은 숨겨져 있음)
    checkbox_label = page.locator(f'label:has-text("{checkbox_text}")')

    # 체크박스가 이미 선택되어 있는지 확인
    checkbox_input = checkbox_label.locator('input[type="checkbox"]')
    if not checkbox_input.is_checked():
        # label을 클릭하여 체크박스 활성화
        checkbox_label.click()
        page.wait_for_timeout(500)

@when('입력 필드를 클릭')
def click_input_field(page: Page):
    """입력 필드 클릭"""
    input_field = page.locator("textarea").first
    input_field.click()
    page.wait_for_timeout(300)

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then('입력 필드가 비워짐')
def input_field_empty(page: Page):
    """입력 필드가 비워졌는지 확인"""
    input_field = page.locator("textarea").first
    expect(input_field).to_have_value("")

@then(parsers.parse('"{text}" 텍스트가 표시됨'))
def text_displayed(page: Page, text: str):
    """특정 텍스트가 표시되는지 확인"""
    page_content = page.content()
    assert text in page_content, f"'{text}' 텍스트가 표시되지 않음"

@then(parsers.parse('"{button_text}" 버튼이 표시됨'))
def button_displayed(page: Page, button_text: str):
    """버튼이 표시되는지 확인"""
    button = page.locator(f"button:has-text('{button_text}')").first
    expect(button).to_be_visible()

@then(parsers.parse('"{checkbox_text}" 체크박스가 선택됨'))
def checkbox_selected(page: Page, checkbox_text: str):
    """체크박스가 선택되었는지 확인"""
    checkbox_label = page.locator(f'label:has-text("{checkbox_text}")')
    checkbox_input = checkbox_label.locator('input[type="checkbox"]')
    expect(checkbox_input).to_be_checked()

@then(parsers.parse('입력 필드에 "{text}" 텍스트가 표시됨'))
def input_field_contains_text(page: Page, text: str):
    """입력 필드에 텍스트가 표시되는지 확인"""
    input_field = page.locator("textarea").first
    expect(input_field).to_have_value(text)

@then('통계 정보가 실시간으로 표시됨')
def statistics_displayed_realtime(page: Page):
    """통계 정보 실시간 표시 확인"""
    page_content = page.content()
    # "자" 또는 "토큰" 텍스트가 있는지 확인
    assert "자" in page_content or "토큰" in page_content, "통계 정보가 표시되지 않음"
