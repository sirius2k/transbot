"""텍스트 분석 및 처리 기능을 제공하는 모듈"""
from utils import count_tokens, strip_markdown


class TextAnalyzer:
    """텍스트 분석 및 Markdown 처리를 담당하는 클래스"""

    def __init__(self, model: str = "gpt-4o"):
        """
        Args:
            model: 토큰 카운팅에 사용할 모델명 (기본 gpt-4o)
        """
        self.model = model

    def count_tokens(self, text: str) -> int:
        return count_tokens(text, self.model)

    def count_characters(self, text: str) -> int:
        return len(text)

    def get_statistics(self, text: str) -> dict:
        """텍스트의 통계 정보를 반환합니다.

        Args:
            text: 분석할 텍스트

        Returns:
            통계 정보 딕셔너리 {
                "characters": 문자 수,
                "tokens": 토큰 수,
                "words": 단어 수 (공백 기준),
                "lines": 줄 수
            }
        """
        return {
            "characters": len(text),
            "tokens": self.count_tokens(text),
            "words": len(text.split()),
            "lines": len(text.splitlines())
        }

    def strip_markdown(self, text: str) -> str:
        return strip_markdown(text)

    def has_markdown(self, text: str) -> bool:
        stripped = self.strip_markdown(text)
        return stripped != text

    def format_statistics_display(self, text: str, direction_arrow: str = "") -> str:
        """통계 정보를 UI 표시용 HTML로 포맷합니다.

        Args:
            text: 분석할 텍스트
            direction_arrow: 번역 방향 화살표 (예: "🇰🇷 → 🇺🇸")

        Returns:
            HTML 형식의 통계 문자열
        """
        char_count = len(text)
        token_count = self.count_tokens(text)

        if direction_arrow:
            return f"<div style='text-align: right;'>{direction_arrow}<br/>{char_count:,}자 / {token_count:,} 토큰</div>"
        else:
            return f"<div style='text-align: right; color: #888;'>{char_count:,}자 / {token_count:,} 토큰</div>"
