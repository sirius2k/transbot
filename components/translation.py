"""번역 관리 기능을 제공하는 모듈"""

import logging
import time
from typing import Optional, Any
from config import Config
from langfuse.decorators import observe, langfuse_context
from utils import count_tokens

logger = logging.getLogger("transbot.translation")


class TranslationManager:
    """번역 작업을 관리하는 클래스

    OpenAI 클라이언트를 관리하고 번역 설정(모델, temperature)을 유지합니다.
    """

    # 지원하는 모델 목록
    SUPPORTED_MODELS = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo"
    ]

    def __init__(
        self,
        client: Any,
        config: Optional[Config] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        max_tokens: Optional[int] = None
    ) -> None:
        """
        Args:
            client: OpenAI 클라이언트 인스턴스
            config: Config 인스턴스 (None이면 Config.load() 호출)
            model: 사용할 AI 모델 (None이면 config에서 로드)
            temperature: 번역 창의성 설정 (None이면 config에서 로드)
            timeout: API 타임아웃 초 (None이면 config에서 로드)
            max_retries: API 재시도 횟수 (None이면 config에서 로드)
            max_tokens: 최대 출력 토큰 수 (None이면 config에서 로드)

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        # Config에서 기본값 로드
        self.config = config if config is not None else Config.load()

        # 파라미터가 None이면 config 값 사용
        self.model = model if model is not None else self.config.DEFAULT_MODEL
        self.temperature = temperature if temperature is not None else self.config.DEFAULT_TEMPERATURE
        self.timeout = timeout if timeout is not None else self.config.OPENAI_API_TIMEOUT
        self.max_retries = max_retries if max_retries is not None else self.config.OPENAI_MAX_RETRIES
        self.max_tokens = max_tokens if max_tokens is not None else self.config.MAX_TOKENS

        # 모델 검증
        if not self.validate_model(self.model):
            raise ValueError(f"지원하지 않는 모델입니다: {self.model}")

        self.client = client

    @observe(as_type="generation", name="translation")
    def translate(self, text: str, source: str, target: str, session_id: str = "unknown") -> str:
        """텍스트를 번역합니다.

        @observe(as_type="generation")로 Langfuse에 자동 추적됩니다.
        입력/출력, 타이밍, 에러 상태가 자동으로 기록됩니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")
            session_id: 세션 ID (Langfuse 추적용)

        Returns:
            번역된 텍스트
        """
        start_time = time.time()
        input_length = len(text)

        # Langfuse trace에 session_id 설정
        langfuse_context.update_current_trace(session_id=session_id)

        # API 호출 시작 로깅
        logger.info(
            "번역 API 호출 시작",
            extra={
                "provider": "openai" if not hasattr(self, 'deployment') else "azure",
                "model": self.model,
                "source_lang": source,
                "target_lang": target,
                "input_length": input_length,
                "temperature": self.temperature
            }
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following {source} text to {target}. IMPORTANT: Preserve all Markdown formatting (bold, italic, headings, lists, links, code blocks, blockquotes, tables, etc.) in the translation. Only respond with the translation, nothing else."  # noqa: E501
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )
            result = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Langfuse observation에 모델/사용량/메타데이터 업데이트
            langfuse_context.update_current_observation(
                model=self.model,
                usage={
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens,
                },
                metadata={"direction": f"{source}→{target}"},
            )

            # API 호출 성공 로깅
            response_time_ms = int((time.time() - start_time) * 1000)
            logger.info(
                "번역 API 호출 성공",
                extra={
                    "provider": "openai" if not hasattr(self, 'deployment') else "azure",
                    "model": self.model,
                    "response_time_ms": response_time_ms,
                    "output_length": len(result),
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                }
            )

            langfuse_context.flush()
            return result

        except Exception as e:
            # 에러 발생 시 입력 토큰 추정 (Langfuse에 usage 정보 제공)
            estimated_input_tokens = count_tokens(text, self.model)
            langfuse_context.update_current_observation(
                model=self.model,
                usage={
                    "input": estimated_input_tokens,
                    "output": 0,
                    "total": estimated_input_tokens,
                },
                metadata={"direction": f"{source}→{target}"},
            )

            # API 호출 실패 로깅
            logger.error(
                "번역 API 호출 실패",
                extra={
                    "provider": "openai" if not hasattr(self, 'deployment') else "azure",
                    "model": self.model,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "input_length": input_length
                },
                exc_info=True
            )

            langfuse_context.flush()
            raise

    def set_model(self, model: str) -> None:
        """사용할 AI 모델을 변경합니다.

        Args:
            model: 새로운 모델명

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        if not self.validate_model(model):
            raise ValueError(f"지원하지 않는 모델입니다: {model}")
        self.model = model

    def set_temperature(self, temperature: float) -> None:
        """번역 창의성 설정을 변경합니다.

        Args:
            temperature: 0.0 ~ 1.0 사이의 값

        Raises:
            ValueError: 유효하지 않은 temperature 값
        """
        if not 0.0 <= temperature <= 1.0:
            raise ValueError("temperature는 0.0에서 1.0 사이여야 합니다")
        self.temperature = temperature

    @staticmethod
    def get_model_list() -> list[str]:
        return TranslationManager.SUPPORTED_MODELS.copy()

    @staticmethod
    def validate_model(model: str) -> bool:
        return model in TranslationManager.SUPPORTED_MODELS


