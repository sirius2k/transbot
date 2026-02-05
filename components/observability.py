"""LLM 관찰성 모듈

Langfuse @observe 데코레이터를 통한 LLM 사용 추적 및 모니터링 기능을 제공합니다.
"""

import logging

from langfuse.decorators import langfuse_context

from config import Config

logger = logging.getLogger("transbot.observability")


def configure_langfuse(config: Config) -> bool:
    """Langfuse 클라이언트를 설정합니다.

    Config의 환경 변수를 기반으로 langfuse_context를 구성합니다.
    Langfuse가 비활성화되어 있거나 설정에 실패한 경우,
    enabled=False로 설정하여 모든 @observe 데코레이터가 no-op으로 동작합니다.

    Args:
        config: Config 객체

    Returns:
        bool: Langfuse 활성화 여부
    """
    if not config.langfuse_enabled:
        langfuse_context.configure(enabled=False)
        return False

    try:
        langfuse_context.configure(
            public_key=config.LANGFUSE_PUBLIC_KEY,
            secret_key=config.LANGFUSE_SECRET_KEY,
            host=config.LANGFUSE_HOST,
            timeout=5,
            enabled=True,
        )
        return True
    except Exception as e:
        logger.warning("Langfuse 초기화 실패 (추적 비활성화)", extra={
            "error_type": type(e).__name__,
            "error_message": str(e)
        }, exc_info=True)
        langfuse_context.configure(enabled=False)
        return False