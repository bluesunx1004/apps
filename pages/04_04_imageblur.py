import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# DNN 모델 파일 경로
modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

st.title("얼굴 블러 처리 앱 (OpenCV DNN)")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

blur_strength = st.slider("블러 강도", min_value=15, max_value=101, step=2, value=51)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # 얼굴 검출 (OpenCV DNN)
    blob = cv2.dnn.blobFromImage(image_cv, 1.0, (900, 900), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([image_cv.shape[1], image_cv.shape[0], image_cv.shape[1], image_cv.shape[0]])
            (x1, y1, x2, y2) = box.astype("int")
            w = x2 - x1
            h = y2 - y1
            faces.append((x1, y1, w, h))

    st.write(f"감지된 얼굴 수: {len(faces)}")

    for (x, y, w, h) in faces:
        # 패딩 추가
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_cv.shape[1])
        y2 = min(y + h + pad, image_cv.shape[0])
        face_region = image_cv[y1:y2, x1:x2]

        # 영역이 비어 있으면 skip
        if face_region.size == 0:
            continue

        # 커널 크기 보정
        k = blur_strength
        if face_region.shape[0] < k or face_region.shape[1] < k:
            k = min(face_region.shape[0], face_region.shape[1])
            k = k if k % 2 == 1 else k - 1
            if k <= 0:
                continue

        # 블러 처리
        blurred = cv2.GaussianBlur(face_region, (k, k), 30)
        image_cv[y1:y2, x1:x2] = blurred

    # 결과 이미지 출력
    result_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    st.image(result_image, caption="블러 처리된 이미지", use_column_width=True)

    # 다운로드 버튼
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
