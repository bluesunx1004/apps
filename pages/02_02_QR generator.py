import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.title("🔳 QR 코드 생성기")
st.markdown("URL이나 텍스트를 입력하면 실시간으로 QR 코드를 생성할 수 있어요!")

# 사용자 입력
user_input = st.text_input("QR 코드에 담을 URL 또는 텍스트를 입력하세요:")

if user_input:
    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(user_input)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 이미지를 BytesIO로 저장
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Streamlit에 표시
    st.image(buffer, caption="🔍 생성된 QR 코드", use_container_width=True)

    # 다운로드 버튼
    st.download_button(
        label="📥 QR 코드 이미지 다운로드",
        data=buffer,
        file_name="qr_code.png",
        mime="image/png"
    )
else:
    st.info("왼쪽 입력창에 URL이나 텍스트를 입력해 주세요 😊")
