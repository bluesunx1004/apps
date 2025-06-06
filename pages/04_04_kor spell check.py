import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("📝 맞춤법 검사기 (부산대 기반 웹 요청)")

text = st.text_area("문장을 입력하세요:", height=150)

if st.button("검사하기"):
    if text.strip():
        with st.spinner("검사 중입니다..."):
            try:
                res = requests.post(
                    "https://speller.cs.pusan.ac.kr/results",
                    data={"text1": text},
                    timeout=10
                )
                soup = BeautifulSoup(res.text, "html.parser")
                suggestions = soup.select("table td > span.red")

                if suggestions:
                    st.success("✔️ 교정 제안 있음:")
                    for i, s in enumerate(suggestions, start=1):
                        st.markdown(f"**{i}.** {s.text}")
                else:
                    st.success("🎉 문장에서 교정할 부분이 없습니다!")

            except Exception as e:
                st.error(f"오류 발생: {e}")
    else:
        st.warning("문장을 입력해주세요.")
