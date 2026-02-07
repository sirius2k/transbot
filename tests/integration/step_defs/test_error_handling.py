"""TC-006 에러 핸들링 테스트의 Step 정의"""
import pytest
import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-006-error-handling.feature')

# ============================================================================
# Given Steps (전제 조건) - 재사용
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

@when(parsers.parse('사용자가 {length:d}자의 매우 긴 텍스트를 입력'))
def user_enters_very_long_text(page: Page, length: int):
    """매우 긴 텍스트 입력 (길이 초과)"""
    long_text = "A" * length
    input_field = page.locator("textarea").first
    input_field.fill(long_text)
    # 에러 메시지 표시를 위해 대기
    page.wait_for_timeout(1500)

@when(parsers.parse('사용자가 {length:d}자의 긴 텍스트를 입력'))
def user_enters_long_text(page: Page, length: int):
    """긴 텍스트 입력 (경고 수준)"""
    long_text = "B" * length
    input_field = page.locator("textarea").first
    input_field.fill(long_text)
    # 경고 메시지 표시를 위해 대기
    page.wait_for_timeout(1500)

@when('모든 스타일 체크박스를 해제')
def deselect_all_styles(page: Page):
    """모든 스타일 체크박스 해제"""
    # 주요 스타일 체크박스들의 텍스트 목록
    style_labels = [
        "직역/축자",
        "자연스러운 구어체",
        "비즈니스/업무용",
        "공식/문서용",
        "간결체"
    ]

    for style_label in style_labels:
        try:
            checkbox_label = page.locator(f'label:has-text("{style_label}")').first
            if checkbox_label.is_visible(timeout=1000):
                checkbox_input = checkbox_label.locator('input[type="checkbox"]')
                if checkbox_input.is_checked():
                    checkbox_label.click()
                    page.wait_for_timeout(300)
        except Exception:
            # 일부 체크박스가 없을 수 있으므로 무시
            continue

    # 추가 대기 (경고 메시지 표시)
    page.wait_for_timeout(500)

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then(parsers.parse('"{error_text}" 에러 메시지가 표시됨'))
def error_message_displayed(page: Page, error_text: str):
    """에러 메시지 표시 확인"""
    page_content = page.content()
    assert error_text in page_content, f"'{error_text}' 에러 메시지가 표시되지 않음"

@then(parsers.parse('"{warning_text}" 경고 메시지가 표시됨'))
def warning_message_displayed(page: Page, warning_text: str):
    """경고 메시지 표시 확인"""
    page_content = page.content()
    assert warning_text in page_content, f"'{warning_text}' 경고 메시지가 표시되지 않음"
