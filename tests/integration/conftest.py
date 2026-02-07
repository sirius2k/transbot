"""pytest-bdd + Playwright fixtures for integration tests"""
import pytest
from playwright.sync_api import Browser, Page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """브라우저 컨텍스트 설정"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture
def page(browser: Browser) -> Page:
    """각 테스트마다 새로운 페이지 생성"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
