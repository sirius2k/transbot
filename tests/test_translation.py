"""TranslationManager 클래스 테스트"""
import pytest
from unittest.mock import Mock
from components.translation import TranslationManager


class TestTranslationManager:
    """TranslationManager 클래스 테스트"""

    def setup_method(self):
        """각 테스트 전에 실행"""
        self.mock_client = Mock()
        self.manager = TranslationManager(self.mock_client, model="gpt-4o")

    def test_init_with_defaults(self):
        """기본값으로 초기화 테스트"""
        mock_client = Mock()
        manager = TranslationManager(mock_client)
        assert manager.client == mock_client
        assert manager.model == "gpt-4o-mini"
        assert manager.temperature == 0.3

    def test_init_with_custom_values(self):
        """커스텀 값으로 초기화 테스트"""
        mock_client = Mock()
        manager = TranslationManager(mock_client, model="gpt-4", temperature=0.5)
        assert manager.client == mock_client
        assert manager.model == "gpt-4"
        assert manager.temperature == 0.5

    def test_init_with_invalid_model(self):
        """잘못된 모델로 초기화 시 ValueError 발생 테스트"""
        mock_client = Mock()
        with pytest.raises(ValueError, match="지원하지 않는 모델입니다"):
            TranslationManager(mock_client, model="invalid-model")

    def test_translate_success(self):
        """번역 성공 테스트"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Translated text"

        self.mock_client.chat.completions.create.return_value = mock_response

        result = self.manager.translate("Hello", "English", "Korean")
        assert result == "Translated text"

    def test_translate_calls_api_with_correct_params(self):
        """번역 시 올바른 매개변수로 API 호출하는지 테스트"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "번역된 텍스트"

        self.mock_client.chat.completions.create.return_value = mock_response

        self.manager.translate("Hello", "English", "Korean")

        # API 호출 확인
        self.mock_client.chat.completions.create.assert_called_once()
        call_args = self.mock_client.chat.completions.create.call_args

        # 모델 확인
        assert call_args.kwargs["model"] == "gpt-4o"
        # temperature 확인
        assert call_args.kwargs["temperature"] == 0.3
        # messages 구조 확인
        messages = call_args.kwargs["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "English" in messages[0]["content"]
        assert "Korean" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"

    def test_translate_uses_custom_temperature(self):
        """커스텀 temperature가 번역에 적용되는지 테스트"""
        self.manager.set_temperature(0.7)

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Translated"

        self.mock_client.chat.completions.create.return_value = mock_response

        self.manager.translate("Test", "English", "Korean")

        call_args = self.mock_client.chat.completions.create.call_args
        assert call_args.kwargs["temperature"] == 0.7

    def test_set_model_valid(self):
        """유효한 모델로 변경 테스트"""
        self.manager.set_model("gpt-4-turbo")
        assert self.manager.model == "gpt-4-turbo"

    def test_set_model_invalid(self):
        """잘못된 모델로 변경 시 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="지원하지 않는 모델입니다"):
            self.manager.set_model("invalid-model")

    def test_set_temperature_valid(self):
        """유효한 temperature로 변경 테스트"""
        self.manager.set_temperature(0.5)
        assert self.manager.temperature == 0.5

        self.manager.set_temperature(0.0)
        assert self.manager.temperature == 0.0

        self.manager.set_temperature(1.0)
        assert self.manager.temperature == 1.0

    def test_set_temperature_invalid(self):
        """잘못된 temperature로 변경 시 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="temperature는 0.0에서 1.0 사이여야 합니다"):
            self.manager.set_temperature(-0.1)

        with pytest.raises(ValueError, match="temperature는 0.0에서 1.0 사이여야 합니다"):
            self.manager.set_temperature(1.1)

    def test_get_model_list(self):
        """모델 목록 반환 테스트"""
        models = TranslationManager.get_model_list()
        assert isinstance(models, list)
        assert len(models) == 5
        assert "gpt-4o" in models
        assert "gpt-4o-mini" in models
        assert "gpt-4-turbo" in models
        assert "gpt-4" in models
        assert "gpt-3.5-turbo" in models

    def test_get_model_list_returns_copy(self):
        """모델 목록이 원본과 독립적인지 테스트"""
        models = TranslationManager.get_model_list()
        models.append("custom-model")
        # 원본은 변경되지 않아야 함
        assert "custom-model" not in TranslationManager.SUPPORTED_MODELS

    def test_validate_model_valid(self):
        """유효한 모델 검증 테스트"""
        assert TranslationManager.validate_model("gpt-4o") is True
        assert TranslationManager.validate_model("gpt-4o-mini") is True
        assert TranslationManager.validate_model("gpt-4-turbo") is True
        assert TranslationManager.validate_model("gpt-4") is True
        assert TranslationManager.validate_model("gpt-3.5-turbo") is True

    def test_validate_model_invalid(self):
        """잘못된 모델 검증 테스트"""
        assert TranslationManager.validate_model("invalid-model") is False
        assert TranslationManager.validate_model("") is False
        assert TranslationManager.validate_model("gpt-5") is False
