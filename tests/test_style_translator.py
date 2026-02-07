"""
components/style_translator.py의 단위 테스트
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from components.style_translator import StyleTranslator


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI 클라이언트"""
    client = Mock()

    # Mock response 구조
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Mocked translation"

    client.chat.completions.create.return_value = mock_response

    return client


@pytest.fixture
def style_translator(mock_openai_client):
    """StyleTranslator 인스턴스"""
    return StyleTranslator(
        client=mock_openai_client,
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=2000,
        timeout=30
    )


class TestStyleTranslatorInit:
    """StyleTranslator 초기화 테스트"""

    def test_init_default_params(self, mock_openai_client):
        """기본 파라미터로 초기화 테스트"""
        translator = StyleTranslator(client=mock_openai_client)

        assert translator.client == mock_openai_client
        assert translator.model == "gpt-4o-mini"
        assert translator.temperature == 0.3
        assert translator.max_tokens == 2000
        assert translator.timeout == 30

    def test_init_custom_params(self, mock_openai_client):
        """커스텀 파라미터로 초기화 테스트"""
        translator = StyleTranslator(
            client=mock_openai_client,
            model="gpt-4o",
            temperature=0.5,
            max_tokens=3000,
            timeout=60
        )

        assert translator.model == "gpt-4o"
        assert translator.temperature == 0.5
        assert translator.max_tokens == 3000
        assert translator.timeout == 60

    def test_init_with_azure_deployment(self, mock_openai_client):
        """Azure deployment 파라미터로 초기화 테스트"""
        translator = StyleTranslator(
            client=mock_openai_client,
            model="gpt-4o-mini",
            deployment="my-deployment-name"
        )

        assert translator.deployment == "my-deployment-name"
        assert translator.model == "gpt-4o-mini"


class TestStyleConstants:
    """스타일 상수 테스트"""

    def test_style_constants_exist(self):
        """스타일 상수 존재 확인"""
        assert StyleTranslator.STYLE_CONVERSATIONAL == "conversational"
        assert StyleTranslator.STYLE_BUSINESS == "business"
        assert StyleTranslator.STYLE_FORMAL == "formal"
        assert StyleTranslator.STYLE_LITERAL == "literal"
        assert StyleTranslator.STYLE_CONCISE == "concise"

    def test_style_labels_complete(self):
        """모든 스타일에 대한 레이블 존재 확인"""
        labels = StyleTranslator.STYLE_LABELS

        assert "conversational" in labels
        assert "business" in labels
        assert "formal" in labels
        assert "literal" in labels
        assert "concise" in labels

        # 레이블에 이모지 포함 확인
        assert "📱" in labels["conversational"]
        assert "💼" in labels["business"]

    def test_style_instructions_complete(self):
        """모든 스타일에 대한 지침 존재 확인"""
        instructions = StyleTranslator.STYLE_INSTRUCTIONS

        assert "conversational" in instructions
        assert "business" in instructions
        assert "formal" in instructions
        assert "literal" in instructions
        assert "concise" in instructions

        # 지침이 영어로 작성되어 있는지 확인
        assert "English" in instructions["conversational"]


class TestTranslateSingleStyle:
    """단일 스타일 번역 테스트"""

    def test_translate_conversational_style(self, style_translator, mock_openai_client):
        """자연스러운 구어체 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Hey, how's it going?"

        result = style_translator.translate_single_style(
            text="안녕하세요, 어떻게 지내세요?",
            style=StyleTranslator.STYLE_CONVERSATIONAL
        )

        assert result == "Hey, how's it going?"
        assert mock_openai_client.chat.completions.create.called

    def test_translate_business_style(self, style_translator, mock_openai_client):
        """비즈니스 기본 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Thank you for your inquiry."

        result = style_translator.translate_single_style(
            text="문의해 주셔서 감사합니다.",
            style=StyleTranslator.STYLE_BUSINESS
        )

        assert result == "Thank you for your inquiry."

    def test_translate_formal_style(self, style_translator, mock_openai_client):
        """공식/문서용 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "We hereby acknowledge receipt of your application."

        result = style_translator.translate_single_style(
            text="귀하의 신청서를 수령하였음을 확인합니다.",
            style=StyleTranslator.STYLE_FORMAL
        )

        assert result == "We hereby acknowledge receipt of your application."

    def test_translate_literal_style(self, style_translator, mock_openai_client):
        """원문 유지 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "I am happy."

        result = style_translator.translate_single_style(
            text="나는 행복하다.",
            style=StyleTranslator.STYLE_LITERAL
        )

        assert result == "I am happy."

    def test_translate_concise_style(self, style_translator, mock_openai_client):
        """간결하게 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Got it."

        result = style_translator.translate_single_style(
            text="알겠습니다.",
            style=StyleTranslator.STYLE_CONCISE
        )

        assert result == "Got it."

    def test_translate_with_preserve_proper_nouns(self, style_translator, mock_openai_client):
        """고유명사 유지 옵션 테스트"""
        result = style_translator.translate_single_style(
            text="나는 서울에서 일합니다.",
            style=StyleTranslator.STYLE_BUSINESS,
            preserve_proper_nouns=True
        )

        # API 호출 시 고유명사 유지 지침이 포함되었는지 확인
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args[1]['messages'][0]['content']

        assert "Preserve all proper nouns" in system_message

    def test_translate_with_custom_instruction(self, style_translator, mock_openai_client):
        """커스텀 스타일 지침 테스트"""
        custom_instruction = "Translate in a humorous tone."

        result = style_translator.translate_single_style(
            text="안녕하세요",
            style=StyleTranslator.STYLE_BUSINESS,
            custom_instruction=custom_instruction
        )

        # API 호출 시 커스텀 지침이 사용되었는지 확인
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args[1]['messages'][0]['content']

        assert custom_instruction in system_message

    def test_translate_api_failure(self, style_translator, mock_openai_client):
        """API 호출 실패 시 에러 처리 테스트"""
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(Exception) as exc_info:
            style_translator.translate_single_style(
                text="안녕하세요",
                style=StyleTranslator.STYLE_BUSINESS
            )

        assert "API Error" in str(exc_info.value)

    def test_translate_with_azure_deployment(self, mock_openai_client):
        """Azure deployment 사용 시 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Thank you."

        translator = StyleTranslator(
            client=mock_openai_client,
            model="gpt-4o-mini",
            deployment="my-azure-deployment"
        )

        result = translator.translate_single_style(
            text="감사합니다",
            style=StyleTranslator.STYLE_BUSINESS
        )

        assert result == "Thank you."
        # API 호출 시 deployment가 사용되었는지 확인
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args[1]['model'] == "my-azure-deployment"


