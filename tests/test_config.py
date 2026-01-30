"""Config 클래스 테스트"""
import pytest
import os
from config import Config


class TestConfigInit:
    """Config 초기화 테스트"""

    def test_init_default_values(self):
        """기본값으로 초기화 테스트"""
        config = Config()

        # OpenAI API 설정
        assert config.OPENAI_API_KEY is None
        assert config.OPENAI_API_TIMEOUT == 60
        assert config.OPENAI_MAX_RETRIES == 3

        # AI 모델 설정
        assert config.DEFAULT_MODEL == "gpt-4o-mini"
        assert config.DEFAULT_TEMPERATURE == 0.3
        assert config.MAX_TOKENS == 4000

        # 언어 감지 설정
        assert config.LANGUAGE_DETECTION_THRESHOLD == 0.5

        # 애플리케이션 설정
        assert config.APP_TITLE == "영어-한국어 번역기"
        assert config.APP_ICON == "🌐"
        assert config.APP_LAYOUT == "centered"

        # UI 설정
        assert config.TEXT_AREA_HEIGHT == 200
        assert config.MAX_INPUT_LENGTH == 50000


class TestConfigLoad:
    """Config.load() 메서드 테스트"""

    def test_load_with_no_env_vars(self, monkeypatch):
        """환경 변수가 없을 때 기본값 사용 테스트

        주의: .env 파일이 존재하는 경우 load_dotenv()가 자동으로 로드하므로
        실제로는 .env 파일의 값이 사용될 수 있습니다.
        """
        # 모든 관련 환경 변수 제거 (OPENAI_API_KEY 제외 - .env 파일에서 로드됨)
        for key in [
            "OPENAI_API_TIMEOUT",
            "OPENAI_MAX_RETRIES",
            "DEFAULT_MODEL",
            "DEFAULT_TEMPERATURE",
            "MAX_TOKENS",
            "LANGUAGE_DETECTION_THRESHOLD",
            "APP_TITLE",
            "APP_ICON",
            "APP_LAYOUT",
            "TEXT_AREA_HEIGHT",
            "MAX_INPUT_LENGTH"
        ]:
            monkeypatch.delenv(key, raising=False)

        config = Config.load()

        # 모든 값이 기본값이어야 함
        # 단, .env 파일에 설정된 값이 있으면 그 값이 우선됨
        assert config.OPENAI_API_TIMEOUT == 60
        assert config.OPENAI_MAX_RETRIES == 3
        assert config.DEFAULT_MODEL == "gpt-4o-mini"
        assert config.DEFAULT_TEMPERATURE == 0.3
        assert config.MAX_TOKENS == 4000
        assert config.LANGUAGE_DETECTION_THRESHOLD == 0.5
        # .env 파일에 APP_TITLE=TransBot이 설정되어 있음
        assert config.APP_TITLE == "TransBot"
        assert config.APP_ICON == "🌐"
        assert config.APP_LAYOUT == "centered"
        assert config.TEXT_AREA_HEIGHT == 200
        assert config.MAX_INPUT_LENGTH == 50000

    def test_load_with_env_vars(self, monkeypatch):
        """환경 변수가 설정되어 있을 때 로드 테스트"""
        # 환경 변수 설정
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key_123")
        monkeypatch.setenv("OPENAI_API_TIMEOUT", "120")
        monkeypatch.setenv("OPENAI_MAX_RETRIES", "5")
        monkeypatch.setenv("DEFAULT_MODEL", "gpt-4o")
        monkeypatch.setenv("DEFAULT_TEMPERATURE", "0.5")
        monkeypatch.setenv("MAX_TOKENS", "8000")
        monkeypatch.setenv("LANGUAGE_DETECTION_THRESHOLD", "0.7")
        monkeypatch.setenv("APP_TITLE", "Custom Translator")
        monkeypatch.setenv("APP_ICON", "🔥")
        monkeypatch.setenv("APP_LAYOUT", "wide")
        monkeypatch.setenv("TEXT_AREA_HEIGHT", "300")
        monkeypatch.setenv("MAX_INPUT_LENGTH", "100000")

        config = Config.load()

        # 환경 변수 값이 적용되어야 함
        assert config.OPENAI_API_KEY == "test_api_key_123"
        assert config.OPENAI_API_TIMEOUT == 120
        assert config.OPENAI_MAX_RETRIES == 5
        assert config.DEFAULT_MODEL == "gpt-4o"
        assert config.DEFAULT_TEMPERATURE == 0.5
        assert config.MAX_TOKENS == 8000
        assert config.LANGUAGE_DETECTION_THRESHOLD == 0.7
        assert config.APP_TITLE == "Custom Translator"
        assert config.APP_ICON == "🔥"
        assert config.APP_LAYOUT == "wide"
        assert config.TEXT_AREA_HEIGHT == 300
        assert config.MAX_INPUT_LENGTH == 100000

    def test_load_with_partial_env_vars(self, monkeypatch):
        """일부 환경 변수만 설정되어 있을 때 테스트"""
        # 일부만 설정
        monkeypatch.setenv("DEFAULT_MODEL", "gpt-4")
        monkeypatch.setenv("APP_TITLE", "My Translator")
        # 나머지는 제거
        for key in [
            "OPENAI_API_TIMEOUT",
            "OPENAI_MAX_RETRIES",
            "DEFAULT_TEMPERATURE",
            "MAX_TOKENS",
            "LANGUAGE_DETECTION_THRESHOLD",
            "APP_ICON",
            "APP_LAYOUT",
            "TEXT_AREA_HEIGHT",
            "MAX_INPUT_LENGTH"
        ]:
            monkeypatch.delenv(key, raising=False)

        config = Config.load()

        # 설정된 값은 환경 변수 값, 나머지는 기본값
        assert config.DEFAULT_MODEL == "gpt-4"
        assert config.APP_TITLE == "My Translator"
        assert config.OPENAI_API_TIMEOUT == 60  # 기본값
        assert config.DEFAULT_TEMPERATURE == 0.3  # 기본값
        assert config.APP_ICON == "🌐"  # 기본값


