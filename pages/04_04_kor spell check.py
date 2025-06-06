import streamlit as st
import requests

def check_spelling(text):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "text1": text
    }
    res = requests.post("https://speller.cs.pusan.ac.kr/results", data=data, headers=headers)
    return res.text

st.title("📝 한글 맞춤법 검사기 (직접 API 호출)")

user_input = st.text_area("검사할 문장을 입력하세요:", height=150)

if st.button("맞춤법 검사"):
    if user_input.strip():
        try:
            html_result = check_spelling(user_input)
            st.markdown("✅ **API 호출 성공**")
            st.markdown("원시 HTML 응답 내용 일부:")
            st.code(html_result[:500])  # 일부만 출력
            st.warning("※ 이 방식은 HTML 파싱이 필요합니다. 예쁘게 출력하려면 추가 처리가 필요해요.")
        except Exception as e:
            st.error(f"API 호출 중 오류 발생: {e}")
