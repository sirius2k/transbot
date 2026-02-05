"""TranslationManager 클래스 테스트"""
import pytest
from unittest.mock import Mock
from components.translation import (
    TranslationManager,
    AzureTranslationManager,
    TranslationManagerFactory
)


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
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 15

        self.mock_client.chat.completions.create.return_value = mock_response

        result = self.manager.translate("Hello", "English", "Korean", "test-session")
        assert result == "Translated text"

    def test_translate_calls_api_with_correct_params(self):
        """번역 시 올바른 매개변수로 API 호출하는지 테스트"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "번역된 텍스트"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 15

        self.mock_client.chat.completions.create.return_value = mock_response

        self.manager.translate("Hello", "English", "Korean", "test-session")

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
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 5

        self.mock_client.chat.completions.create.return_value = mock_response

        self.manager.translate("Test", "English", "Korean", "test-session")

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


class TestAzureTranslationManager:
    """AzureTranslationManager 클래스 테스트"""

    def setup_method(self):
        """각 테스트 전에 실행"""
        self.mock_client = Mock()

    def test_azure_init_with_deployment(self):
        """deployment로 초기화 테스트"""
        manager = AzureTranslationManager(
            self.mock_client,
            deployment="my-gpt4o-deployment"
        )

        assert manager.deployment == "my-gpt4o-deployment"
        assert manager.model == "my-gpt4o-deployment"  # deployment를 기본값으로 사용
        assert manager.client == self.mock_client
        assert manager.temperature == 0.3  # Config 기본값

    def test_azure_init_with_model_and_deployment(self):
        """model과 deployment 동시 초기화 테스트"""
        manager = AzureTranslationManager(
            self.mock_client,
            deployment="my-deployment",
            model="gpt-4o"
        )

        assert manager.deployment == "my-deployment"
        assert manager.model == "gpt-4o"  # model 파라미터 우선

    def test_azure_translate_uses_deployment(self):
        """translate()에서 deployment 사용 확인"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "번역 결과"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 15
        self.mock_client.chat.completions.create.return_value = mock_response

        manager = AzureTranslationManager(
            self.mock_client,
            deployment="my-deployment"
        )

        # 번역 실행
        result = manager.translate("Hello", "English", "Korean", "test-session")

        # deployment가 model 파라미터로 사용되었는지 확인
        self.mock_client.chat.completions.create.assert_called_once()
        call_args = self.mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "my-deployment"
        assert result == "번역 결과"

    def test_azure_translate_success(self):
        """Azure 번역 성공 테스트"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "안녕하세요"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 15
        self.mock_client.chat.completions.create.return_value = mock_response

        manager = AzureTranslationManager(
            self.mock_client,
            deployment="my-gpt4o"
        )

        result = manager.translate("Hello", "English", "Korean", "test-session")
        assert result == "안녕하세요"

    def test_azure_translate_api_params(self):
        """Azure API 호출 파라미터 검증"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "번역됨"
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 5
        self.mock_client.chat.completions.create.return_value = mock_response

        manager = AzureTranslationManager(
            self.mock_client,
            deployment="my-deployment",
            temperature=0.5,
            max_tokens=5000
        )

        manager.translate("Test", "English", "Korean", "test-session")

        # API 호출 파라미터 검증
        call_args = self.mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "my-deployment"
        assert call_args.kwargs["temperature"] == 0.5
        assert call_args.kwargs["max_tokens"] == 5000

    def test_azure_load_deployments_empty(self, monkeypatch):
        """빈 deployment 로드 테스트"""
        from config import Config

        # 빈 AZURE_DEPLOYMENTS 설정
        monkeypatch.setenv("AZURE_DEPLOYMENTS", "")

        config = Config.load()
        AzureTranslationManager.load_deployments(config)

        assert AzureTranslationManager.SUPPORTED_DEPLOYMENTS == {}

    def test_azure_load_deployments_valid(self, monkeypatch):
        """정상 deployment 로드 테스트"""
        from config import Config

        # deployment 문자열 설정
        monkeypatch.setenv("AZURE_DEPLOYMENTS", "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini")

        config = Config.load()
        AzureTranslationManager.load_deployments(config)

        assert "gpt-4o" in AzureTranslationManager.SUPPORTED_DEPLOYMENTS
        assert "gpt-4o-mini" in AzureTranslationManager.SUPPORTED_DEPLOYMENTS
        assert AzureTranslationManager.SUPPORTED_DEPLOYMENTS["gpt-4o"] == "my-gpt4o"
        assert AzureTranslationManager.SUPPORTED_DEPLOYMENTS["gpt-4o-mini"] == "my-mini"

    def test_azure_validate_deployment_valid(self, monkeypatch):
        """유효한 deployment 검증"""
        from config import Config

        monkeypatch.setenv("AZURE_DEPLOYMENTS", "gpt-4o:my-deployment")
        config = Config.load()
        AzureTranslationManager.load_deployments(config)

        assert AzureTranslationManager.validate_deployment("my-deployment") is True

    def test_azure_validate_deployment_invalid(self, monkeypatch):
        """무효한 deployment 검증"""
        from config import Config

        monkeypatch.setenv("AZURE_DEPLOYMENTS", "gpt-4o:my-deployment")
        config = Config.load()
        AzureTranslationManager.load_deployments(config)

        assert AzureTranslationManager.validate_deployment("invalid-deployment") is False


class TestTranslationManagerFactory:
    """TranslationManagerFactory 클래스 테스트"""

    def setup_method(self):
        """각 테스트 전에 실행"""
        self.mock_client = Mock()

    def test_factory_create_openai(self):
        """Factory로 OpenAI Manager 생성 테스트"""
        manager = TranslationManagerFactory.create(
            "openai",
            self.mock_client,
            model="gpt-4o"
        )

        assert isinstance(manager, TranslationManager)
        assert not isinstance(manager, AzureTranslationManager)
        assert manager.model == "gpt-4o"

    def test_factory_create_azure(self):
        """Factory로 Azure Manager 생성 테스트"""
        manager = TranslationManagerFactory.create(
            "azure",
            self.mock_client,
            deployment="my-deployment"
        )

        assert isinstance(manager, AzureTranslationManager)
        assert manager.deployment == "my-deployment"

    def test_factory_create_azure_with_deployment(self):
        """Factory + deployment 파라미터 테스트"""
        manager = TranslationManagerFactory.create(
            "azure",
            self.mock_client,
            deployment="custom-deployment",
            model="gpt-4o",
            temperature=0.7
        )

        assert isinstance(manager, AzureTranslationManager)
        assert manager.deployment == "custom-deployment"
        assert manager.model == "gpt-4o"
        assert manager.temperature == 0.7