class TestConfigTypeConversion:
    """타입 변환 테스트"""

    def test_get_int_env_valid(self, monkeypatch):
        """정수 환경 변수 변환 성공 테스트"""
        monkeypatch.setenv("TEST_INT", "123")
        result = Config._get_int_env("TEST_INT", 999)
        assert result == 123
        assert isinstance(result, int)

    def test_get_int_env_default(self, monkeypatch):
        """정수 환경 변수가 없을 때 기본값 반환 테스트"""
        monkeypatch.delenv("TEST_INT", raising=False)
        result = Config._get_int_env("TEST_INT", 999)
        assert result == 999

    def test_get_int_env_invalid(self, monkeypatch):
        """정수 환경 변수 변환 실패 테스트"""
        monkeypatch.setenv("TEST_INT", "not_a_number")
        with pytest.raises(ValueError, match="정수여야 합니다"):
            Config._get_int_env("TEST_INT", 999)

    def test_get_float_env_valid(self, monkeypatch):
        """실수 환경 변수 변환 성공 테스트"""
        monkeypatch.setenv("TEST_FLOAT", "3.14")
        result = Config._get_float_env("TEST_FLOAT", 1.0)
        assert result == 3.14
        assert isinstance(result, float)

    def test_get_float_env_default(self, monkeypatch):
        """실수 환경 변수가 없을 때 기본값 반환 테스트"""
        monkeypatch.delenv("TEST_FLOAT", raising=False)
        result = Config._get_float_env("TEST_FLOAT", 1.0)
        assert result == 1.0

    def test_get_float_env_invalid(self, monkeypatch):
        """실수 환경 변수 변환 실패 테스트"""
        monkeypatch.setenv("TEST_FLOAT", "not_a_float")
        with pytest.raises(ValueError, match="실수여야 합니다"):
            Config._get_float_env("TEST_FLOAT", 1.0)

    def test_get_str_env_valid(self, monkeypatch):
        """문자열 환경 변수 반환 테스트"""
        monkeypatch.setenv("TEST_STR", "hello")
        result = Config._get_str_env("TEST_STR", "default")
        assert result == "hello"
        assert isinstance(result, str)

    def test_get_str_env_default(self, monkeypatch):
        """문자열 환경 변수가 없을 때 기본값 반환 테스트"""
        monkeypatch.delenv("TEST_STR", raising=False)
        result = Config._get_str_env("TEST_STR", "default")
        assert result == "default"


