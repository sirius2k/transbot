"""LanguageDetector 클래스 테스트"""
import pytest
from components.language import LanguageDetector


class TestLanguageDetector:
    """LanguageDetector 클래스 테스트"""

    def setup_method(self):
        """각 테스트 전에 실행"""
        self.detector = LanguageDetector()

    def test_detect_korean(self):
        """한국어 감지 테스트"""
        result = self.detector.detect("안녕하세요")
        assert result == "Korean"

    def test_detect_english(self):
        """영어 감지 테스트"""
        result = self.detector.detect("Hello world")
        assert result == "English"

    def test_detect_empty(self):
        """빈 문자열 감지 테스트"""
        result = self.detector.detect("")
        assert result == "unknown"

    def test_detect_whitespace_only(self):
        """공백만 있는 문자열 감지 테스트"""
        result = self.detector.detect("   ")
        assert result == "unknown"

    def test_detect_mixed_korean_dominant(self):
        """한국어가 우세한 혼합 텍스트 감지 테스트"""
        result = self.detector.detect("안녕하세요 반갑습니다 Hello")
        assert result == "Korean"

    def test_detect_mixed_english_dominant(self):
        """영어가 우세한 혼합 텍스트 감지 테스트"""
        result = self.detector.detect("Hello World 안녕")
        assert result == "English"

    def test_get_translation_direction_korean(self):
        """한국어 → 영어 방향 테스트"""
        source, target, arrow = self.detector.get_translation_direction("안녕")
        assert source == "Korean"
        assert target == "English"
        assert arrow == "🇰🇷 → 🇺🇸"

    def test_get_translation_direction_english(self):
        """영어 → 한국어 방향 테스트"""
        source, target, arrow = self.detector.get_translation_direction("Hello")
        assert source == "English"
        assert target == "Korean"
        assert arrow == "🇺🇸 → 🇰🇷"

    def test_get_translation_direction_unknown(self):
        """알 수 없는 언어 방향 테스트"""
        source, target, arrow = self.detector.get_translation_direction("123")
        assert source == "unknown"
        assert target == "unknown"
        assert arrow == "❓"

    def test_get_language_code_korean(self):
        """한국어 코드 변환 테스트"""
        result = self.detector.get_language_code("Korean")
        assert result == "ko"

    def test_get_language_code_english(self):
        """영어 코드 변환 테스트"""
        result = self.detector.get_language_code("English")
        assert result == "en"

    def test_get_language_code_unknown(self):
        """알 수 없는 언어 코드 테스트"""
        result = self.detector.get_language_code("French")
        assert result == "unknown"

    def test_get_language_flag_korean(self):
        """한국어 플래그 이모지 테스트"""
        result = self.detector.get_language_flag("Korean")
        assert result == "🇰🇷"

    def test_get_language_flag_english(self):
        """영어 플래그 이모지 테스트"""
        result = self.detector.get_language_flag("English")
        assert result == "🇺🇸"

    def test_get_language_flag_unknown(self):
        """알 수 없는 언어 플래그 테스트"""
        result = self.detector.get_language_flag("unknown")
        assert result == "❓"

    def test_custom_threshold(self):
        """커스텀 임계값 테스트"""
        detector = LanguageDetector(threshold=0.7)
        assert detector.threshold == 0.7
