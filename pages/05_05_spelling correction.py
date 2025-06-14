import streamlit as st
from kiwipiepy import Kiwi

st.title("한글 띄어쓰기 교정 앱 (kiwipiepy)")

kiwi = Kiwi()

text = st.text_area("교정할 문장을 입력하세요:", height=200)
if st.button("교정하기"):
    if text.strip():
        # 띄어쓰기 교정 (맞춤법은 지원하지 않음)
        result = kiwi.tokenize(text)
        corrected = ' '.join(t.form for t in result)
        st.write("**띄어쓰기 교정 결과:**")
        st.write(corrected)
    else:
        st.warning("문장을 입력해주세요!")
