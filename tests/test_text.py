"""TextAnalyzer 클래스 테스트"""
from components.text import TextAnalyzer


class TestTextAnalyzer:
    """TextAnalyzer 클래스 테스트"""

    def setup_method(self):
        """각 테스트 전에 실행"""
        self.analyzer = TextAnalyzer(model="gpt-4o")

    def test_count_tokens_simple(self):
        """간단한 텍스트 토큰 카운트 테스트"""
        result = self.analyzer.count_tokens("Hello world")
        assert isinstance(result, int)
        assert result > 0

    def test_count_tokens_korean(self):
        """한국어 텍스트 토큰 카운트 테스트"""
        result = self.analyzer.count_tokens("안녕하세요")
        assert isinstance(result, int)
        assert result > 0

    def test_count_tokens_empty(self):
        """빈 문자열 토큰 카운트 테스트"""
        result = self.analyzer.count_tokens("")
        assert result == 0

    def test_count_tokens_long_text(self):
        """긴 텍스트 토큰 카운트 테스트"""
        long_text = "Hello world " * 100
        result = self.analyzer.count_tokens(long_text)
        assert isinstance(result, int)
        assert result > 100

    def test_count_tokens_different_models(self):
        """다른 모델로 토큰 카운트 테스트"""
        analyzer_mini = TextAnalyzer(model="gpt-4o-mini")
        result = analyzer_mini.count_tokens("Hello")
        assert isinstance(result, int)
        assert result > 0

    def test_count_characters(self):
        """문자 수 계산 테스트"""
        result = self.analyzer.count_characters("Hello")
        assert result == 5

    def test_count_characters_korean(self):
        """한국어 문자 수 계산 테스트"""
        result = self.analyzer.count_characters("안녕")
        assert result == 2

    def test_get_statistics(self):
        """통계 정보 테스트"""
        text = "Hello world\nSecond line"
        stats = self.analyzer.get_statistics(text)

        assert "characters" in stats
        assert "tokens" in stats
        assert "words" in stats
        assert "lines" in stats
        assert stats["characters"] == len(text)
        assert stats["words"] == 4  # "Hello", "world", "Second", "line"
        assert stats["lines"] == 2

    def test_get_statistics_empty(self):
        """빈 문자열 통계 테스트"""
        stats = self.analyzer.get_statistics("")

        assert stats["characters"] == 0
        assert stats["tokens"] == 0
        assert stats["words"] == 0
        assert stats["lines"] == 0  # 빈 문자열은 0줄

    def test_strip_markdown_bold(self):
        """볼드 Markdown 제거 테스트"""
        result = self.analyzer.strip_markdown("**bold text**")
        assert result == "bold text"

    def test_strip_markdown_multiple(self):
        """복합 Markdown 제거 테스트"""
        text = "# Title\n**Bold** and *italic*"
        result = self.analyzer.strip_markdown(text)
        assert "Title" in result
        assert "#" not in result
        assert "**" not in result

    def test_strip_markdown_plain_text(self):
        """Markdown이 없는 텍스트 테스트"""
        text = "plain text"
        result = self.analyzer.strip_markdown(text)
        assert result == text

    def test_has_markdown_true(self):
        """Markdown 포함 여부 테스트 (포함)"""
        result = self.analyzer.has_markdown("**bold**")
        assert result is True

    def test_has_markdown_false(self):
        """Markdown 포함 여부 테스트 (미포함)"""
        result = self.analyzer.has_markdown("plain text")
        assert result is False

    def test_format_statistics_display_with_arrow(self):
        """통계 표시 포맷팅 테스트 (화살표 포함)"""
        text = "Hello"
        result = self.analyzer.format_statistics_display(text, "🇺🇸 → 🇰🇷")

        assert "5" in result  # 5자
        assert "🇺🇸 → 🇰🇷" in result
        assert "토큰" in result
        assert "<div" in result

    def test_format_statistics_display_without_arrow(self):
        """통계 표시 포맷팅 테스트 (화살표 없음)"""
        text = "Hello"
        result = self.analyzer.format_statistics_display(text)

        assert "5" in result  # 5자
        assert "토큰" in result
        assert "#888" in result  # 회색 스타일

    def test_custom_model(self):
        """커스텀 모델 지정 테스트"""
        analyzer = TextAnalyzer(model="gpt-3.5-turbo")
        assert analyzer.model == "gpt-3.5-turbo"
        result = analyzer.count_tokens("Hello")
        assert isinstance(result, int)
