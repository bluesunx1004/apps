import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("🧠 얼굴 자동 블러 처리기 (간단 버전)")

# 모델 로드
net = cv2.dnn.readNetFromCaffe(
    "deploy.prototxt",
    "res10_300x300_ssd_iter_140000.caffemodel"
)

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 얼굴 탐지
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104, 177, 123))
    net.setInput(blob)
    detections = net.forward()

    # 얼굴 블러 처리
    count = 0
    for i in range(detections.shape[2]):
        if detections[0, 0, i, 2] > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            face = image[y1:y2, x1:x2]
            if face.size > 0:
                image[y1:y2, x1:x2] = cv2.GaussianBlur(face, (99, 99), 30)
                count += 1

    # 결과 출력
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption=f"✅ 얼굴 {count}개 블러 처리됨", use_column_width=True)

    # 다운로드
    result = Image.fromarray(image_rgb)
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    st.download_button("📥 이미지 다운로드", buf.getvalue(), "blurred_faces.png", "image/png")
