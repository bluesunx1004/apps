import streamlit as st
from hanspell import spell_checker
from pykospacing import Spacing

# Streamlit 앱 타이틀
st.title("한글 맞춤법 & 띄어쓰기 교정 앱")

# 입력 텍스트 박스
text = st.text_area("교정할 문장을 입력하세요:", height=200)

# 교정 버튼
if st.button("교정하기"):
    if text.strip():
        # hanspell: 맞춤법 & 띄어쓰기 교정
        try:
            spelled = spell_checker.check(text)
            hanspell_result = spelled.checked
            st.write("**hanspell 교정 결과:**")
            st.write(hanspell_result)
        except Exception as e:
            st.error(f"hanspell 맞춤법 검사 중 오류 발생: {e}")
            hanspell_result = text

        # pykospacing: 띄어쓰기 교정
        try:
            spacing = Spacing()
            kospacing_result = spacing(text)
            st.write("**pykospacing 띄어쓰기 교정 결과:**")
            st.write(kospacing_result)
        except Exception as e:
            st.error(f"pykospacing 띄어쓰기 교정 중 오류 발생: {e}")
            kospacing_result = text

        # 두 결과 비교
        st.write("---")
        st.write("**결과 비교**")
        st.write("- hanspell: 맞춤법 & 띄어쓰기 교정")
        st.write("- pykospacing: 띄어쓰기 교정")

    else:
        st.warning("문장을 입력해주세요!")
