"""TC-005 설정 관리 테스트의 Step 정의"""
import pytest
import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-005-settings-config.feature')

# ============================================================================
# Given Steps (전제 조건) - TC-004에서 재사용
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

@when(parsers.parse('"{checkbox_text}" 체크박스를 해제'))
def deselect_checkbox(page: Page, checkbox_text: str):
    """체크박스 해제"""
    checkbox_label = page.locator(f'label:has-text("{checkbox_text}")')

    # 체크박스가 선택되어 있으면 해제
    checkbox_input = checkbox_label.locator('input[type="checkbox"]')
    if checkbox_input.is_checked():
        # label을 클릭하여 체크박스 비활성화
        checkbox_label.click()
        page.wait_for_timeout(500)

@when(parsers.parse('커스텀 스타일 입력 필드에 "{text}" 입력'))
def enter_custom_style_text(page: Page, text: str):
    """커스텀 스타일 입력 필드에 텍스트 입력"""
    # 커스텀 스타일 입력 필드 찾기 (placeholder 또는 key 기반)
    custom_input = page.locator('textarea').nth(1)  # 두 번째 textarea (첫 번째는 메인 입력)
    custom_input.fill(text)
    page.wait_for_timeout(500)

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then(parsers.parse('"{checkbox_text}" 체크박스가 선택됨'))
def checkbox_selected(page: Page, checkbox_text: str):
    """체크박스가 선택되었는지 확인"""
    # 이모지 제거하고 핵심 텍스트만 사용
    core_text = checkbox_text.replace("🏷️ ", "").replace("✍️ ", "")
    checkbox_label = page.locator(f'label:has-text("{core_text}")')
    checkbox_input = checkbox_label.locator('input[type="checkbox"]')
    expect(checkbox_input).to_be_checked()

@then(parsers.parse('"{checkbox_text}" 체크박스가 해제됨'))
def checkbox_unchecked(page: Page, checkbox_text: str):
    """체크박스가 해제되었는지 확인"""
    checkbox_label = page.locator(f'label:has-text("{checkbox_text}")')
    checkbox_input = checkbox_label.locator('input[type="checkbox"]')
    expect(checkbox_input).not_to_be_checked()

@then('커스텀 스타일 입력 필드가 표시됨')
def custom_style_input_visible(page: Page):
    """커스텀 스타일 입력 필드 표시 확인"""
    # 두 번째 textarea가 커스텀 스타일 입력 필드
    custom_input = page.locator('textarea').nth(1)
    expect(custom_input).to_be_visible()

@then(parsers.parse('입력 필드에 "{text}" 텍스트가 표시됨'))
def input_field_contains_text(page: Page, text: str):
    """입력 필드에 텍스트가 표시되는지 확인"""
    # 두 번째 textarea 확인 (커스텀 스타일)
    custom_input = page.locator('textarea').nth(1)
    expect(custom_input).to_have_value(text)
