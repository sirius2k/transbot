"""언어 감지 및 번역 방향 관리 기능을 제공하는 모듈"""
from utils import detect_language


class LanguageDetector:
    """텍스트의 언어를 자동 감지하고 번역 방향을 결정하는 클래스"""

    # 언어별 번역 방향 설정
    DIRECTION_CONFIG = {
        "Korean": {
            "source": "Korean",
            "target": "English",
            "arrow": "🇰🇷 → 🇺🇸",
            "code": "ko",
            "flag": "🇰🇷"
        },
        "English": {
            "source": "English",
            "target": "Korean",
            "arrow": "🇺🇸 → 🇰🇷",
            "code": "en",
            "flag": "🇺🇸"
        },
        "unknown": {
            "source": "unknown",
            "target": "unknown",
            "arrow": "❓",
            "code": "unknown",
            "flag": "❓"
        }
    }

    def __init__(self, threshold: float = 0.5):
        """
        Args:
            threshold: 한국어 감지 임계값 (기본 0.5, 현재 미사용)
        """
        self.threshold = threshold

    def detect(self, text: str) -> str:
        return detect_language(text)

    def get_translation_direction(self, text: str) -> tuple[str, str, str]:
        """텍스트를 분석하여 번역 방향을 결정합니다.

        Args:
            text: 입력 텍스트

        Returns:
            (source_lang, target_lang, direction_arrow) 튜플
            예: ("Korean", "English", "🇰🇷 → 🇺🇸")
        """
        detected = self.detect(text)
        config = self.DIRECTION_CONFIG.get(detected, self.DIRECTION_CONFIG["unknown"])
        return (config["source"], config["target"], config["arrow"])

    def get_language_code(self, language: str) -> str:
        """언어명을 ISO 639-1 코드로 변환합니다.

        Args:
            language: 언어명 ("Korean", "English", "unknown")

        Returns:
            언어 코드 ("ko", "en", "unknown")
        """
        config = self.DIRECTION_CONFIG.get(language, self.DIRECTION_CONFIG["unknown"])
        return config["code"]

    def get_language_flag(self, language: str) -> str:
        config = self.DIRECTION_CONFIG.get(language, self.DIRECTION_CONFIG["unknown"])
        return config["flag"]
