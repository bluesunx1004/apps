import streamlit as st
import requests
from bs4 import BeautifulSoup

def check_spelling(text):
    url = "https://speller.cs.pusan.ac.kr/results"
    data = {
        "text1": text
    }

    response = requests.post(url, data=data)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for err in soup.select(".tdReplace"):
        original = err.find_previous_sibling("td").text.strip()
        corrected = err.text.strip()
        info = err.find_next_sibling("td").text.strip()
        results.append({
            "original": original,
            "corrected": corrected,
            "info": info
        })

    return results

# Streamlit UI
st.title("📝 한글 맞춤법 검사기 (부산대 기반)")
st.write("아래에 문장을 입력하면 맞춤법을 검사하고 교정된 표현을 제안해줍니다.")

text = st.text_area("검사할 문장을 입력하세요:", height=200)

if st.button("✅ 맞춤법 검사"):
    if not text.strip():
        st.warning("문장을 입력해주세요.")
    else:
        with st.spinner("검사 중입니다..."):
            result = check_spelling(text)
        if not result:
            st.success("맞춤법 오류를 찾지 못했습니다! 🎉")
        else:
            st.warning(f"총 {len(result)}개의 교정 제안이 있습니다.")
            for i, item in enumerate(result, 1):
                st.markdown(f"""
                **{i}. 원문**: `{item['original']}`  
                **→ 수정안**: `{item['corrected']}`  
                🛈 _{item['info']}_  
                ---
                """)
