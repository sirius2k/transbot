"""테스트 공통 설정"""
import pytest


@pytest.fixture(autouse=True)
def disable_langfuse():
    """모든 테스트에서 Langfuse를 비활성화합니다.

    @observe 데코레이터가 no-op으로 동작하도록 하여
    테스트 실행 시 Langfuse 서버 연결 없이 정상 동작합니다.
    """
    from langfuse.decorators import langfuse_context
    langfuse_context.configure(enabled=False)
    yield