import streamlit as st
from hanspell import spell_checker

st.title("📝 한글 맞춤법 검사기")

user_input = st.text_area("검사할 문장을 입력하세요:", height=150)

if st.button("맞춤법 검사"):
    if user_input.strip():
        try:
            result = spell_checker.check(user_input)
            if result:  # 결과가 제대로 왔는지 확인
                st.markdown("✅ **검사 결과:**")
                st.write(result.checked)
                st.markdown("🔍 **오류 통계:**")
                st.json({
                    "맞춤법 오류": result.errors,
                    "원문": result.original,
                    "수정된 문장": result.checked
                })
            else:
                st.error("맞춤법 검사 결과를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("문장을 입력해주세요.")
