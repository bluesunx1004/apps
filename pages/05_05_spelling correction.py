import streamlit as st
import openai
import os

# Streamlit 인터페이스
st.title("🧠 AI 한국어 맞춤법 검사기")

openai_api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")

text = st.text_area("검사할 문장을 입력하세요:", height=200)

if st.button("검사하기"):
    if not openai_api_key or not text.strip():
        st.warning("API 키와 문장을 모두 입력해주세요.")
    else:
        try:
            openai.api_key = openai_api_key

            prompt = f"""
다음 문장의 맞춤법과 띄어쓰기를 모두 교정해줘. 원래 문장은 그대로 두지 말고 수정된 문장만 출력해줘:

{text}
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )

            corrected_text = response.choices[0].message.content.strip()

            st.subheader("✅ 수정된 문장:")
            st.write(corrected_text)

        except Exception as e:
            st.error(f"오류 발생: {e}")
