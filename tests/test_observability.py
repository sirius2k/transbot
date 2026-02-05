"""configure_langfuse 함수 테스트"""
import pytest
from unittest.mock import Mock, patch

from components.observability import configure_langfuse
from config import Config


@pytest.fixture
def mock_config_enabled():
    """Langfuse 활성화된 Config Mock"""
    config = Mock(spec=Config)
    config.LANGFUSE_PUBLIC_KEY = "pk-test"
    config.LANGFUSE_SECRET_KEY = "sk-test"
    config.LANGFUSE_HOST = "http://localhost:3000"
    config.langfuse_enabled = True
    return config


@pytest.fixture
def mock_config_disabled():
    """Langfuse 비활성화된 Config Mock"""
    config = Mock(spec=Config)
    config.langfuse_enabled = False
    return config


class TestConfigureLangfuse:
    """configure_langfuse 함수 테스트"""

    @patch('components.observability.langfuse_context')
    def test_configure_success(self, mock_context, mock_config_enabled):
        """정상 설정 테스트"""
        result = configure_langfuse(mock_config_enabled)

        assert result is True
        mock_context.configure.assert_called_once_with(
            public_key="pk-test",
            secret_key="sk-test",
            host="http://localhost:3000",
            timeout=5,
            enabled=True,
        )

    @patch('components.observability.langfuse_context')
    def test_configure_disabled(self, mock_context, mock_config_disabled):
        """비활성화 시 enabled=False 설정 테스트"""
        result = configure_langfuse(mock_config_disabled)

        assert result is False
        mock_context.configure.assert_called_once_with(enabled=False)

    @patch('components.observability.langfuse_context')
    def test_configure_failure_graceful_degradation(self, mock_context, mock_config_enabled):
        """초기화 실패 시 graceful degradation 테스트"""
        mock_context.configure.side_effect = [
            Exception("Connection failed"),
            None,
        ]

        result = configure_langfuse(mock_config_enabled)

        assert result is False
        assert mock_context.configure.call_count == 2
        second_call = mock_context.configure.call_args_list[1]
        assert second_call.kwargs == {"enabled": False}