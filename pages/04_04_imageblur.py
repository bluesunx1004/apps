import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Haar Cascade 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.title("얼굴 블러 처리 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
blur_strength = st.slider("블러 강도", min_value=15, max_value=101, step=2, value=51)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # 성능 향상을 위해 임시로 이미지 축소
    resize_scale = 600 / max(image_cv.shape[:2])
    small_img = cv2.resize(image_cv, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_LINEAR)

    # 얼굴 감지 (더 민감하게 조정)
    faces = face_cascade.detectMultiScale(
        small_img, 
        scaleFactor=1.05,  # 더 정밀하게
        minNeighbors=3,    # 너무 적게 설정하면 오탐 가능
        minSize=(30, 30)   # 최소 얼굴 크기 설정
    )

    # 인식된 얼굴 좌표 원래 이미지 크기로 복원
    faces = [(int(x/resize_scale), int(y/resize_scale), int(w/resize_scale), int(h/resize_scale)) for (x, y, w, h) in faces]

    for (x, y, w, h) in faces:
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_cv.shape[1])
        y2 = min(y + h + pad, image_cv.shape[0])

        face_region = image_cv[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 30)
        image_cv[y1:y2, x1:x2] = blurred

    result_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    st.image(result_image, caption="블러 처리된 이미지", use_column_width=True)

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
