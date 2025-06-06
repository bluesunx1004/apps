import streamlit as st
from hanspell import spell_checker

st.title("🇰🇷 한글 맞춤법 검사기 ✏️")
st.write("텍스트를 입력하면 맞춤법과 문법 오류를 자동으로 교정해드려요!")

text = st.text_area("검사할 텍스트를 입력하세요:", height=200)

if st.button("✅ 맞춤법 검사"):
    if text.strip():
        with st.spinner("검사 중입니다... 🔍"):
            result = spell_checker.check(text)
            corrected = result.checked
        st.success("✔️ 맞춤법 검사 완료!")
        st.subheader("📝 교정된 문장:")
        st.text_area("결과", corrected, height=200)
        
        st.download_button(
            label="📥 결과 텍스트 다운로드",
            data=corrected,
            file_name="corrected_text.txt",
            mime="text/plain"
        )
    else:
        st.warning("검사할 텍스트를 입력해주세요.")
