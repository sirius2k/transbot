"""app.py 함수 테스트"""
import pytest
from unittest.mock import Mock, patch


class TestFormatTranslationResult:
    """format_translation_result() 함수 테스트"""

    def test_single_line_with_content(self):
        """한 줄 텍스트에 두 공백 추가"""
        from app import format_translation_result

        text = "Hello World"
        result = format_translation_result(text)

        assert result == "Hello World  "

    def test_multiple_lines_with_content(self):
        """여러 줄 텍스트의 각 줄에 두 공백 추가"""
        from app import format_translation_result

        text = "Line 1\nLine 2\nLine 3"
        result = format_translation_result(text)

        expected = "Line 1  \nLine 2  \nLine 3  "
        assert result == expected

    def test_empty_lines_preserved(self):
        """빈 줄은 공백 없이 보존"""
        from app import format_translation_result

        text = "Line 1\n\nLine 2"
        result = format_translation_result(text)

        expected = "Line 1  \n\nLine 2  "
        assert result == expected

    def test_whitespace_only_lines(self):
        """공백만 있는 줄은 두 공백 추가하지 않음"""
        from app import format_translation_result

        text = "Line 1\n   \nLine 2"
        result = format_translation_result(text)

        expected = "Line 1  \n   \nLine 2  "
        assert result == expected

    def test_mixed_content_and_empty_lines(self):
        """콘텐츠 줄과 빈 줄이 혼합된 경우"""
        from app import format_translation_result

        text = "Paragraph 1\n\nParagraph 2\n  \nParagraph 3"
        result = format_translation_result(text)

        expected = "Paragraph 1  \n\nParagraph 2  \n  \nParagraph 3  "
        assert result == expected

    def test_trailing_newline(self):
        """끝에 개행이 있는 경우"""
        from app import format_translation_result

        text = "Line 1\nLine 2\n"
        result = format_translation_result(text)

        expected = "Line 1  \nLine 2  \n"
        assert result == expected

    def test_indented_lines(self):
        """들여쓰기된 줄도 두 공백 추가"""
        from app import format_translation_result

        text = "Normal line\n    Indented line\n        Double indented"
        result = format_translation_result(text)

        expected = "Normal line  \n    Indented line  \n        Double indented  "
        assert result == expected

    def test_empty_string(self):
        """빈 문자열은 빈 문자열 반환"""
        from app import format_translation_result

        text = ""
        result = format_translation_result(text)

        assert result == ""

    def test_only_newlines(self):
        """개행만 있는 경우"""
        from app import format_translation_result

        text = "\n\n\n"
        result = format_translation_result(text)

        expected = "\n\n\n"
        assert result == expected

    def test_markdown_list_preserved(self):
        """마크다운 리스트 형식이 보존됨"""
        from app import format_translation_result

        text = "- Item 1\n- Item 2\n- Item 3"
        result = format_translation_result(text)

        expected = "- Item 1  \n- Item 2  \n- Item 3  "
        assert result == expected

    def test_code_block_preserved(self):
        """코드 블록 형식이 보존됨"""
        from app import format_translation_result

        text = "```python\nprint('hello')\nprint('world')\n```"
        result = format_translation_result(text)

        expected = "```python  \nprint('hello')  \nprint('world')  \n```  "
        assert result == expected


