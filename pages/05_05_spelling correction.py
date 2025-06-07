import streamlit as st
from hanspell import spell_checker
from pykospacing import Spacing

spacing = Spacing()

st.title("📝 한국어 맞춤법 + 띄어쓰기 보정기")

text = st.text_area("문장을 입력하세요:", height=200)

if st.button("검사하기"):
    if not text.strip():
        st.warning("문장을 입력해주세요.")
    else:
        try:
            # 1단계: 띄어쓰기 보정
            spaced = spacing(text)

            # 2단계: 맞춤법 교정
            result = spell_checker.check(spaced)

            if result:
                corrected = result.checked
                st.subheader("✅ 교정 결과:")
                st.write(corrected)
            else:
                st.error("맞춤법 교정 실패: 결과 없음")

        except Exception as e:
            st.error(f"오류 발생: {e}")
