import streamlit as st
from googletrans import Translator
from PyPDF2 import PdfReader
from io import StringIO

translator = Translator()

st.title("📘 자동 번역기 (영어 ↔ 한국어)")

# 번역 방향 선택
direction = st.selectbox("번역 방향을 선택하세요:", ["영어 ➡️ 한국어", "한국어 ➡️ 영어"])

# 번역 방향 설정
if direction == "영어 ➡️ 한국어":
    src_lang = "en"
    dest_lang = "ko"
else:
    src_lang = "ko"
    dest_lang = "en"

# 입력 방법 선택
option = st.radio("입력 방법 선택:", ["직접 입력", "PDF 파일 업로드"])

input_text = ""

if option == "직접 입력":
    input_text = st.text_area(f"{src_lang.upper()} 텍스트를 입력하세요:", height=200)

elif option == "PDF 파일 업로드":
    uploaded_pdf = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])
    if uploaded_pdf is not None:
        try:
            reader = PdfReader(uploaded_pdf)
            pages = [page.extract_text() for page in reader.pages]
            input_text = "\n".join(pages)
            st.code(input_text[:500] + ("..." if len(input_text) > 500 else ""), language="text")
        except Exception as e:
            st.error(f"PDF 텍스트 추출 실패: {e}")

# 번역 버튼
if st.button("🔄 번역하기"):
    if input_text.strip():
        with st.spinner("번역 중입니다... ⏳"):
            try:
                translated = translator.translate(input_text, src=src_lang, dest=dest_lang)
                translated_text = translated.text
                st.success("✅ 번역 완료!")
                st.text_area(f"📜 번역 결과 ({dest_lang.upper()})", value=translated_text, height=300)

                # 다운로드 버튼
                st.download_button(
                    label="📥 번역 결과 텍스트 다운로드",
                    data=translated_text,
                    file_name="translated_result.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"번역 중 오류 발생: {e}")
    else:
        st.warning("번역할 텍스트를 입력하거나 PDF를 업로드 해주세요.")
