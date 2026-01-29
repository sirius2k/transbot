"""번역 관리 기능을 제공하는 모듈"""

from typing import Optional
from config import Config


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
        client,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Args:
            client: OpenAI 클라이언트 인스턴스
            model: 사용할 AI 모델 (None이면 config에서 로드)
            temperature: 번역 창의성 설정 (None이면 config에서 로드)
            timeout: API 타임아웃 초 (None이면 config에서 로드)
            max_retries: API 재시도 횟수 (None이면 config에서 로드)
            max_tokens: 최대 출력 토큰 수 (None이면 config에서 로드)

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        # Config에서 기본값 로드
        config = Config.load()

        # 파라미터가 None이면 config 값 사용
        self.model = model if model is not None else config.DEFAULT_MODEL
        self.temperature = temperature if temperature is not None else config.DEFAULT_TEMPERATURE
        self.timeout = timeout if timeout is not None else config.OPENAI_API_TIMEOUT
        self.max_retries = max_retries if max_retries is not None else config.OPENAI_MAX_RETRIES
        self.max_tokens = max_tokens if max_tokens is not None else config.MAX_TOKENS

        # 모델 검증
        if not self.validate_model(self.model):
            raise ValueError(f"지원하지 않는 모델입니다: {self.model}")

        self.client = client

    def translate(self, text: str, source: str, target: str) -> str:
        """텍스트를 번역합니다.

        OpenAI API를 사용하여 클래스의 설정(model, temperature, timeout, max_tokens)을 적용합니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")

        Returns:
            번역된 텍스트
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following {source} text to {target}. IMPORTANT: Preserve all Markdown formatting (bold, italic, headings, lists, links, code blocks, blockquotes, tables, etc.) in the translation. Only respond with the translation, nothing else."
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
        return response.choices[0].message.content

    def set_model(self, model: str):
        """사용할 AI 모델을 변경합니다.

        Args:
            model: 새로운 모델명

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        if not self.validate_model(model):
            raise ValueError(f"지원하지 않는 모델입니다: {model}")
        self.model = model

    def set_temperature(self, temperature: float):
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