class TestConfigValidation:
    """검증 메서드 테스트"""

    def test_validate_model_valid(self):
        """유효한 모델 검증 테스트"""
        # 예외가 발생하지 않아야 함
        Config._validate_model("gpt-4o")
        Config._validate_model("gpt-4o-mini")
        Config._validate_model("gpt-4-turbo")
        Config._validate_model("gpt-4")
        Config._validate_model("gpt-3.5-turbo")

    def test_validate_model_invalid(self):
        """유효하지 않은 모델 검증 테스트"""
        with pytest.raises(ValueError, match="지원하지 않는 모델입니다"):
            Config._validate_model("invalid-model")

    def test_validate_temperature_valid(self):
        """유효한 temperature 검증 테스트"""
        Config._validate_temperature(0.0)
        Config._validate_temperature(0.5)
        Config._validate_temperature(1.0)

    def test_validate_temperature_too_low(self):
        """temperature가 너무 낮을 때 검증 테스트"""
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config._validate_temperature(-0.1)

    def test_validate_temperature_too_high(self):
        """temperature가 너무 높을 때 검증 테스트"""
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config._validate_temperature(1.1)

    def test_validate_threshold_valid(self):
        """유효한 임계값 검증 테스트"""
        Config._validate_threshold(0.0)
        Config._validate_threshold(0.5)
        Config._validate_threshold(1.0)

    def test_validate_threshold_too_low(self):
        """임계값이 너무 낮을 때 검증 테스트"""
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config._validate_threshold(-0.1)

    def test_validate_threshold_too_high(self):
        """임계값이 너무 높을 때 검증 테스트"""
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config._validate_threshold(1.1)

    def test_validate_layout_valid(self):
        """유효한 레이아웃 검증 테스트"""
        Config._validate_layout("centered")
        Config._validate_layout("wide")

    def test_validate_layout_invalid(self):
        """유효하지 않은 레이아웃 검증 테스트"""
        with pytest.raises(ValueError, match="지원하지 않는 레이아웃 모드입니다"):
            Config._validate_layout("invalid-layout")


class TestConfigIntegration:
    """통합 테스트"""

    def test_load_with_invalid_model(self, monkeypatch):
        """잘못된 모델로 로드 시 검증 실패 테스트"""
        monkeypatch.setenv("DEFAULT_MODEL", "invalid-model")
        with pytest.raises(ValueError, match="지원하지 않는 모델입니다"):
            Config.load()

    def test_load_with_invalid_temperature(self, monkeypatch):
        """잘못된 temperature로 로드 시 검증 실패 테스트"""
        monkeypatch.setenv("DEFAULT_TEMPERATURE", "1.5")
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config.load()

    def test_load_with_invalid_threshold(self, monkeypatch):
        """잘못된 임계값으로 로드 시 검증 실패 테스트"""
        monkeypatch.setenv("LANGUAGE_DETECTION_THRESHOLD", "-0.5")
        with pytest.raises(ValueError, match="0.0에서 1.0 사이여야 합니다"):
            Config.load()

    def test_load_with_invalid_layout(self, monkeypatch):
        """잘못된 레이아웃으로 로드 시 검증 실패 테스트"""
        monkeypatch.setenv("APP_LAYOUT", "invalid")
        with pytest.raises(ValueError, match="지원하지 않는 레이아웃 모드입니다"):
            Config.load()

    def test_load_with_invalid_int_type(self, monkeypatch):
        """정수 타입이어야 하는 환경 변수에 문자열 설정 시 테스트"""
        monkeypatch.setenv("OPENAI_API_TIMEOUT", "not_a_number")
        with pytest.raises(ValueError, match="정수여야 합니다"):
            Config.load()

    def test_load_with_invalid_float_type(self, monkeypatch):
        """실수 타입이어야 하는 환경 변수에 문자열 설정 시 테스트"""
        monkeypatch.setenv("DEFAULT_TEMPERATURE", "not_a_float")
        with pytest.raises(ValueError, match="실수여야 합니다"):
            Config.load()

    def test_load_with_all_valid_custom_values(self, monkeypatch):
        """모든 커스텀 값이 유효할 때 로드 성공 테스트"""
        # 모든 환경 변수를 유효한 값으로 설정
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
        monkeypatch.setenv("OPENAI_API_TIMEOUT", "90")
        monkeypatch.setenv("OPENAI_MAX_RETRIES", "5")
        monkeypatch.setenv("DEFAULT_MODEL", "gpt-4")
        monkeypatch.setenv("DEFAULT_TEMPERATURE", "0.7")
        monkeypatch.setenv("MAX_TOKENS", "6000")
        monkeypatch.setenv("LANGUAGE_DETECTION_THRESHOLD", "0.6")
        monkeypatch.setenv("APP_TITLE", "Custom App")
        monkeypatch.setenv("APP_ICON", "🚀")
        monkeypatch.setenv("APP_LAYOUT", "wide")
        monkeypatch.setenv("TEXT_AREA_HEIGHT", "250")
        monkeypatch.setenv("MAX_INPUT_LENGTH", "75000")

        config = Config.load()

        # 모든 값이 설정한 대로 로드되어야 함
        assert config.OPENAI_API_KEY == "sk-test123"
        assert config.OPENAI_API_TIMEOUT == 90
        assert config.OPENAI_MAX_RETRIES == 5
        assert config.DEFAULT_MODEL == "gpt-4"
        assert config.DEFAULT_TEMPERATURE == 0.7
        assert config.MAX_TOKENS == 6000
        assert config.LANGUAGE_DETECTION_THRESHOLD == 0.6
        assert config.APP_TITLE == "Custom App"
        assert config.APP_ICON == "🚀"
        assert config.APP_LAYOUT == "wide"
        assert config.TEXT_AREA_HEIGHT == 250
        assert config.MAX_INPUT_LENGTH == 75000


