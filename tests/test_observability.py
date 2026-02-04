"""LangfuseObserver 클래스 테스트"""
import pytest
from unittest.mock import Mock, patch

from components.observability import LangfuseObserver
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


class TestLangfuseObserverInit:
    """LangfuseObserver 초기화 테스트"""

    @patch('components.observability.Langfuse')
    def test_langfuse_observer_init_success(self, mock_langfuse, mock_config_enabled):
        """정상 초기화 테스트"""
        mock_instance = Mock()
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)

        assert observer._client is not None
        assert observer._init_failed is False
        mock_langfuse.assert_called_once_with(
            public_key="pk-test",
            secret_key="sk-test",
            host="http://localhost:3000",
            timeout=5
        )

    def test_langfuse_observer_disabled(self, mock_config_disabled):
        """비활성화 시 초기화 건너뜀 테스트"""
        observer = LangfuseObserver(mock_config_disabled)

        assert observer._client is None
        assert observer._init_failed is False

    @patch('components.observability.Langfuse')
    @patch('builtins.print')
    def test_langfuse_init_failure(self, mock_print, mock_langfuse, mock_config_enabled):
        """초기화 실패 시 graceful degradation 테스트"""
        mock_langfuse.side_effect = Exception("Connection failed")

        observer = LangfuseObserver(mock_config_enabled)

        assert observer._client is None
        assert observer._init_failed is True
        mock_print.assert_called_once()
        assert "Langfuse 초기화 실패" in str(mock_print.call_args)


class TestLangfuseObserverTrackTranslation:
    """LangfuseObserver.track_translation 테스트"""

    @patch('components.observability.Langfuse')
    def test_track_translation_success(self, mock_langfuse, mock_config_enabled):
        """정상 추적 테스트"""
        mock_instance = Mock()
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)
        observer.track_translation(
            source_text="Hello",
            target_text="안녕하세요",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=15,
            latency_ms=500.5,
            session_id="test-session"
        )

        mock_instance.trace.assert_called_once_with(
            name="translation",
            input={
                "source_text": "Hello",
                "source_lang": "en",
                "target_lang": "ko",
            },
            output={"target_text": "안녕하세요"},
            metadata={
                "model": "gpt-4o-mini",
                "direction": "en→ko",
                "session_id": "test-session",
                "latency_ms": 500.5,
            },
            usage={
                "input": 10,
                "output": 15,
                "total": 25,
            },
            level="DEFAULT",
            status_message=None,
        )

    @patch('components.observability.Langfuse')
    def test_track_translation_with_error(self, mock_langfuse, mock_config_enabled):
        """에러 포함 추적 테스트"""
        mock_instance = Mock()
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)
        observer.track_translation(
            source_text="Hello",
            target_text="",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=0,
            latency_ms=100.0,
            session_id="test-session",
            error="API rate limit exceeded"
        )

        mock_instance.trace.assert_called_once()
        call_kwargs = mock_instance.trace.call_args.kwargs
        assert call_kwargs["level"] == "ERROR"
        assert call_kwargs["status_message"] == "API rate limit exceeded"

    @patch('components.observability.Langfuse')
    @patch('builtins.print')
    def test_track_translation_failure(self, mock_print, mock_langfuse, mock_config_enabled):
        """추적 실패 시 no-op 테스트"""
        mock_instance = Mock()
        mock_instance.trace.side_effect = Exception("Network error")
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)

        # 예외가 발생해도 애플리케이션은 정상 동작
        observer.track_translation(
            source_text="Hello",
            target_text="안녕하세요",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=15,
            latency_ms=500.5,
            session_id="test-session"
        )

        mock_print.assert_called_once()
        assert "Langfuse 추적 실패" in str(mock_print.call_args)

    @patch('components.observability.Langfuse')
    @patch('builtins.print')
    def test_track_translation_timeout(self, mock_print, mock_langfuse, mock_config_enabled):
        """타임아웃 발생 시 처리 테스트"""
        mock_instance = Mock()
        mock_instance.trace.side_effect = TimeoutError("Request timeout")
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)
        observer.track_translation(
            source_text="Hello",
            target_text="안녕하세요",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=15,
            latency_ms=500.5,
            session_id="test-session"
        )

        mock_print.assert_called_once()
        assert "Langfuse 전송 타임아웃" in str(mock_print.call_args)

    def test_track_translation_when_disabled(self, mock_config_disabled):
        """비활성화 시 no-op 테스트"""
        observer = LangfuseObserver(mock_config_disabled)

        # 클라이언트가 None이어도 예외 발생하지 않음
        observer.track_translation(
            source_text="Hello",
            target_text="안녕하세요",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=15,
            latency_ms=500.5,
            session_id="test-session"
        )

    @patch('components.observability.Langfuse')
    def test_track_translation_when_init_failed(self, mock_langfuse, mock_config_enabled):
        """초기화 실패 후 no-op 테스트"""
        mock_langfuse.side_effect = Exception("Init failed")

        observer = LangfuseObserver(mock_config_enabled)
        assert observer._init_failed is True

        # 초기화 실패 후에도 추적 호출 가능 (no-op)
        observer.track_translation(
            source_text="Hello",
            target_text="안녕하세요",
            source_lang="en",
            target_lang="ko",
            model="gpt-4o-mini",
            input_tokens=10,
            output_tokens=15,
            latency_ms=500.5,
            session_id="test-session"
        )


class TestLangfuseObserverFlush:
    """LangfuseObserver.flush 테스트"""

    @patch('components.observability.Langfuse')
    def test_flush_success(self, mock_langfuse, mock_config_enabled):
        """정상 flush 테스트"""
        mock_instance = Mock()
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)
        observer.flush()

        mock_instance.flush.assert_called_once()

    @patch('components.observability.Langfuse')
    @patch('builtins.print')
    def test_flush_failure(self, mock_print, mock_langfuse, mock_config_enabled):
        """flush 실패 시 no-op 테스트"""
        mock_instance = Mock()
        mock_instance.flush.side_effect = Exception("Flush failed")
        mock_langfuse.return_value = mock_instance

        observer = LangfuseObserver(mock_config_enabled)
        observer.flush()

        mock_print.assert_called_once()
        assert "Langfuse flush 실패" in str(mock_print.call_args)

    def test_flush_when_client_none(self, mock_config_disabled):
        """클라이언트 없을 때 no-op 테스트"""
        observer = LangfuseObserver(mock_config_disabled)

        # 클라이언트가 None이어도 예외 발생하지 않음
        observer.flush()
