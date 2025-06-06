import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("얼굴 자동 블러 처리기")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 얼굴 탐지용 Haar cascade 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def blur_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = image[y:y+h, x:x+w]
        roi_blur = cv2.GaussianBlur(roi, (99, 99), 30)
        image[y:y+h, x:x+w] = roi_blur

    return image

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image.convert("RGB"))
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    result = blur_faces(image_bgr)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    st.image(result_rgb, caption="블러 처리된 이미지", use_column_width=True)
