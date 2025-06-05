import streamlit as st

# 페이지 설정
st.set_page_config(page_title="유용한 기능 모음 앱", page_icon="🧰", layout="centered")

# 앱 제목 및 설명
st.title("🧰 유용한 기능 모음 앱")
st.markdown("#### 실생활과 업무에 유용한 다양한 도구들을 하나의 앱으로!")

st.markdown("""
이 앱은 다음과 같은 기능을 제공합니다:

- 📄 **PDF ➜ PPT 변환기**: 업로드한 PDF 파일을 자동으로 PowerPoint 슬라이드로 변환
- 🔳 **QR 코드 생성기**: 텍스트나 URL을 입력하면 QR 코드를 즉시 생성
- 🌍 **영문 문서 ➜ 한글 자동 번역기**: 영어 텍스트나 문서를 빠르게 한국어로 번역
- 📝 **맞춤법 검사기**: 한글 문장의 철자 및 문법 오류를 자동으로 교정
- 👤 **얼굴 모자이크 처리기**: 이미지에서 얼굴을 자동 감지하고 블러 처리

사이드바에서 원하는 기능을 선택해 주세요 👇
""")

# 이미지 (아이콘 등)
st.image("https://cdn-icons-png.flaticon.com/512/535/535234.png", width=120)

st.markdown("---")
st.info("🔧 새로운 기능이 계속 추가될 예정입니다. 즐겨찾기 해두시면 편리하게 이용하실 수 있어요!")

