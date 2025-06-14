import streamlit as st
from hanspell import spell_checker

st.title("한글 띄어쓰기 & 맞춤법 교정 앱")

text = st.text_area("교정할 문장을 입력하세요:", height=200)
if st.button("교정하기"):
    if text.strip():
        try:
            result = spell_checker.check(text)
            st.write("**교정 결과:**")
            st.write(result.checked)
            st.write("**수정된 부분:**")
            st.write(result.errors)
        except Exception as e:
            st.error(f"맞춤법 검사 중 오류가 발생했습니다: {e}")
    else:
        st.warning("문장을 입력해주세요!")