class TestSetupSidebarOpenAI:
    """setup_sidebar() OpenAI Provider 테스트"""

    @pytest.fixture
    def mock_streamlit(self):
        """Streamlit 컴포넌트 mock"""
        with patch('app.st') as mock_st:
            mock_st.sidebar.header = Mock()
            mock_st.sidebar.markdown = Mock()
            mock_st.sidebar.selectbox = Mock()
            mock_st.sidebar.error = Mock()
            mock_st.stop = Mock()
            yield mock_st

    @pytest.fixture
    def mock_config(self):
        """Config mock"""
        with patch('app.config') as mock_cfg:
            mock_cfg.DEFAULT_MODEL = "gpt-4o-mini"
            # get_available_openai_models() mock 추가
            mock_cfg.get_available_openai_models.return_value = {
                "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
                "GPT-4o (최고 품질)": "gpt-4o",
                "GPT-4 Turbo": "gpt-4-turbo",
                "GPT-4": "gpt-4",
                "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
            }
            yield mock_cfg

    def test_openai_returns_model_and_options(self, mock_streamlit, mock_config):
        """OpenAI provider로 호출 시 모델 목록 반환"""
        from app import setup_sidebar

        # selectbox가 "GPT-4o Mini (추천 - 가성비)" 반환하도록 설정
        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        selected_model, model_options = setup_sidebar("openai")

        # 선택된 모델이 올바르게 반환됨
        assert selected_model == "gpt-4o-mini"

        # 모델 옵션 딕셔너리가 올바르게 반환됨
        expected_options = {
            "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
            "GPT-4o (최고 품질)": "gpt-4o",
            "GPT-4 Turbo": "gpt-4-turbo",
            "GPT-4": "gpt-4",
            "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
        }
        assert model_options == expected_options

    def test_openai_default_model_selected(self, mock_streamlit, mock_config):
        """DEFAULT_MODEL에 해당하는 모델이 기본 선택됨"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # selectbox가 호출되었는지 확인
        mock_streamlit.sidebar.selectbox.assert_called_once()

        # index=0이 전달되었는지 확인 (gpt-4o-mini가 첫 번째)
        call_args = mock_streamlit.sidebar.selectbox.call_args
        assert call_args.kwargs["index"] == 0

    def test_openai_default_model_gpt4o(self, mock_streamlit, mock_config):
        """DEFAULT_MODEL이 gpt-4o일 때 두 번째 인덱스 선택"""
        from app import setup_sidebar

        # Config의 DEFAULT_MODEL을 gpt-4o로 변경
        mock_config.DEFAULT_MODEL = "gpt-4o"
        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o (최고 품질)"

        setup_sidebar("openai")

        # index=1이 전달되었는지 확인 (gpt-4o가 두 번째)
        call_args = mock_streamlit.sidebar.selectbox.call_args
        assert call_args.kwargs["index"] == 1

    def test_openai_ui_rendering(self, mock_streamlit, mock_config):
        """OpenAI provider 사용 시 '🔵 OpenAI' 표시"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # Provider 정보가 올바르게 표시되는지 확인
        mock_streamlit.sidebar.markdown.assert_any_call("**Provider:** 🔵 OpenAI")


