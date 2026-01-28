"""
TransBot 유틸리티 함수 모듈
"""
import tiktoken
import re


# ============================================================================
# 언어 감지 상수
# ============================================================================

_KOREAN_DETECTION_THRESHOLD = 0.5  # 한국어 감지 임계값 (50% 이상)


# ============================================================================
# Markdown 패턴 상수
# ============================================================================

_MARKDOWN_CODE_BLOCK_PATTERN = re.compile(r'```[\s\S]*?```')
_MARKDOWN_INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')
_MARKDOWN_IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\([^)]+\)')
_MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\([^)]+\)')
_MARKDOWN_BOLD_PATTERN = re.compile(r'\*\*([^*]+)\*\*')
_MARKDOWN_ITALIC_PATTERN = re.compile(r'\*([^*]+)\*')
_MARKDOWN_HEADING_PATTERN = re.compile(r'^#{1,6}\s+', re.MULTILINE)
_MARKDOWN_LIST_PATTERN = re.compile(r'^\s*[-*+]\s+', re.MULTILINE)
_MARKDOWN_NUMBERED_LIST_PATTERN = re.compile(r'^\s*\d+\.\s+', re.MULTILINE)
_MARKDOWN_QUOTE_PATTERN = re.compile(r'^\s*>\s+', re.MULTILINE)
_MARKDOWN_HORIZONTAL_RULE_PATTERN = re.compile(r'^[-_*]{3,}$', re.MULTILINE)


# ============================================================================
# 언어 감지 함수
# ============================================================================

def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "unknown"

    korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7a3')
    english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)

    total_alpha = korean_chars + english_chars

    if total_alpha == 0:
        return "unknown"

    if korean_chars / total_alpha > _KOREAN_DETECTION_THRESHOLD:
        return "Korean"
    else:
        return "English"


# ============================================================================
# 토큰 카운팅 함수
# ============================================================================

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


# ============================================================================
# Markdown 처리 함수
# ============================================================================

def strip_markdown(text: str) -> str:
    text = _MARKDOWN_CODE_BLOCK_PATTERN.sub('', text)
    text = _MARKDOWN_INLINE_CODE_PATTERN.sub(r'\1', text)
    text = _MARKDOWN_IMAGE_PATTERN.sub(r'\1', text)
    text = _MARKDOWN_LINK_PATTERN.sub(r'\1', text)
    text = _MARKDOWN_BOLD_PATTERN.sub(r'\1', text)
    text = _MARKDOWN_ITALIC_PATTERN.sub(r'\1', text)
    text = _MARKDOWN_HEADING_PATTERN.sub('', text)
    text = _MARKDOWN_LIST_PATTERN.sub('', text)
    text = _MARKDOWN_NUMBERED_LIST_PATTERN.sub('', text)
    text = _MARKDOWN_QUOTE_PATTERN.sub('', text)
    text = _MARKDOWN_HORIZONTAL_RULE_PATTERN.sub('', text)
    return text.strip()
