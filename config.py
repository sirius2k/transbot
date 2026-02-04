"""
TransBot 설정 관리 모듈

환경 변수를 통해 애플리케이션 설정을 관리합니다.
"""
import os
from typing import Optional, Literal
from dotenv import load_dotenv


class Config:
    """애플리케이션 설정 클래스

    환경 변수에서 설정을 로드하고 타입 검증을 수행합니다.
    환경 변수가 설정되지 않은 경우 기본값을 사용합니다.
    """

    # ========================================================================
    # 기본값 정의
    # ========================================================================

    # OpenAI API 설정
    _DEFAULT_OPENAI_API_TIMEOUT = 60
    _DEFAULT_OPENAI_MAX_RETRIES = 3

    # AI 모델 설정
    _DEFAULT_MODEL = "gpt-4o-mini"
    _DEFAULT_TEMPERATURE = 0.3
    _DEFAULT_MAX_TOKENS = 4000

    # 언어 감지 설정
    _DEFAULT_LANGUAGE_DETECTION_THRESHOLD = 0.5

    # 애플리케이션 설정
    _DEFAULT_APP_TITLE = "TransBot"
    _DEFAULT_APP_ICON = "🌐"
    _DEFAULT_APP_LAYOUT = "centered"

    # UI 설정
    _DEFAULT_TEXT_AREA_HEIGHT = 200
    _DEFAULT_MAX_INPUT_LENGTH = 50000

    # Azure OpenAI 설정
    _DEFAULT_AI_PROVIDER = "openai"
    _DEFAULT_AZURE_API_VERSION = "2024-02-15-preview"

    # 지원하는 모델 목록
    _SUPPORTED_MODELS = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo"
    ]

    # 지원하는 레이아웃 모드
    _SUPPORTED_LAYOUTS = ["centered", "wide"]

    def __init__(self) -> None:
        """Config 인스턴스를 초기화합니다."""
        # OpenAI API 설정
        self.OPENAI_API_KEY: Optional[str] = None
        self.OPENAI_API_TIMEOUT: int = self._DEFAULT_OPENAI_API_TIMEOUT
        self.OPENAI_MAX_RETRIES: int = self._DEFAULT_OPENAI_MAX_RETRIES

        # AI 모델 설정
        self.DEFAULT_MODEL: str = self._DEFAULT_MODEL
        self.DEFAULT_TEMPERATURE: float = self._DEFAULT_TEMPERATURE
        self.MAX_TOKENS: int = self._DEFAULT_MAX_TOKENS

        # 언어 감지 설정
        self.LANGUAGE_DETECTION_THRESHOLD: float = self._DEFAULT_LANGUAGE_DETECTION_THRESHOLD

        # 애플리케이션 설정
        self.APP_TITLE: str = self._DEFAULT_APP_TITLE
        self.APP_ICON: str = self._DEFAULT_APP_ICON
        self.APP_LAYOUT: Literal["centered", "wide"] = self._DEFAULT_APP_LAYOUT  # type: ignore

        # UI 설정
        self.TEXT_AREA_HEIGHT: int = self._DEFAULT_TEXT_AREA_HEIGHT
        self.MAX_INPUT_LENGTH: int = self._DEFAULT_MAX_INPUT_LENGTH

        # Azure OpenAI 설정
        self.AI_PROVIDER: Literal["openai", "azure"] = self._DEFAULT_AI_PROVIDER  # type: ignore
        self.AZURE_OPENAI_API_KEY: Optional[str] = None
        self.AZURE_OPENAI_ENDPOINT: Optional[str] = None
        self.AZURE_OPENAI_API_VERSION: str = self._DEFAULT_AZURE_API_VERSION
        self.AZURE_DEPLOYMENTS: Optional[str] = None

        # Langfuse 설정
        self.LANGFUSE_PUBLIC_KEY: Optional[str] = None
        self.LANGFUSE_SECRET_KEY: Optional[str] = None
        self.LANGFUSE_HOST: Optional[str] = None

    @classmethod
    def load(cls) -> 'Config':
        """환경 변수를 로드하고 Config 객체를 반환합니다.

        .env 파일에서 환경 변수를 로드한 후, 타입 변환 및 검증을 수행합니다.

        Returns:
            Config: 설정이 로드된 Config 인스턴스

        Raises:
            ValueError: 잘못된 설정값이 입력된 경우
        """
        # .env 파일 로드
        load_dotenv()

        config = cls()

        # OpenAI API 설정
        config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        config.OPENAI_API_TIMEOUT = cls._get_int_env(
            "OPENAI_API_TIMEOUT",
            cls._DEFAULT_OPENAI_API_TIMEOUT
        )
        config.OPENAI_MAX_RETRIES = cls._get_int_env(
            "OPENAI_MAX_RETRIES",
            cls._DEFAULT_OPENAI_MAX_RETRIES
        )

        # AI 모델 설정
        config.DEFAULT_MODEL = cls._get_str_env(
            "DEFAULT_MODEL",
            cls._DEFAULT_MODEL
        )
        cls._validate_model(config.DEFAULT_MODEL)

        config.DEFAULT_TEMPERATURE = cls._get_float_env(
            "DEFAULT_TEMPERATURE",
            cls._DEFAULT_TEMPERATURE
        )
        cls._validate_temperature(config.DEFAULT_TEMPERATURE)

        config.MAX_TOKENS = cls._get_int_env(
            "MAX_TOKENS",
            cls._DEFAULT_MAX_TOKENS
        )

        # 언어 감지 설정
        config.LANGUAGE_DETECTION_THRESHOLD = cls._get_float_env(
            "LANGUAGE_DETECTION_THRESHOLD",
            cls._DEFAULT_LANGUAGE_DETECTION_THRESHOLD
        )
        cls._validate_threshold(config.LANGUAGE_DETECTION_THRESHOLD)

        # 애플리케이션 설정
        config.APP_TITLE = cls._get_str_env(
            "APP_TITLE",
            cls._DEFAULT_APP_TITLE
        )
        config.APP_ICON = cls._get_str_env(
            "APP_ICON",
            cls._DEFAULT_APP_ICON
        )
        layout_str = cls._get_str_env(
            "APP_LAYOUT",
            cls._DEFAULT_APP_LAYOUT
        )
        cls._validate_layout(layout_str)
        config.APP_LAYOUT = layout_str  # type: ignore

        # UI 설정
        config.TEXT_AREA_HEIGHT = cls._get_int_env(
            "TEXT_AREA_HEIGHT",
            cls._DEFAULT_TEXT_AREA_HEIGHT
        )
        config.MAX_INPUT_LENGTH = cls._get_int_env(
            "MAX_INPUT_LENGTH",
            cls._DEFAULT_MAX_INPUT_LENGTH
        )

        # Azure OpenAI 설정
        provider_str = cls._get_str_env(
            "AI_PROVIDER",
            cls._DEFAULT_AI_PROVIDER
        )
        cls._validate_provider(provider_str)
        config.AI_PROVIDER = provider_str  # type: ignore

        config.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        config.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        config.AZURE_OPENAI_API_VERSION = cls._get_str_env(
            "AZURE_OPENAI_API_VERSION",
            cls._DEFAULT_AZURE_API_VERSION
        )
        config.AZURE_DEPLOYMENTS = os.getenv("AZURE_DEPLOYMENTS")

        # Langfuse 설정
        config.LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
        config.LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
        config.LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

        return config

    # ========================================================================
    # 환경 변수 로드 헬퍼 메서드
    # ========================================================================

    @staticmethod
    def _get_str_env(key: str, default: str) -> str:
        """문자열 환경 변수를 가져옵니다.

        Args:
            key: 환경 변수 키
            default: 기본값

        Returns:
            환경 변수 값 또는 기본값
        """
        return os.getenv(key, default)

    @staticmethod
    def _get_int_env(key: str, default: int) -> int:
        """정수 환경 변수를 가져옵니다.

        Args:
            key: 환경 변수 키
            default: 기본값

        Returns:
            환경 변수 값 (정수) 또는 기본값

        Raises:
            ValueError: 환경 변수가 정수로 변환될 수 없는 경우
        """
        value = os.getenv(key)
        if value is None:
            return default

        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"환경 변수 '{key}'의 값 '{value}'은(는) 정수여야 합니다."
            )

    @staticmethod
    def _get_float_env(key: str, default: float) -> float:
        """실수 환경 변수를 가져옵니다.

        Args:
            key: 환경 변수 키
            default: 기본값

        Returns:
            환경 변수 값 (실수) 또는 기본값

        Raises:
            ValueError: 환경 변수가 실수로 변환될 수 없는 경우
        """
        value = os.getenv(key)
        if value is None:
            return default

        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"환경 변수 '{key}'의 값 '{value}'은(는) 실수여야 합니다."
            )

    # ========================================================================
    # 검증 메서드
    # ========================================================================

    @classmethod
    def _validate_model(cls, model: str) -> None:
        """모델이 지원되는지 검증합니다.

        Args:
            model: 검증할 모델명

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        if model not in cls._SUPPORTED_MODELS:
            raise ValueError(
                f"지원하지 않는 모델입니다: {model}. "
                f"지원 모델: {', '.join(cls._SUPPORTED_MODELS)}"
            )

    @staticmethod
    def _validate_temperature(temperature: float) -> None:
        """temperature 값이 유효한지 검증합니다.

        Args:
            temperature: 검증할 temperature 값

        Raises:
            ValueError: temperature가 0.0~1.0 범위를 벗어난 경우
        """
        if not 0.0 <= temperature <= 1.0:
            raise ValueError(
                f"temperature는 0.0에서 1.0 사이여야 합니다. (현재: {temperature})"
            )

    @staticmethod
    def _validate_threshold(threshold: float) -> None:
        """언어 감지 임계값이 유효한지 검증합니다.

        Args:
            threshold: 검증할 임계값

        Raises:
            ValueError: 임계값이 0.0~1.0 범위를 벗어난 경우
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                f"언어 감지 임계값은 0.0에서 1.0 사이여야 합니다. (현재: {threshold})"
            )

    @classmethod
    def _validate_layout(cls, layout: str) -> None:
        """레이아웃 모드가 유효한지 검증합니다.

        Args:
            layout: 검증할 레이아웃 모드

        Raises:
            ValueError: 지원하지 않는 레이아웃 모드인 경우
        """
        if layout not in cls._SUPPORTED_LAYOUTS:
            raise ValueError(
                f"지원하지 않는 레이아웃 모드입니다: {layout}. "
                f"지원 모드: {', '.join(cls._SUPPORTED_LAYOUTS)}"
            )

    @staticmethod
    def _validate_provider(provider: str) -> None:
        """AI Provider가 유효한지 검증합니다.

        Args:
            provider: 검증할 Provider ("openai" 또는 "azure")

        Raises:
            ValueError: 지원하지 않는 Provider인 경우
        """
        if provider not in ["openai", "azure"]:
            raise ValueError(
                f"지원하지 않는 Provider입니다: {provider}. "
                f"지원 Provider: openai, azure"
            )

    @property
    def langfuse_enabled(self) -> bool:
        """Langfuse가 활성화되었는지 확인합니다.

        Returns:
            bool: 3개 환경 변수가 모두 설정된 경우 True, 그렇지 않으면 False
        """
        return all([
            self.LANGFUSE_PUBLIC_KEY,
            self.LANGFUSE_SECRET_KEY,
            self.LANGFUSE_HOST
        ])

    @staticmethod
    def parse_azure_deployments(deployments_str: Optional[str]) -> dict[str, str]:
        """Azure deployment 문자열을 파싱합니다.

        Args:
            deployments_str: "model:deployment,model:deployment" 형식의 문자열
                           예: "gpt-4o:my-gpt4o,gpt-4o-mini:my-mini"

        Returns:
            모델명과 deployment 이름의 매핑 딕셔너리
            예: {"gpt-4o": "my-gpt4o", "gpt-4o-mini": "my-mini"}
        """
        if not deployments_str:
            return {}

        result = {}
        for pair in deployments_str.split(","):
            pair = pair.strip()
            if ":" in pair:
                model, deployment = pair.split(":", 1)
                result[model.strip()] = deployment.strip()

        return result
