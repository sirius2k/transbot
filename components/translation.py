"""번역 관리 기능을 제공하는 모듈"""
from utils import translate as translate_func


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

    def __init__(self, client, model: str = "gpt-4o-mini", temperature: float = 0.3):
        """
        Args:
            client: OpenAI 클라이언트 인스턴스
            model: 사용할 AI 모델 (기본 gpt-4o-mini)
            temperature: 번역 창의성 설정 (기본 0.3)

        Raises:
            ValueError: 지원하지 않는 모델인 경우
        """
        if not self.validate_model(model):
            raise ValueError(f"지원하지 않는 모델입니다: {model}")

        self.client = client
        self.model = model
        self.temperature = temperature

    def translate(self, text: str, source: str, target: str) -> str:
        """텍스트를 번역합니다.

        기존 translate() 함수를 사용하되, 클래스의 설정(model, temperature)을 적용합니다.

        Args:
            text: 번역할 텍스트
            source: 원본 언어 (예: "Korean", "English")
            target: 대상 언어 (예: "English", "Korean")

        Returns:
            번역된 텍스트
        """
        # 기존 translate 함수를 사용하되, temperature는 클래스 설정 사용
        # 현재 utils.translate는 temperature를 매개변수로 받지 않으므로
        # client의 completions.create 호출에 직접 전달
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
            temperature=self.temperature
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
        """지원하는 모델 목록을 반환합니다.

        Returns:
            모델명 리스트
        """
        return TranslationManager.SUPPORTED_MODELS.copy()

    @staticmethod
    def validate_model(model: str) -> bool:
        """모델이 지원되는지 검증합니다.

        Args:
            model: 검증할 모델명

        Returns:
            지원 여부 (True/False)
        """
        return model in TranslationManager.SUPPORTED_MODELS
