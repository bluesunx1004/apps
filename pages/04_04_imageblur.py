
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Haar Cascade 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.title("얼굴 블러 처리 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)

    # OpenCV는 BGR 포맷 사용
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    faces = face_cascade.detectMultiScale(image_cv, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_region = image_cv[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(face_region, (99, 99), 30)
        image_cv[y:y+h, x:x+w] = blurred

    # 다시 RGB로 변환하여 출력
    result_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    st.image(result_image, caption="블러 처리된 이미지", use_column_width=True)
