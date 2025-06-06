import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("🧠 얼굴 자동 블러 처리기")

# DNN 모델 불러오기
try:
    net = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt",
        "res10_300x300_ssd_iter_140000.caffemodel"
    )
except:
    st.error("❗ 모델 파일이 없습니다. 같은 폴더에 넣어주세요.")
    st.stop()

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        st.error("❗ 이미지를 불러오지 못했습니다.")
        st.stop()

    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104, 177, 123))
    net.setInput(blob)
    detections = net.forward()

    count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)

            # 이미지 범위 내로 좌표 보정
            x1, y1 = np.clip([x1, y1], 0, [w - 1, h - 1])
            x2, y2 = np.clip([x2, y2], 0, [w - 1, h - 1])

            face = image[y1:y2, x1:x2]
            if face.size > 0:
                blurred = cv2.GaussianBlur(face, (99, 99), 30)
                image[y1:y2, x1:x2] = blurred
                count += 1

    # 결과 표시
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption=f"✅ {count}개의 얼굴 블러 처리", use_container_width=True)

    if count > 0:
        result = Image.fromarray(image_rgb)
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button("📥 결과 이미지 다운로드", buf.getvalue(), "blurred_faces.png", "image/png")
    else:
        st.warning("😢 얼굴을 찾을 수 없습니다.")
