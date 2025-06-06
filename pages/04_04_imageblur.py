import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="얼굴 블러 처리기", layout="centered")
st.title("📸 얼굴 블러 처리기")
st.write("OpenCV를 사용하여 얼굴을 감지하고 블러 처리합니다.")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# OpenCV 내장 얼굴 감지 모델 불러오기
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def blur_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]
        face_roi = cv2.GaussianBlur(face_roi, (99, 99), 30)
        image[y:y+h, x:x+w] = face_roi

    return image

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image.convert("RGB"))
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    result_image = blur_faces(image_bgr)
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

    st.image(result_image_rgb, caption="블러 처리된 이미지", use_column_width=True)
