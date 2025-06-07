import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os

# 현재 파일 위치 기준 경로 계산
base_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(base_dir, "res10_300x300_ssd_iter_140000.caffemodel")
CONFIG_FILE = os.path.join(base_dir, "deploy.prototxt.txt")

net = cv2.dnn.readNetFromCaffe(CONFIG_FILE, MODEL_FILE)


st.title("DNN 기반 얼굴 블러 처리 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
blur_strength = st.slider("블러 강도", min_value=15, max_value=101, step=2, value=51)

CONFIDENCE_THRESHOLD = 0.5  # 얼굴로 인식할 최소 신뢰도

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    (h, w) = image_cv.shape[:2]

    # DNN 입력용 blob 생성
    blob = cv2.dnn.blobFromImage(image_cv, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONFIDENCE_THRESHOLD:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            # 패딩 추가
            pad_w = int(0.2 * (x2 - x1))
            pad_h = int(0.2 * (y2 - y1))
            x1p = max(x1 - pad_w, 0)
            y1p = max(y1 - pad_h, 0)
            x2p = min(x2 + pad_w, w)
            y2p = min(y2 + pad_h, h)

            # 블러 처리
            face_region = image_cv[y1p:y2p, x1p:x2p]
            if face_region.size == 0:
                continue  # 빈 영역 방지
            blurred = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 30)
            image_cv[y1p:y2p, x1p:x2p] = blurred

    result_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    st.image(result_image, caption="블러 처리된 이미지", use_column_width=True)

    # 다운로드
    result_pil = Image.fromarray(result_image)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="블러 처리된 이미지 다운로드",
        data=byte_im,
        file_name="blurred_image_dnn.png",
        mime="image/png"
    )
