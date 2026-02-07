"""간단한 Smoke 테스트 (pytest-bdd 없이)"""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.integration

def test_app_loads(page: Page):
    """앱이 로드되는지 확인"""
    page.goto("http://localhost:8501")
    expect(page).to_have_title("TransBot", timeout=10000)

def test_title_visible(page: Page):
    """타이틀이 표시되는지 확인"""
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    expect(page.locator("h1")).to_contain_text("TransBot")

def test_input_field_exists(page: Page):
    """입력 필드가 존재하는지 확인"""
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    expect(page.locator("textarea")).to_be_visible()