class TestTranslateMultiStyle:
    """다중 스타일 번역 테스트"""

    def test_translate_multi_style_success(self, style_translator, mock_openai_client):
        """다중 스타일 동시 번역 성공 테스트"""
        # Mock API 응답을 스타일별로 다르게 설정
        responses = ["Casual translation", "Business translation", "Formal translation"]
        mock_openai_client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content=resp))]) for resp in responses
        ]

        styles = [
            StyleTranslator.STYLE_CONVERSATIONAL,
            StyleTranslator.STYLE_BUSINESS,
            StyleTranslator.STYLE_FORMAL
        ]

        result = style_translator.translate_multi_style(
            text="안녕하세요",
            styles=styles
        )

        assert len(result) == 3
        assert "conversational" in result
        assert "business" in result
        assert "formal" in result

    def test_translate_multi_style_partial_failure(self, style_translator, mock_openai_client):
        """일부 스타일 번역 실패 시 처리 테스트"""
        # 첫 번째 스타일은 성공, 두 번째는 실패, 세 번째는 성공
        mock_openai_client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content="Success 1"))]),
            Exception("API Error"),
            Mock(choices=[Mock(message=Mock(content="Success 3"))])
        ]

        styles = [
            StyleTranslator.STYLE_CONVERSATIONAL,
            StyleTranslator.STYLE_BUSINESS,
            StyleTranslator.STYLE_FORMAL
        ]

        result = style_translator.translate_multi_style(
            text="안녕하세요",
            styles=styles
        )

        # 성공한 스타일은 결과 포함, 실패한 스타일은 에러 메시지
        assert result["conversational"] == "Success 1"
        assert "[business 번역 실패]" in result["business"]
        assert result["formal"] == "Success 3"

    def test_translate_multi_style_with_alternatives(self, style_translator, mock_openai_client):
        """대안 표현 포함 다중 번역 테스트"""
        # 기본 번역 + 대안 표현 응답 Mock
        mock_openai_client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content="Primary translation"))]),
            Mock(choices=[Mock(message=Mock(content="Alternative 1\nAlternative 2"))])
        ]

        result = style_translator.translate_multi_style(
            text="안녕하세요",
            styles=[StyleTranslator.STYLE_CONVERSATIONAL],
            include_alternatives=True
        )

        assert "conversational" in result
        assert "primary" in result["conversational"]
        assert "alternatives" in result["conversational"]
        assert len(result["conversational"]["alternatives"]) == 2


