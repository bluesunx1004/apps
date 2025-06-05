import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch
from io import StringIO
from PyPDF2 import PdfReader

# 모델 로드 캐싱
@st.cache_resource
def load_model():
    model_name = "Helsinki-NLP/opus-mt-en-ko"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

st.title("📘 영어 ➜ 한국어 자동 번역기 (텍스트 & PDF)")
st.write("영어 텍스트 또는 PDF 문서를 업로드하면 한국어로 번역해 드립니다.")

# 입력 선택
option = st.radio("입력 방법을 선택하세요:", ["직접 입력", "텍스트 파일 업로드", "PDF 파일 업로드"])

input_text = ""

if option == "직접 입력":
    input_text = st.text_area("영어 텍스트를 입력하세요:", height=200)
elif option == "텍스트 파일 업로드":
    uploaded_txt = st.file_uploader("📄 .txt 파일 업로드", type=["txt"])
    if uploaded_txt is not None:
        input_text = uploaded_txt.read().decode("utf-8")
        st.code(input_text[:500] + ("..." if len(input_text) > 500 else ""), language="text")
else:
    uploaded_pdf = st.file_uploader("📄 PDF 파일 업로드", type=["pdf"])
    if uploaded_pdf is not None:
        try:
            reader = PdfReader(uploaded_pdf)
            pages = [page.extract_text() for page in reader.pages]
            input_text = "\n".join(pages)
            st.code(input_text[:500] + ("..." if len(input_text) > 500 else ""), language="text")
        except Exception as e:
            st.error(f"PDF에서 텍스트 추출 실패: {e}")

def translate(text):
    if not text.strip():
        return ""
    inputs = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt", truncation=True)
    translated = model.generate(**inputs)
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    return result

if st.button("🔄 번역하기"):
    if input_text.strip():
        with st.spinner("번역 중입니다... ⏳"):
            translated_text = translate(input_text)
        st.success("✅ 번역 완료!")
        st.text_area("📜 번역 결과 (한국어)", value=translated_text, height=300)

        # 번역 결과 다운로드 준비
        txt_buffer = StringIO()
        txt_buffer.write(translated_text)
        txt_buffer.seek(0)
        st.download_button(
            label="📥 번역 결과 텍스트 다운로드",
            data=txt_buffer,
            file_name="translated_result.txt",
            mime="text/plain"
        )
    else:
        st.warning("번역할 텍스트나 문서를 입력 또는 업로드해주세요.")
