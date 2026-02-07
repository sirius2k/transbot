"""pytest-bdd + Playwright fixtures for integration tests"""
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
