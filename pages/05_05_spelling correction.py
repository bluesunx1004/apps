import streamlit as st
from hanspell import spell_checker

st.title("📝 한국어 맞춤법 검사기")

text = st.text_area("텍스트를 입력하세요:", height=200)

if st.button("검사하기"):
    if not text.strip():
        st.warning("검사할 텍스트를 입력하세요.")
    else:
        try:
            result = spell_checker.check(text)

            # result가 유효한지 체크
            if result is None:
                st.error("맞춤법 검사 결과를 불러오지 못했습니다. 다시 시도해 주세요.")
            else:
                checked_text = result.checked
                errors = result.errors

                st.subheader("✅ 수정된 결과:")
                st.write(checked_text)

                st.markdown("---")
                st.markdown(f"🔍 **수정된 단어 수:** {len(errors)}")

                if errors:
                    st.subheader("❗ 수정된 부분:")
                    for err in errors:
                        st.write(f"- `{err}` → `{errors[err]}`")

        except Exception as e:
            st.error(f"오류 발생: {e}")
