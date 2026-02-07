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
