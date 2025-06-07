import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Haar Cascade 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.title("얼굴 블러 처리 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 블러 강도 슬라이더 (커널 크기)
blur_strength = st.slider("블러 강도", min_value=15, max_value=101, step=2, value=51)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # 얼굴 감지
    faces = face_cascade.detectMultiScale(image_cv, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # 패딩 추가 (얼굴 주변 20%씩 확대)
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_cv.shape[1])
        y2 = min(y + h + pad, image_cv.shape[0])

        face_region = image_cv[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 30)
        image_cv[y1:y2, x1:x2] = blurred

    # RGB 변환 및 출력
    result_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    st.image(result_image, caption="블러 처리된 이미지", use_column_width=True)

    # 다운로드 버튼용: 이미지 바이너리 저장
    result_pil = Image.fromarray(result_image)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="블러 처리된 이미지 다운로드",
        data=byte_im,
        file_name="blurred_image.png",
        mime="image/png"
    )
