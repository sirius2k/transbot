"""
TransBot 유틸리티 함수 모듈
"""
import tiktoken
import re


def detect_language(text: str) -> str:
    """텍스트의 언어를 자동 감지합니다. (한글/영어)"""
    if not text or not text.strip():
        return "unknown"

    # 한글 문자 확인 (가-힣)
    korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7a3')
    # 영문 알파벳 확인
    english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)

    # 전체 알파벳 문자 수
    total_alpha = korean_chars + english_chars

    if total_alpha == 0:
        return "unknown"

    # 한글이 50% 이상이면 한국어, 아니면 영어
    if korean_chars / total_alpha > 0.5:
        return "Korean"
    else:
        return "English"


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """텍스트의 토큰 수를 계산합니다."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def strip_markdown(text: str) -> str:
    """Markdown 포맷을 제거하고 순수 텍스트만 반환합니다."""
    # 코드 블록 제거 (```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 인라인 코드 제거 (`)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # 이미지 제거 ![alt](url) - 링크보다 먼저 처리
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    # 링크 제거 [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 볼드 제거 (**)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # 이탤릭 제거 (*)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # 헤딩 제거 (#)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # 리스트 기호 제거 (-, *, +)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    # 번호 리스트 제거 (1., 2., ...)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # 인용문 제거 (>)
    text = re.sub(r'^\s*>\s+', '', text, flags=re.MULTILINE)
    # 수평선 제거 (---, ___, ***)
    text = re.sub(r'^[-_*]{3,}$', '', text, flags=re.MULTILINE)

    return text.strip()


def translate(client, text: str, source: str, target: str, model: str) -> str:
    """OpenAI API를 사용하여 텍스트를 번역합니다."""
    response = client.chat.completions.create(
        model=model,
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
        temperature=0.3
    )
    return response.choices[0].message.content
