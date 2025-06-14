import streamlit as st
import face_recognition
import numpy as np
import cv2
from PIL import Image
import io

st.title("얼굴 블러 처리 앱 (딥러닝 기반)")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

blur_strength = st.slider("블러 강도 (커널 크기)", min_value=15, max_value=101, step=2, value=51)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    # 얼굴 위치 찾기 (top, right, bottom, left)
    face_locations = face_recognition.face_locations(image_np)

    st.write(f"감지된 얼굴 수: {len(face_locations)}")

    for face in face_locations:
        top, right, bottom, left = face

        # 패딩 추가
        pad_x = int(0.2 * (right - left))
        pad_y = int(0.2 * (bottom - top))

        x1 = max(left - pad_x, 0)
        y1 = max(top - pad_y, 0)
        x2 = min(right + pad_x, image_np.shape[1])
        y2 = min(bottom + pad_y, image_np.shape[0])

        face_region = image_np[y1:y2, x1:x2]

        # 블러 커널 크기 유효성 체크
        k = blur_strength
        if face_region.shape[0] < k or face_region.shape[1] < k:
            k = min(face_region.shape[0] | 1, face_region.shape[1] | 1)  # 가장 가까운 홀수

        blurred = cv2.GaussianBlur(face_region, (k, k), 30)
        image_np[y1:y2, x1:x2] = blurred

    st.image(image_np, caption="블러 처리된 이미지", use_column_width=True)

    # 이미지 저장
    result_pil = Image.fromarray(image_np)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="블러 처리된 이미지 다운로드",
        data=byte_im,
        file_name="blurred_image.png",
        mime="image/png"
    )
