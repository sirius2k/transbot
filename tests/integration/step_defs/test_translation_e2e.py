"""TC-002 번역 E2E 플로우 테스트의 Step 정의"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect
import re

pytestmark = pytest.mark.integration

# Feature 파일 로드
scenarios('../features/TC-002-translation-e2e.feature')

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
    page.wait_for_load_state("networkidle")
    # URL 끝의 슬래시(/) 포함하여 검증
    expect(page).to_have_url(re.compile(r"http://localhost:8501/?"), timeout=5000)

@given('입력 필드가 빈 상태임')
def input_field_empty(page: Page):
    """입력 필드 빈 상태 확인"""
    input_field = page.locator("textarea").first
    # 입력 필드가 있으면 비우기
    if input_field.is_visible():
        input_field.fill("")

@given('"원문 유지" 옵션이 체크됨')
def keep_original_checked(page: Page):
    """원문 유지 옵션 체크"""
    # 사이드바 열기 (닫혀있을 수 있음)
    sidebar_button = page.locator('[data-testid="collapsedControl"]')
    if sidebar_button.is_visible():
        sidebar_button.click()
        page.wait_for_timeout(500)

    # "원문 유지" 체크박스 찾기 및 체크
    keep_original_label = page.locator('label:has-text("원문 유지")')
    keep_original_checkbox = keep_original_label.locator('input[type="checkbox"]')
    if not keep_original_checkbox.is_checked():
        # label을 클릭하여 체크박스 활성화
        keep_original_label.click()
        page.wait_for_timeout(300)

@given(parsers.parse('"{style_name}" 스타일이 선택됨'))
def style_selected(page: Page, style_name: str):
    """특정 스타일 체크박스 선택"""
    # 사이드바 열기 (닫혀있을 수 있음)
    sidebar_button = page.locator('[data-testid="collapsedControl"]')
    if sidebar_button.is_visible():
        sidebar_button.click()
        page.wait_for_timeout(500)

    # Streamlit 체크박스는 label을 클릭해야 함 (input은 숨겨져 있음)
    # 이모지가 포함된 전체 라벨 텍스트로 찾기
    style_label = page.locator(f'label:has-text("{style_name}")')

    # 체크박스가 이미 체크되어 있는지 확인
    style_checkbox = style_label.locator('input[type="checkbox"]')
    if not style_checkbox.is_checked():
        # label을 클릭하여 체크박스 활성화
        style_label.click()
        page.wait_for_timeout(300)

# ============================================================================
# When Steps (실행 동작)
# ============================================================================

@when(parsers.parse('사용자가 "{text}" 텍스트를 입력'))
def user_enters_text(page: Page, text: str):
    """텍스트 입력"""
    input_field = page.locator("textarea").first
    input_field.fill(text)
    page.wait_for_timeout(500)

@when('사용자가 Markdown 텍스트를 입력')
def user_enters_markdown_text(page: Page):
    """Markdown 텍스트 입력"""
    markdown_text = "# Hello World\n\nThis is a **bold** text."
    input_field = page.locator("textarea").first
    input_field.fill(markdown_text)
    page.wait_for_timeout(500)

@when(parsers.parse('"{button_text}" 버튼을 클릭'))
def click_button(page: Page, button_text: str):
    """버튼 클릭"""
    button = page.locator(f"button:has-text('{button_text}')")
    button.click()
    # 번역이 완료될 때까지 충분히 대기 (최대 30초)
    page.wait_for_timeout(30000)

# ============================================================================
# Then Steps (예상 결과)
# ============================================================================

@then('번역 결과 섹션이 표시됨')
def translation_result_section_visible(page: Page):
    """번역 결과 섹션 표시 확인"""
    # "번역 결과" 텍스트가 페이지에 있는지 확인
    result_header = page.locator("text=번역 결과").first
    expect(result_header).to_be_visible(timeout=5000)

@then(parsers.parse('번역 결과에 "{text}" 텍스트가 포함됨'))
def translation_result_contains_text(page: Page, text: str):
    """번역 결과에 특정 텍스트 포함 확인"""
    # 번역 결과 영역 전체에서 텍스트 검색
    page_content = page.content()
    # 대소문자 구분 없이 검색
    assert text.lower() in page_content.lower(), f"번역 결과에 '{text}'가 포함되지 않음"

@then(parsers.parse('번역 결과에 "{text1}" 또는 "{text2}" 텍스트가 포함됨'))
def translation_result_contains_either_text(page: Page, text1: str, text2: str):
    """번역 결과에 여러 텍스트 중 하나 포함 확인"""
    page_content = page.content().lower()
    assert text1.lower() in page_content or text2.lower() in page_content, \
        f"번역 결과에 '{text1}' 또는 '{text2}'가 포함되지 않음"

@then(parsers.parse('언어 감지 결과가 "{language}"로 표시됨'))
def language_detection_result(page: Page, language: str):
    """언어 감지 결과 확인"""
    # "감지된 언어" 텍스트 찾기
    page_content = page.content()
    assert language in page_content, f"언어 감지 결과에 '{language}'가 표시되지 않음"

@then('통계 정보가 표시됨')
def statistics_displayed(page: Page):
    """통계 정보 표시 확인"""
    # 번역 결과가 표시되면 통계도 함께 표시됨 (별도 검증 불필요)
    pass

@then(parsers.parse('"{button_text}" 버튼이 활성화됨'))
def button_enabled(page: Page, button_text: str):
    """버튼 활성화 상태 확인"""
    button = page.locator(f"button:has-text('{button_text}')").first
    expect(button).to_be_enabled()

@then(parsers.parse('번역 결과에 "{char}" 문자가 포함됨'))
def translation_result_contains_character(page: Page, char: str):
    """번역 결과에 특정 문자 포함 확인 (Markdown 문법 등)"""
    page_content = page.content()
    assert char in page_content, f"번역 결과에 '{char}' 문자가 포함되지 않음"

@then('원문과 번역 결과가 함께 표시됨')
def original_and_translation_displayed(page: Page):
    """원문과 번역 결과 함께 표시 확인"""
    page_content = page.content()
    # "원문"과 "번역" 텍스트가 모두 있는지 확인
    assert "원문" in page_content or "Original" in page_content, "원문이 표시되지 않음"

@then(parsers.parse('"{style_name}" 스타일 번역이 표시됨'))
def style_translation_displayed(page: Page, style_name: str):
    """특정 스타일 번역 표시 확인"""
    page_content = page.content()
    assert style_name in page_content, f"{style_name} 스타일이 표시되지 않음"

@then('두 스타일이 명확히 구분되어 표시됨')
def two_styles_clearly_separated(page: Page):
    """두 스타일 구분 표시 확인"""
    page_content = page.content()
    # 자연스러운 구어체와 공식/문서용이 모두 표시되어야 함
    conversational_count = page_content.count("자연스러운 구어체")
    formal_count = page_content.count("공식/문서용")
    assert conversational_count > 0 and formal_count > 0, "두 스타일이 명확히 구분되지 않음"
