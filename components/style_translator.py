"""다양한 스타일로 번역을 생성하는 모듈

이 모듈은 한국어→영어 번역 시 다양한 번역 스타일(구어체, 비즈니스, 공식, 원문 유지, 간결)을
제공하는 StyleTranslator 클래스를 포함합니다.
"""

import logging
from typing import List, Dict, Optional, Union
from openai import OpenAI

logger = logging.getLogger("transbot.style_translator")


class StyleTranslator:
    """다양한 스타일로 번역을 생성하는 클래스"""

    # 스타일 상수 및 정의
    STYLE_CONVERSATIONAL = "conversational"  # 자연스러운 구어체
    STYLE_BUSINESS = "business"  # 비즈니스 기본
    STYLE_FORMAL = "formal"  # 공식/문서용
    STYLE_LITERAL = "literal"  # 원문 유지
    STYLE_CONCISE = "concise"  # 간결하게

    STYLE_LABELS = {
        STYLE_CONVERSATIONAL: "📱 자연스러운 구어체",
        STYLE_BUSINESS: "💼 비즈니스 기본",
        STYLE_FORMAL: "📋 공식/문서용",
        STYLE_LITERAL: "📝 원문 유지",
        STYLE_CONCISE: "✂️ 간결하게"
    }

    STYLE_INSTRUCTIONS = {
        STYLE_CONVERSATIONAL: "Use natural, conversational English as if speaking with a friend.",
        STYLE_BUSINESS: "Use standard business English, professional but not overly formal.",
        STYLE_FORMAL: "Use formal, official English suitable for documents and reports.",
        STYLE_LITERAL: "Translate literally, preserving the original structure and meaning as much as possible.",
        STYLE_CONCISE: "Translate concisely, conveying only the core message."
    }

    def __init__(
        self,
        client: OpenAI,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 2000,
        timeout: int = 30
    ):
        """
        Args:
            client: OpenAI 클라이언트
            model: 사용할 AI 모델
            temperature: 생성 온도 (0-1)
            max_tokens: 최대 토큰 수
            timeout: 타임아웃 (초)
        """
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def translate_single_style(
        self,
        text: str,
        style: str,
        source_lang: str = "Korean",
        target_lang: str = "English",
        preserve_proper_nouns: bool = False,
        custom_instruction: Optional[str] = None
    ) -> str:
        """단일 스타일로 번역

        Args:
            text: 번역할 텍스트
            style: 스타일 키 (STYLE_* 상수 중 하나)
            source_lang: 원본 언어
            target_lang: 대상 언어
            preserve_proper_nouns: 고유명사 유지 여부
            custom_instruction: 커스텀 스타일 지침 (있으면 style 무시)

        Returns:
            번역된 텍스트

        Raises:
            Exception: API 호출 실패 시
        """
        try:
            # 스타일 지침 생성
            if custom_instruction:
                style_instruction = custom_instruction
            else:
                style_instruction = self.STYLE_INSTRUCTIONS.get(
                    style,
                    self.STYLE_INSTRUCTIONS[self.STYLE_BUSINESS]  # 기본값
                )

            # 고유명사 유지 옵션
            proper_noun_instruction = ""
            if preserve_proper_nouns:
                proper_noun_instruction = "\nIMPORTANT: Preserve all proper nouns (names, places, brands) in their original form."

            # 시스템 프롬프트 구성
            system_prompt = f"""You are a professional translator. Translate the following {source_lang} text to {target_lang}.
IMPORTANT: Preserve all Markdown formatting exactly as it appears in the original text.

STYLE INSTRUCTION: {style_instruction}{proper_noun_instruction}

Only respond with the translation, nothing else."""

            # API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )

            translation = response.choices[0].message.content

            logger.info(
                "스타일 번역 완료",
                extra={
                    "style": style,
                    "input_length": len(text),
                    "output_length": len(translation)
                }
            )

            return translation

        except Exception as e:
            logger.error(
                f"{style} 스타일 번역 실패",
                extra={"error": str(e)},
                exc_info=True
            )
            raise

    def translate_multi_style(
        self,
        text: str,
        styles: List[str],
        source_lang: str = "Korean",
        target_lang: str = "English",
        preserve_proper_nouns: bool = False,
        include_alternatives: bool = False
    ) -> Dict[str, Union[str, Dict[str, Union[str, List[str]]]]]:
        """여러 스타일로 번역 생성

        Args:
            text: 번역할 텍스트
            styles: 스타일 키 리스트
            source_lang: 원본 언어
            target_lang: 대상 언어
            preserve_proper_nouns: 고유명사 유지 여부
            include_alternatives: 대안 표현 포함 여부 (각 스타일당 2-3개)

        Returns:
            {
                "conversational": "번역 결과 1",
                "business": "번역 결과 2",
                ...
            }
            또는 include_alternatives=True인 경우:
            {
                "conversational": {
                    "primary": "번역 결과",
                    "alternatives": ["대안1", "대안2"]
                },
                ...
            }
        """
        results = {}

        logger.info(
            "다중 스타일 번역 시작",
            extra={
                "styles": styles,
                "include_alternatives": include_alternatives
            }
        )

        for style in styles:
            try:
                translation = self.translate_single_style(
                    text=text,
                    style=style,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    preserve_proper_nouns=preserve_proper_nouns
                )

                # 대안 표현 생성 (옵션)
                if include_alternatives:
                    alternatives = self._generate_alternatives(
                        text=text,
                        base_translation=translation,
                        style=style,
                        source_lang=source_lang,
                        target_lang=target_lang
                    )
                    results[style] = {
                        "primary": translation,
                        "alternatives": alternatives
                    }
                else:
                    results[style] = translation

            except Exception as e:
                logger.error(
                    f"{style} 스타일 번역 실패, 건너뜀",
                    extra={"error": str(e)}
                )
                results[style] = f"[{style} 번역 실패]"

        return results

    def auto_select_styles_for_short_text(self, text: str) -> List[str]:
        """짧은 텍스트에 적합한 스타일 자동 선택

        Args:
            text: 분석할 텍스트

        Returns:
            추천 스타일 리스트 (2-3개)
        """
        # 간단한 휴리스틱: 대화체는 구어체 + 간결하게 추천
        # 향후 AI 기반 분석으로 개선 가능

        # 기본 추천
        recommended = [
            self.STYLE_CONVERSATIONAL,
            self.STYLE_CONCISE
        ]

        # 비즈니스 키워드 감지 시 비즈니스 스타일 추가
        business_keywords = ["회의", "보고", "프로젝트", "일정", "업무"]
        if any(keyword in text for keyword in business_keywords):
            recommended.append(self.STYLE_BUSINESS)
        else:
            # 일반 대화는 구어체 + 간결하게만
            pass

        logger.info(
            "자동 스타일 선택 완료",
            extra={"recommended_styles": recommended}
        )

        return recommended

    def _generate_alternatives(
        self,
        text: str,
        base_translation: str,
        style: str,
        source_lang: str,
        target_lang: str
    ) -> List[str]:
        """동일 스타일 내에서 대안 표현 생성

        Args:
            text: 원본 텍스트
            base_translation: 기본 번역
            style: 스타일
            source_lang: 원본 언어
            target_lang: 대상 언어

        Returns:
            대안 표현 리스트 (2-3개)
        """
        try:
            style_instruction = self.STYLE_INSTRUCTIONS.get(style, "")

            prompt = f"""Given this translation:
"{base_translation}"

Provide 2-3 alternative ways to express the same meaning in {target_lang}, following this style: {style_instruction}

Only output the alternatives, one per line, without numbering or explanation."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator providing alternative expressions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # 다양성을 위해 높은 온도
                max_tokens=500,
                timeout=self.timeout
            )

            alternatives_text = response.choices[0].message.content
            alternatives = [line.strip() for line in alternatives_text.split('\n') if line.strip()]

            logger.info(
                "대안 표현 생성 완료",
                extra={"style": style, "count": len(alternatives)}
            )

            return alternatives[:3]  # 최대 3개

        except Exception as e:
            logger.error(
                "대안 표현 생성 실패",
                extra={"error": str(e)}
            )
            return []
