import streamlit as st
from pnu_korean_spell_checker import KoreanSpellChecker

st.set_page_config(page_title="한글 맞춤법 검사기", page_icon="📝")

st.title("📝 한글 맞춤법 검사기")
st.caption("🚀 빠르고 안정적인 맞춤법 검사 (부산대 API 기반)")

# 사용자 입력
user_input = st.text_area("검사할 문장을 입력하세요:", height=200)

# 검사 버튼
if st.button("맞춤법 검사"):
    if user_input.strip():
        with st.spinner("검사 중입니다..."):
            try:
                results = KoreanSpellChecker.check(user_input)
                corrected = results["result_text"]

                st.success("✅ 맞춤법 검사 완료!")

                # 수정된 문장 표시
                st.markdown("### ✏️ 수정된 문장")
                st.markdown(f"> {corrected}")

                # 오류 리스트
                if results["errors"]:
                    st.markdown("### 🔍 발견된 오류")
                    for idx, err in enumerate(results["errors"], 1):
                        st.markdown(
                            f"**{idx}.** `{err['error']}` → **{err['suggestion']}** (위치: {err['start']}~{err['end']})"
                        )
                else:
                    st.info("맞춤법 오류가 발견되지 않았습니다.")

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {e}")
    else:
        st.warning("문장을 입력해주세요.")