class TestConfigAzure:
    """Config 클래스 Azure 설정 테스트"""

    def test_init_azure_default_values(self):
        """Azure 기본값 초기화 테스트"""
        config = Config()

        # Azure OpenAI 설정 기본값
        assert config.AI_PROVIDER == "openai"
        assert config.AZURE_OPENAI_API_KEY is None
        assert config.AZURE_OPENAI_ENDPOINT is None
        assert config.AZURE_OPENAI_API_VERSION == "2024-02-15-preview"
        assert config.AZURE_DEPLOYMENTS is None

    def test_load_with_azure_provider(self, monkeypatch):
        """AI_PROVIDER=azure 로드 테스트"""
        monkeypatch.setenv("AI_PROVIDER", "azure")
        monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-azure-key")
        monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
        monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        monkeypatch.setenv("AZURE_DEPLOYMENTS", "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini")

        config = Config.load()

        assert config.AI_PROVIDER == "azure"
        assert config.AZURE_OPENAI_API_KEY == "test-azure-key"
        assert config.AZURE_OPENAI_ENDPOINT == "https://test.openai.azure.com/"
        assert config.AZURE_OPENAI_API_VERSION == "2024-02-15-preview"
        assert config.AZURE_DEPLOYMENTS == "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini"

    def test_load_with_openai_provider_default(self, monkeypatch):
        """AI_PROVIDER 미설정 시 openai 기본값 테스트"""
        # AI_PROVIDER를 설정하지 않음
        monkeypatch.delenv("AI_PROVIDER", raising=False)

        config = Config.load()

        assert config.AI_PROVIDER == "openai"

    def test_validate_provider_openai(self):
        """"openai" Provider 검증 성공 테스트"""
        # 예외가 발생하지 않아야 함
        Config._validate_provider("openai")

    def test_validate_provider_azure(self):
        """"azure" Provider 검증 성공 테스트"""
        # 예외가 발생하지 않아야 함
        Config._validate_provider("azure")

    def test_validate_provider_invalid(self):
        """유효하지 않은 provider 검증 실패 테스트"""
        with pytest.raises(ValueError, match="지원하지 않는 Provider입니다"):
            Config._validate_provider("invalid-provider")

    def test_parse_azure_deployments_valid(self):
        """정상 deployment 파싱 테스트"""
        deployments_str = "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini"
        result = Config.parse_azure_deployments(deployments_str)

        assert result == {
            "gpt-4o": "my-gpt4o",
            "gpt-4o-mini": "my-mini"
        }

    def test_parse_azure_deployments_empty(self):
        """빈 문자열 파싱 테스트"""
        result = Config.parse_azure_deployments("")

        assert result == {}

    def test_parse_azure_deployments_none(self):
        """None 파싱 테스트"""
        result = Config.parse_azure_deployments(None)

        assert result == {}

    def test_parse_azure_deployments_multiple(self):
        """여러 deployment 파싱 테스트"""
        deployments_str = "gpt-4o:deploy1,gpt-4o-mini:deploy2,gpt-4-turbo:deploy3"
        result = Config.parse_azure_deployments(deployments_str)

        assert result == {
            "gpt-4o": "deploy1",
            "gpt-4o-mini": "deploy2",
            "gpt-4-turbo": "deploy3"
        }
        assert len(result) == 3