class AzureTranslationManager(TranslationManager):
    """Azure OpenAI 번역 관리 클래스

    TranslationManager를 상속하여 Azure OpenAI의 deployment 방식을 지원합니다.
    """

    # Azure deployment 목록 (설정에서 로드)
    SUPPORTED_DEPLOYMENTS: dict[str, str] = {}

    def __init__(
        self,
        client: Any,
        deployment: str,
        config: Optional[Config] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        max_tokens: Optional[int] = None
    ) -> None:
        """Azure OpenAI용 초기화

        Args:
            client: AzureOpenAI 클라이언트 인스턴스
            deployment: Azure deployment 이름 (필수)
            config: Config 인스턴스 (None이면 Config.load() 호출)
            model: 원래 모델명 (표시용, 선택)
            temperature: 번역 창의성 설정 (None이면 config에서 로드)
            timeout: API 타임아웃 초 (None이면 config에서 로드)
            max_retries: API 재시도 횟수 (None이면 config에서 로드)
            max_tokens: 최대 출력 토큰 수 (None이면 config에서 로드)
        """
        # Config에서 기본값 로드
        self.config = config if config is not None else Config.load()

        # deployment 저장 (필수)
        self.deployment = deployment
        # model은 표시용 (deployment를 기본값으로 사용)
        self.model = model if model is not None else deployment

        # 나머지 속성 초기화
        self.temperature = temperature if temperature is not None else self.config.DEFAULT_TEMPERATURE
        self.timeout = timeout if timeout is not None else self.config.OPENAI_API_TIMEOUT
        self.max_retries = max_retries if max_retries is not None else self.config.OPENAI_MAX_RETRIES
        self.max_tokens = max_tokens if max_tokens is not None else self.config.MAX_TOKENS

        self.client = client

    @observe(as_type="generation", name="translation")
    def translate(self, text: str, source: str, target: str, session_id: str = "unknown") -> str:
        """텍스트를 번역합니다 (Azure 전용).

        @observe(as_type="generation")로 Langfuse에 자동 추적됩니다.
        OpenAI와 다른 점: model 파라미터에 deployment 이름을 사용합니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")
            session_id: 세션 ID (Langfuse 추적용)

        Returns:
            번역된 텍스트
        """
        start_time = time.time()
        input_length = len(text)

        # Langfuse trace에 session_id 설정
        langfuse_context.update_current_trace(session_id=session_id)

        # API 호출 시작 로깅
        logger.info(
            "번역 API 호출 시작",
            extra={
                "provider": "azure",
                "model": self.model,
                "deployment": self.deployment,
                "source_lang": source,
                "target_lang": target,
                "input_length": input_length,
                "temperature": self.temperature
            }
        )

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,  # Azure는 deployment 이름 사용
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following {source} text to {target}. IMPORTANT: Preserve all Markdown formatting (bold, italic, headings, lists, links, code blocks, blockquotes, tables, etc.) in the translation. Only respond with the translation, nothing else."  # noqa: E501
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )
            result = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Langfuse observation에 모델/사용량/메타데이터 업데이트
            langfuse_context.update_current_observation(
                model=self.model,
                usage={
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens,
                },
                metadata={
                    "direction": f"{source}→{target}",
                    "deployment": self.deployment,
                },
            )

            # API 호출 성공 로깅
            response_time_ms = int((time.time() - start_time) * 1000)
            logger.info(
                "번역 API 호출 성공",
                extra={
                    "provider": "azure",
                    "model": self.model,
                    "deployment": self.deployment,
                    "response_time_ms": response_time_ms,
                    "output_length": len(result),
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                }
            )

            langfuse_context.flush()
            return result

        except Exception as e:
            # 에러 발생 시 입력 토큰 추정 (Langfuse에 usage 정보 제공)
            estimated_input_tokens = count_tokens(text, self.model)
            langfuse_context.update_current_observation(
                model=self.model,
                usage={
                    "input": estimated_input_tokens,
                    "output": 0,
                    "total": estimated_input_tokens,
                },
                metadata={
                    "direction": f"{source}→{target}",
                    "deployment": self.deployment,
                },
            )

            # API 호출 실패 로깅
            logger.error(
                "번역 API 호출 실패",
                extra={
                    "provider": "azure",
                    "model": self.model,
                    "deployment": self.deployment,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "input_length": input_length
                },
                exc_info=True
            )

            langfuse_context.flush()
            raise

    @classmethod
    def load_deployments(cls, config: Config) -> None:
        """Config에서 deployment 목록을 로드합니다.

        Args:
            config: Config 인스턴스
        """
        cls.SUPPORTED_DEPLOYMENTS = config.parse_azure_deployments(
            config.AZURE_DEPLOYMENTS
        )

    @staticmethod
    def validate_deployment(deployment: str) -> bool:
        """Deployment가 유효한지 검증합니다.

        Args:
            deployment: 검증할 deployment 이름

        Returns:
            유효하면 True, 아니면 False
        """
        return deployment in AzureTranslationManager.SUPPORTED_DEPLOYMENTS.values()


class TranslationManagerFactory:
    """번역 관리자 생성 팩토리

    Provider에 따라 적절한 TranslationManager 인스턴스를 생성합니다.
    """

    @staticmethod
    def create(provider: str, client: Any, **kwargs: Any) -> TranslationManager:
        """Provider에 따른 TranslationManager 생성

        Args:
            provider: "openai" 또는 "azure"
            client: OpenAI 또는 AzureOpenAI 클라이언트
            **kwargs: TranslationManager 초기화 파라미터

        Returns:
            TranslationManager 또는 AzureTranslationManager 인스턴스
        """
        if provider == "azure":
            return AzureTranslationManager(client, **kwargs)
        return TranslationManager(client, **kwargs)
