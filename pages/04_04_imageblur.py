import streamlit as st
import cv2
import numpy as np
import face_recognition
from PIL import Image

st.set_page_config(page_title="얼굴 블러 처리기", layout="centered")
st.title("📸 얼굴 블러 처리기")
st.write("업로드된 이미지에서 얼굴을 감지하고 자동으로 블러 처리합니다.")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

def blur_faces(image):
    # 이미지 로드 및 RGB 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(image_rgb)

    for top, right, bottom, left in face_locations:
        # 얼굴 영역 잘라내기
        face_region = image[top:bottom, left:right]
        # 얼굴 블러 처리
        face_region = cv2.GaussianBlur(face_region, (99, 99), 30)
        # 원본 이미지에 블러 처리된 얼굴 붙이기
        image[top:bottom, left:right] = face_region

    return image

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image.convert("RGB"))
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    result_image = blur_faces(image_bgr)
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

    st.image(result_image_rgb, caption="블러 처리된 이미지", use_column_width=True)