class TestSetupSidebarAzure:
    """setup_sidebar() Azure Provider 테스트"""

    @pytest.fixture
    def mock_streamlit(self):
        """Streamlit 컴포넌트 mock"""
        with patch('app.st') as mock_st:
            mock_st.sidebar.header = Mock()
            mock_st.sidebar.markdown = Mock()
            mock_st.sidebar.selectbox = Mock()
            mock_st.sidebar.error = Mock()
            mock_st.stop = Mock()
            yield mock_st

    @pytest.fixture
    def mock_config(self):
        """Config mock"""
        with patch('app.config') as mock_cfg:
            mock_cfg.DEFAULT_MODEL = "gpt-4o-mini"
            yield mock_cfg

    @pytest.fixture
    def mock_azure_deployments(self):
        """Azure deployments mock"""
        deployments = {
            "gpt-4o": "my-gpt4o-deployment",
            "gpt-4o-mini": "my-mini-deployment",
            "gpt-4-turbo": "my-turbo-deployment"
        }

        with patch('components.translation.AzureTranslationManager') as mock_azure:
            mock_azure.SUPPORTED_DEPLOYMENTS = deployments
            yield mock_azure

    def test_azure_returns_deployment_and_options(
        self, mock_streamlit, mock_config, mock_azure_deployments
    ):
        """Azure provider로 호출 시 deployment 목록 반환"""
        from app import setup_sidebar

        # selectbox가 "gpt-4o-mini (Azure)" 반환하도록 설정
        mock_streamlit.sidebar.selectbox.return_value = "gpt-4o-mini (Azure)"

        selected_deployment, deployment_options = setup_sidebar("azure")

        # 선택된 deployment가 올바르게 반환됨
        assert selected_deployment == "my-mini-deployment"

        # Deployment 옵션 딕셔너리가 올바르게 반환됨
        expected_options = {
            "gpt-4o (Azure)": "my-gpt4o-deployment",
            "gpt-4o-mini (Azure)": "my-mini-deployment",
            "gpt-4-turbo (Azure)": "my-turbo-deployment"
        }
        assert deployment_options == expected_options

    def test_azure_default_model_selected(
        self, mock_streamlit, mock_config, mock_azure_deployments
    ):
        """DEFAULT_MODEL에 해당하는 deployment가 기본 선택됨"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "gpt-4o-mini (Azure)"

        setup_sidebar("azure")

        # selectbox가 호출되었는지 확인
        mock_streamlit.sidebar.selectbox.assert_called_once()

        # index=1이 전달되었는지 확인 (gpt-4o-mini가 두 번째)
        call_args = mock_streamlit.sidebar.selectbox.call_args
        assert call_args.kwargs["index"] == 1

    def test_azure_default_model_gpt4o(
        self, mock_streamlit, mock_config, mock_azure_deployments
    ):
        """DEFAULT_MODEL이 gpt-4o일 때 첫 번째 인덱스 선택"""
        from app import setup_sidebar

        # Config의 DEFAULT_MODEL을 gpt-4o로 변경
        mock_config.DEFAULT_MODEL = "gpt-4o"
        mock_streamlit.sidebar.selectbox.return_value = "gpt-4o (Azure)"

        setup_sidebar("azure")

        # index=0이 전달되었는지 확인 (gpt-4o가 첫 번째)
        call_args = mock_streamlit.sidebar.selectbox.call_args
        assert call_args.kwargs["index"] == 0

    def test_azure_empty_deployments_error(self, mock_streamlit, mock_config):
        """SUPPORTED_DEPLOYMENTS가 비어있을 경우 st.stop() 호출"""
        from streamlit.runtime.scriptrunner import StopException
        from app import setup_sidebar

        # 빈 deployment 딕셔너리
        with patch('components.translation.AzureTranslationManager') as mock_azure:
            mock_azure.SUPPORTED_DEPLOYMENTS = {}

            # st.stop()이 호출되면 StopException 발생하도록 설정
            mock_streamlit.stop.side_effect = StopException()

            # StopException이 발생해야 함
            with pytest.raises(StopException):
                setup_sidebar("azure")

            # 에러 메시지가 표시되었는지 확인
            mock_streamlit.sidebar.error.assert_called_once()
            error_message = mock_streamlit.sidebar.error.call_args[0][0]
            assert "Azure Deployment 미설정" in error_message
            assert "AZURE_DEPLOYMENTS" in error_message

            # st.stop()이 호출되었는지 확인
            mock_streamlit.stop.assert_called_once()

    def test_azure_ui_rendering(
        self, mock_streamlit, mock_config, mock_azure_deployments
    ):
        """Azure provider 사용 시 '🟢 Azure OpenAI' 표시"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "gpt-4o-mini (Azure)"

        setup_sidebar("azure")

        # Provider 정보가 올바르게 표시되는지 확인
        mock_streamlit.sidebar.markdown.assert_any_call("**Provider:** 🟢 Azure OpenAI")


