"""
utils.py의 핵심 함수들에 대한 단위 테스트
"""
import pytest
from unittest.mock import Mock
from utils import detect_language, count_tokens, strip_markdown, translate


class TestDetectLanguage:
    """언어 감지 함수 테스트"""

    def test_detect_korean(self):
        """한국어 텍스트 감지 테스트"""
        result = detect_language("안녕하세요. 한국어 텍스트입니다.")
        assert result == "Korean"

    def test_detect_english(self):
        """영어 텍스트 감지 테스트"""
        result = detect_language("Hello. This is English text.")
        assert result == "English"

    def test_detect_mixed_korean_dominant(self):
        """한국어가 우세한 혼합 텍스트 감지 테스트"""
        result = detect_language("안녕하세요 Hello 한국어가 더 많습니다.")
        assert result == "Korean"

    def test_detect_mixed_english_dominant(self):
        """영어가 우세한 혼합 텍스트 감지 테스트"""
        result = detect_language("Hello 안녕 This is mostly English text.")
        assert result == "English"

    def test_detect_empty_string(self):
        """빈 문자열 감지 테스트"""
        result = detect_language("")
        assert result == "unknown"

    def test_detect_whitespace_only(self):
        """공백만 있는 문자열 감지 테스트"""
        result = detect_language("   \n\t  ")
        assert result == "unknown"

    def test_detect_no_alpha(self):
        """알파벳 문자가 없는 텍스트 감지 테스트"""
        result = detect_language("123 !@# 456")
        assert result == "unknown"

    def test_detect_exact_50_50(self):
        """한글과 영어가 정확히 50:50인 경우 테스트"""
        result = detect_language("안녕 Hello")
        # 50:50인 경우 영어로 판정 (> 0.5 조건)
        assert result == "English"


class TestCountTokens:
    """토큰 카운트 함수 테스트"""

    def test_count_tokens_simple(self):
        """간단한 텍스트 토큰 카운트 테스트"""
        result = count_tokens("Hello world", "gpt-4o")
        assert isinstance(result, int)
        assert result > 0

    def test_count_tokens_korean(self):
        """한국어 텍스트 토큰 카운트 테스트"""
        result = count_tokens("안녕하세요", "gpt-4o")
        assert isinstance(result, int)
        assert result > 0

    def test_count_tokens_empty(self):
        """빈 문자열 토큰 카운트 테스트"""
        result = count_tokens("", "gpt-4o")
        assert result == 0

    def test_count_tokens_long_text(self):
        """긴 텍스트 토큰 카운트 테스트"""
        long_text = "Hello world! " * 100
        result = count_tokens(long_text, "gpt-4o")
        assert isinstance(result, int)
        assert result > 100  # 최소한 100개 이상의 토큰

    def test_count_tokens_different_models(self):
        """다른 모델에 대한 토큰 카운트 테스트"""
        text = "Hello world"
        result_4o = count_tokens(text, "gpt-4o")
        result_35 = count_tokens(text, "gpt-3.5-turbo")

        assert isinstance(result_4o, int)
        assert isinstance(result_35, int)
        assert result_4o > 0
        assert result_35 > 0


class TestStripMarkdown:
    """Markdown 제거 함수 테스트"""

    def test_strip_bold(self):
        """볼드 제거 테스트"""
        result = strip_markdown("**bold text**")
        assert result == "bold text"

    def test_strip_italic(self):
        """이탤릭 제거 테스트"""
        result = strip_markdown("*italic text*")
        assert result == "italic text"

    def test_strip_heading(self):
        """헤딩 제거 테스트"""
        result = strip_markdown("# Heading 1")
        assert result == "Heading 1"

    def test_strip_multiple_headings(self):
        """여러 레벨의 헤딩 제거 테스트"""
        assert strip_markdown("# H1") == "H1"
        assert strip_markdown("## H2") == "H2"
        assert strip_markdown("### H3") == "H3"
        assert strip_markdown("#### H4") == "H4"

    def test_strip_link(self):
        """링크 제거 테스트"""
        result = strip_markdown("[link text](https://example.com)")
        assert result == "link text"

    def test_strip_code(self):
        """인라인 코드 제거 테스트"""
        result = strip_markdown("`code`")
        assert result == "code"

    def test_strip_list_dash(self):
        """대시 리스트 제거 테스트"""
        result = strip_markdown("- list item")
        assert result == "list item"

    def test_strip_list_asterisk(self):
        """별표 리스트 제거 테스트"""
        result = strip_markdown("* list item")
        assert result == "list item"

    def test_strip_list_numbered(self):
        """번호 리스트 제거 테스트"""
        result = strip_markdown("1. list item")
        assert result == "list item"

    def test_strip_blockquote(self):
        """인용문 제거 테스트"""
        result = strip_markdown("> quoted text")
        assert result == "quoted text"

    def test_strip_horizontal_rule(self):
        """수평선 제거 테스트"""
        result = strip_markdown("---")
        assert result == ""

    def test_strip_code_block(self):
        """코드 블록 제거 테스트"""
        text = "```python\nprint('hello')\n```"
        result = strip_markdown(text)
        assert result == ""

    def test_strip_image(self):
        """이미지 제거 테스트"""
        result = strip_markdown("![alt text](image.png)")
        assert result == "alt text"

    def test_strip_complex(self):
        """복합 Markdown 제거 테스트"""
        text = "# Title\n**Bold** and *italic* with `code` and [link](url)"
        result = strip_markdown(text)
        assert "Title" in result
        assert "Bold" in result
        assert "italic" in result
        assert "code" in result
        assert "link" in result
        assert "#" not in result
        assert "**" not in result
        assert "*" not in result
        assert "`" not in result
        assert "[" not in result
        assert "]" not in result
        assert "(" not in result

    def test_strip_empty_string(self):
        """빈 문자열 처리 테스트"""
        result = strip_markdown("")
        assert result == ""

    def test_strip_plain_text(self):
        """일반 텍스트 처리 테스트"""
        text = "This is plain text with no markdown."
        result = strip_markdown(text)
        assert result == text


class TestTranslate:
    """번역 함수 테스트 (Mock 사용)"""

    def test_translate_success(self):
        """번역 성공 테스트"""
        # Mock client 생성
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "번역된 텍스트"

        mock_client.chat.completions.create.return_value = mock_response

        result = translate(mock_client, "Hello", "English", "Korean", "gpt-4o")

        assert result == "번역된 텍스트"
        mock_client.chat.completions.create.assert_called_once()

    def test_translate_with_correct_parameters(self):
        """번역 함수가 올바른 파라미터로 호출되는지 테스트"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Translated"

        mock_client.chat.completions.create.return_value = mock_response

        translate(mock_client, "Test", "English", "Korean", "gpt-4o-mini")

        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['model'] == "gpt-4o-mini"
        assert call_args[1]['temperature'] == 0.3
        assert len(call_args[1]['messages']) == 2
        assert call_args[1]['messages'][0]['role'] == "system"
        assert call_args[1]['messages'][1]['role'] == "user"
        assert call_args[1]['messages'][1]['content'] == "Test"

    def test_translate_preserves_markdown_instruction(self):
        """번역 함수가 Markdown 보존 지시를 포함하는지 테스트"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Result"

        mock_client.chat.completions.create.return_value = mock_response

        translate(mock_client, "Text", "English", "Korean", "gpt-4o")

        call_args = mock_client.chat.completions.create.call_args
        system_message = call_args[1]['messages'][0]['content']

        assert "Markdown" in system_message
        assert "Preserve" in system_message or "preserve" in system_message
