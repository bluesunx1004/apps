import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_spelling(text):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"text1": text}
    res = requests.post("https://speller.cs.pusan.ac.kr/results", data=data, headers=headers)

    # HTML 응답 파싱
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for err in soup.select("table td[style*='color:red']"):
        parent_row = err.find_parent("tr")
        original = err.text.strip()
        suggestion = parent_row.find_all("td")[2].text.strip()
        results.append((original, suggestion))

    # 교정된 문장 추출
    fixed = soup.find("textarea", {"id": "text1"}).text
    return fixed, results

st.set_page_config(page_title="한글 맞춤법 검사기", page_icon="📝")
st.title("📝 한글 맞춤법 검사기 (BeautifulSoup 기반)")

user_input = st.text_area("검사할 문장을 입력하세요:", height=200)

if st.button("맞춤법 검사"):
    if user_input.strip():
        with st.spinner("검사 중입니다..."):
            try:
                corrected_text, errors = check_spelling(user_input)

                st.markdown("### ✅ 교정된 문장:")
                st.markdown(f"> {corrected_text}")

                if errors:
                    st.markdown("### ❌ 발견된 오류:")
                    for i, (err, sug) in enumerate(errors, 1):
                        st.markdown(f"**{i}.** `{err}` → **{sug}**")
                else:
                    st.info("맞춤법 오류가 없습니다!")

            except Exception as e:
                st.error(f"오류 발생: {e}")
    else:
        st.warning("문장을 입력해주세요.")