class TestSetupSidebarEdgeCases:
    """setup_sidebar() 엣지 케이스 테스트"""

    @pytest.fixture
    def mock_streamlit(self):
        """Streamlit 컴포넌트 mock"""
        with patch('app.st') as mock_st:
            mock_st.sidebar.header = Mock()
            mock_st.sidebar.markdown = Mock()
            mock_st.sidebar.selectbox = Mock()
            mock_st.sidebar.error = Mock()
            mock_st.stop = Mock()
            yield mock_st

    @pytest.fixture
    def mock_config(self):
        """Config mock"""
        with patch('app.config') as mock_cfg:
            mock_cfg.DEFAULT_MODEL = "gpt-4o-mini"
            # get_available_openai_models() mock 추가
            mock_cfg.get_available_openai_models.return_value = {
                "GPT-4o Mini (추천 - 가성비)": "gpt-4o-mini",
                "GPT-4o (최고 품질)": "gpt-4o",
                "GPT-4 Turbo": "gpt-4-turbo",
                "GPT-4": "gpt-4",
                "GPT-3.5 Turbo (빠름)": "gpt-3.5-turbo"
            }
            yield mock_cfg

    def test_openai_unknown_default_model(self, mock_streamlit, mock_config):
        """DEFAULT_MODEL이 목록에 없을 때 첫 번째 모델 선택"""
        from app import setup_sidebar

        # Config의 DEFAULT_MODEL을 존재하지 않는 모델로 설정
        mock_config.DEFAULT_MODEL = "gpt-5o"
        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # index=0이 전달되었는지 확인 (기본값)
        call_args = mock_streamlit.sidebar.selectbox.call_args
        assert call_args.kwargs["index"] == 0

    def test_azure_unknown_default_model(self, mock_streamlit, mock_config):
        """Azure에서 DEFAULT_MODEL이 deployment 목록에 없을 때 첫 번째 선택"""
        from app import setup_sidebar

        deployments = {
            "gpt-4o": "my-gpt4o-deployment",
            "gpt-4-turbo": "my-turbo-deployment"
        }

        with patch('components.translation.AzureTranslationManager') as mock_azure:
            mock_azure.SUPPORTED_DEPLOYMENTS = deployments

            # DEFAULT_MODEL을 deployment 목록에 없는 모델로 설정
            mock_config.DEFAULT_MODEL = "gpt-3.5-turbo"
            mock_streamlit.sidebar.selectbox.return_value = "gpt-4o (Azure)"

            setup_sidebar("azure")

            # index=0이 전달되었는지 확인 (기본값)
            call_args = mock_streamlit.sidebar.selectbox.call_args
            assert call_args.kwargs["index"] == 0

    def test_openai_selectbox_options_order(self, mock_streamlit, mock_config):
        """OpenAI selectbox 옵션이 올바른 순서로 전달됨"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # selectbox에 전달된 옵션 확인
        call_args = mock_streamlit.sidebar.selectbox.call_args
        options = call_args.kwargs["options"]

        expected_order = [
            "GPT-4o Mini (추천 - 가성비)",
            "GPT-4o (최고 품질)",
            "GPT-4 Turbo",
            "GPT-4",
            "GPT-3.5 Turbo (빠름)"
        ]
        assert options == expected_order

    def test_azure_selectbox_options_order(self, mock_streamlit, mock_config):
        """Azure selectbox 옵션이 딕셔너리 순서대로 전달됨"""
        from app import setup_sidebar

        # 순서가 명확한 deployment 딕셔너리 (Python 3.7+에서 딕셔너리는 순서 보장)
        deployments = {
            "gpt-4o": "deploy1",
            "gpt-4o-mini": "deploy2",
            "gpt-4-turbo": "deploy3"
        }

        with patch('components.translation.AzureTranslationManager') as mock_azure:
            mock_azure.SUPPORTED_DEPLOYMENTS = deployments

            mock_streamlit.sidebar.selectbox.return_value = "gpt-4o (Azure)"

            setup_sidebar("azure")

            # selectbox에 전달된 옵션 확인
            call_args = mock_streamlit.sidebar.selectbox.call_args
            options = call_args.kwargs["options"]

            expected_order = [
                "gpt-4o (Azure)",
                "gpt-4o-mini (Azure)",
                "gpt-4-turbo (Azure)"
            ]
            assert options == expected_order

    def test_sidebar_header_called(self, mock_streamlit, mock_config):
        """사이드바 헤더가 올바르게 호출됨"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # 헤더가 호출되었는지 확인
        mock_streamlit.sidebar.header.assert_called_once_with("⚙️ 영어-한국어 번역기 설정")

    def test_sidebar_divider_called(self, mock_streamlit, mock_config):
        """사이드바 구분선이 올바르게 호출됨"""
        from app import setup_sidebar

        mock_streamlit.sidebar.selectbox.return_value = "GPT-4o Mini (추천 - 가성비)"

        setup_sidebar("openai")

        # 구분선(---)이 호출되었는지 확인
        mock_streamlit.sidebar.markdown.assert_any_call("---")
