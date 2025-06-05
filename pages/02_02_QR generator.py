import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.title("🔳 QR 코드 생성기")
st.markdown("URL이나 텍스트를 입력하면 실시간으로 QR 코드를 생성하고 크기도 조절할 수 있어요!")

# 사용자 입력
user_input = st.text_input("QR 코드에 담을 URL 또는 텍스트를 입력하세요:")

# 사이즈 입력
qr_size = st.slider("QR 코드 크기 (픽셀)", min_value=100, max_value=1000, value=300, step=50)

if user_input:
    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        box_size=10,  # 기본 크기 (후에 resize로 다시 조정)
        border=4
    )
    qr.add_data(user_input)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 원하는 크기로 리사이징
    img = img.resize((qr_size, qr_size), Image.LANCZOS)

    # 이미지 버퍼로 저장
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # 이미지 표시
    st.image(buffer, caption=f"🔍 {qr_size}px 크기의 QR 코드", use_container_width=False)

    # 다운로드 버튼
    st.download_button(
        label="📥 QR 코드 이미지 다운로드",
        data=buffer,
        file_name="qr_code.png",
        mime="image/png"
    )
else:
    st.info("왼쪽 입력창에 URL이나 텍스트를 입력해 주세요 😊")