class TestTranslateEnglishToKorean:
    """영어→한국어 번역 스타일 테스트"""

    def test_translate_en_to_ko_conversational(self, style_translator, mock_openai_client):
        """영→한 자연스러운 구어체 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "안녕, 어떻게 지내?"

        result = style_translator.translate_single_style(
            text="Hey, how's it going?",
            style=StyleTranslator.STYLE_CONVERSATIONAL,
            source_lang="English",
            target_lang="Korean"
        )

        assert result == "안녕, 어떻게 지내?"

        # API 호출 시 한국어 지침이 사용되었는지 확인
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args[1]['messages'][0]['content']
        assert "구어체 한국어" in system_message

    def test_translate_en_to_ko_literal(self, style_translator, mock_openai_client):
        """영→한 직역 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "나는 행복하다."

        result = style_translator.translate_single_style(
            text="I am happy.",
            style=StyleTranslator.STYLE_LITERAL,
            source_lang="English",
            target_lang="Korean"
        )

        assert result == "나는 행복하다."

        # 직역 지침 확인
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args[1]['messages'][0]['content']
        assert "직역" in system_message

    def test_translate_en_to_ko_business(self, style_translator, mock_openai_client):
        """영→한 비즈니스 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "문의해 주셔서 감사합니다."

        result = style_translator.translate_single_style(
            text="Thank you for your inquiry.",
            style=StyleTranslator.STYLE_BUSINESS,
            source_lang="English",
            target_lang="Korean"
        )

        assert result == "문의해 주셔서 감사합니다."

    def test_translate_en_to_ko_formal(self, style_translator, mock_openai_client):
        """영→한 공식/문서용 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "귀하의 신청서를 수령하였음을 확인합니다."

        result = style_translator.translate_single_style(
            text="We hereby acknowledge receipt of your application.",
            style=StyleTranslator.STYLE_FORMAL,
            source_lang="English",
            target_lang="Korean"
        )

        assert result == "귀하의 신청서를 수령하였음을 확인합니다."

    def test_translate_en_to_ko_concise(self, style_translator, mock_openai_client):
        """영→한 간결하게 번역 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "알겠습니다."

        result = style_translator.translate_single_style(
            text="I understand what you're saying.",
            style=StyleTranslator.STYLE_CONCISE,
            source_lang="English",
            target_lang="Korean"
        )

        assert result == "알겠습니다."

    def test_translate_multi_style_en_to_ko(self, style_translator, mock_openai_client):
        """영→한 다중 스타일 동시 번역 테스트"""
        responses = ["안녕!", "안녕하세요.", "안녕하십니까."]
        mock_openai_client.chat.completions.create.side_effect = [
            Mock(choices=[Mock(message=Mock(content=resp))]) for resp in responses
        ]

        styles = [
            StyleTranslator.STYLE_CONVERSATIONAL,
            StyleTranslator.STYLE_BUSINESS,
            StyleTranslator.STYLE_FORMAL
        ]

        result = style_translator.translate_multi_style(
            text="Hello",
            styles=styles,
            source_lang="English",
            target_lang="Korean"
        )

        assert len(result) == 3
        assert "conversational" in result
        assert "business" in result
        assert "formal" in result

    def test_translate_target_lang_variations(self, style_translator, mock_openai_client):
        """target_lang의 다양한 표기 테스트 (Korean, 한국어)"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "안녕하세요"

        # "Korean" 표기
        result1 = style_translator.translate_single_style(
            text="Hello",
            style=StyleTranslator.STYLE_BUSINESS,
            source_lang="English",
            target_lang="Korean"
        )

        # "한국어" 표기
        result2 = style_translator.translate_single_style(
            text="Hello",
            style=StyleTranslator.STYLE_BUSINESS,
            source_lang="English",
            target_lang="한국어"
        )

        # 두 표기 모두 영→한 지침 사용
        assert result1 == "안녕하세요"
        assert result2 == "안녕하세요"


class TestStyleInstructionsEnToKo:
    """영→한 스타일 지침 상수 테스트"""

    def test_style_instructions_en_to_ko_complete(self):
        """영→한 스타일 지침 완전성 테스트"""
        instructions = StyleTranslator.STYLE_INSTRUCTIONS_EN_TO_KO

        assert "conversational" in instructions
        assert "business" in instructions
        assert "formal" in instructions
        assert "literal" in instructions
        assert "concise" in instructions

        # 지침이 한국어로 작성되어 있는지 확인
        assert "한국어" in instructions["conversational"]
        assert "직역" in instructions["literal"]


class TestGenerateAlternatives:
    """대안 표현 생성 테스트"""

    def test_generate_alternatives_success(self, style_translator, mock_openai_client):
        """대안 표현 생성 성공 테스트"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Alternative 1\nAlternative 2\nAlternative 3"

        result = style_translator._generate_alternatives(
            text="안녕하세요",
            base_translation="Hello",
            style=StyleTranslator.STYLE_CONVERSATIONAL,
            source_lang="Korean",
            target_lang="English"
        )

        assert len(result) == 3
        assert "Alternative 1" in result
        assert "Alternative 2" in result
        assert "Alternative 3" in result

    def test_generate_alternatives_max_three(self, style_translator, mock_openai_client):
        """대안 표현 최대 3개 제한 테스트"""
        # 5개 대안을 반환하지만 최대 3개만 사용
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Alt 1\nAlt 2\nAlt 3\nAlt 4\nAlt 5"

        result = style_translator._generate_alternatives(
            text="안녕하세요",
            base_translation="Hello",
            style=StyleTranslator.STYLE_CONVERSATIONAL,
            source_lang="Korean",
            target_lang="English"
        )

        assert len(result) == 3

    def test_generate_alternatives_failure(self, style_translator, mock_openai_client):
        """대안 표현 생성 실패 시 빈 리스트 반환 테스트"""
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        result = style_translator._generate_alternatives(
            text="안녕하세요",
            base_translation="Hello",
            style=StyleTranslator.STYLE_CONVERSATIONAL,
            source_lang="Korean",
            target_lang="English"
        )

        assert result == []
