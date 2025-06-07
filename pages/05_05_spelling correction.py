import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def check_spelling(text):
    url = "https://search.naver.com/search.naver"
    params = {
        "query": text,
        "where": "nexearch",
        "sm": "top_hty",
        "fbm": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    result = soup.find("span", {"class": "ss_suggest"})
    if result:
        return result.get_text()
    else:
        return text  # 수정 제안 없으면 원문 그대로

# Streamlit 인터페이스
st.title("📝 네이버 맞춤법 검사기 (비공식)")

user_text = st.text_area("검사할 문장을 입력하세요:", height=200)

if st.button("맞춤법 검사"):
    if not user_text.strip():
        st.warning("텍스트를 입력해주세요.")
    else:
        try:
            corrected = check_spelling(user_text)
            if corrected == user_text:
                st.success("맞춤법 수정이 필요하지 않습니다.")
            else:
                st.subheader("✅ 수정된 문장:")
                st.write(corrected)
        except Exception as e:
            st.error(f"오류 발생: {e}")
