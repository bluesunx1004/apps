import streamlit as st

# 앱 타이틀과 설명
st.set_page_config(page_title="유용한 기능 모음 앱", page_icon="🧰", layout="centered")

st.title("🧰 유용한 기능 모음 앱")
st.markdown("#### 다양한 실생활 및 업무에 도움이 되는 도구들을 한 곳에 모았습니다.")
st.markdown("""
이 앱은 아래와 같은 기능들을 제공합니다:
- 📝 **문서 요약기**: 긴 문서를 간단하게 요약
- 🔐 **비밀번호 생성기**: 보안 강도 높은 랜덤 비밀번호 생성

아래 사이드바에서 원하는 기능을 선택해 주세요 👇
""")

st.image("https://cdn-icons-png.flaticon.com/512/535/535234.png", width=150)

st.markdown("---")
st.markdown("ℹ️ **Tip**: 이 앱은 지속적으로 새로운 기능이 추가될 예정입니다. 즐겨찾기에 추가해 주세요!")

