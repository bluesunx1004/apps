import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🕵️‍♂️ 얼굴 블러 처리기 (자동 감지)")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 로드
    image = Image.open(uploaded_file).convert('RGB')
    img_array = np.array(image)

    # OpenCV용 이미지로 변환
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # 얼굴 인식 모델 로드 (Haar Cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # 얼굴 감지
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    st.write(f"감지된 얼굴 수: {len(faces)}")

    # 얼굴 블러 처리
    for (x, y, w, h) in faces:
        face_region = img_cv[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        img_cv[y:y+h, x:x+w] = blurred_face

    # 결과 이미지 RGB로 다시 변환
    result_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # 표시
    st.image(result_img, caption="블러 처리된 이미지", use_column_width=True)

    # 다운로드
    result_pil = Image.fromarray(result_img)
    st.download_button(
        label="📥 이미지 다운로드",
        data=cv2.imencode('.png', cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))[1].tobytes(),
        file_name="blurred_faces.png",
        mime="image/png"
    )
