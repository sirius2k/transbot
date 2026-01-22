import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="영어-한국어 번역기",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 영어-한국어 번역기")

# API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if not api_key:
        st.warning("OpenAI API 키를 입력해주세요.")
        st.stop()

client = OpenAI(api_key=api_key)

# 번역 방향 선택
direction = st.radio(
    "번역 방향을 선택하세요:",
    ["영어 → 한국어", "한국어 → 영어"],
    horizontal=True
)

# 입력 텍스트
if direction == "영어 → 한국어":
    placeholder = "Enter English text to translate..."
    source_lang = "English"
    target_lang = "Korean"
else:
    placeholder = "번역할 한국어 텍스트를 입력하세요..."
    source_lang = "Korean"
    target_lang = "English"

input_text = st.text_area("원문", placeholder=placeholder, height=150)

def translate(text: str, source: str, target: str) -> str:
    """OpenAI API를 사용하여 텍스트를 번역합니다."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following {source} text to {target}. Only respond with the translation, nothing else."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# 번역 버튼
if st.button("번역하기", type="primary", use_container_width=True):
    if input_text.strip():
        with st.spinner("번역 중..."):
            try:
                result = translate(input_text, source_lang, target_lang)
                st.subheader("번역 결과")
                st.text_area("번역문", value=result, height=150, disabled=True)
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
    else:
        st.warning("번역할 텍스트를 입력해주세요.")
