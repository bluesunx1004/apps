import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("📝 네이버 맞춤법 검사기 (Streamlit)")

user_input = st.text_area("문장을 입력하세요:", height=150)

if st.button("검사하기"):
    if user_input.strip():
        with st.spinner("맞춤법 검사 중..."):
            try:
                url = "https://search.naver.com/search.naver"
                params = {
                    "query": f"{user_input} 맞춤법 검사"
                }
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                response = requests.get(url, params=params, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                result = soup.select_one("div._check_result_box > div:nth-of-type(1)").get_text(strip=True)
                st.success("✔️ 검사 결과")
                st.markdown(f"**수정 제안:**  \n{result}")
            except Exception as e:
                st.error(f"검사 중 오류 발생: {e}")
    else:
        st.warning("검사할 문장을 입력해주세요.")
