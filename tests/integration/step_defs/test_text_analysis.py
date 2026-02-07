"""TC-003 텍스트 분석 및 통계 테스트의 Step 정의"""
import pytest
import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-003-text-analysis.feature')

# ============================================================================
# Given Steps (전제 조건) - TC-002에서 재사용
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

@when('입력 필드를 비움')
def user_clears_input(page: Page):
    """입력 필드 비우기"""
    input_field = page.locator("textarea").first
    input_field.fill("")
    # 통계 업데이트를 위해 잠시 대기
    page.wait_for_timeout(1000)

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then('통계 정보가 실시간으로 표시됨')
def statistics_displayed_realtime(page: Page):
    """통계 정보 실시간 표시 확인"""
    page_content = page.content()
    # "자" 또는 "토큰" 텍스트가 있는지 확인
    assert "자" in page_content or "토큰" in page_content, "통계 정보가 표시되지 않음"

@then(parsers.parse('글자 수 "{count}"이 표시됨'))
def character_count_displayed(page: Page, count: str):
    """특정 글자 수가 표시되는지 확인"""
    page_content = page.content()
    # "28"과 "자"가 모두 페이지에 있는지 확인
    assert count in page_content, f"글자 수 '{count}'이 표시되지 않음"
    assert "자" in page_content, "글자 수 단위 '자'가 표시되지 않음"

@then('토큰 수가 표시됨')
def token_count_displayed(page: Page):
    """토큰 수가 표시되는지 확인"""
    page_content = page.content()
    assert "토큰" in page_content, "토큰 수가 표시되지 않음"

@then(parsers.parse('"{text}" 텍스트가 표시됨'))
def text_displayed(page: Page, text: str):
    """특정 텍스트가 표시되는지 확인"""
    page_content = page.content()
    assert text in page_content, f"'{text}' 텍스트가 표시되지 않음"
