import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import mediapipe as mp

st.title("얼굴 블러 처리 앱 (MediaPipe 기반)")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

blur_strength = st.slider("블러 강도 (커널 크기)", min_value=15, max_value=101, step=2, value=51)

# MediaPipe 얼굴 감지 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_copy = image_np.copy()

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(image_np)

        if results.detections:
            st.write(f"감지된 얼굴 수: {len(results.detections)}")
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image_np.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # 패딩 추가
                pad = int(0.2 * w)
                x1 = max(x - pad, 0)
                y1 = max(y - pad, 0)
                x2 = min(x + w + pad, iw)
                y2 = min(y + h + pad, ih)

                face_region = image_copy[y1:y2, x1:x2]

                # 블러 커널 크기 보정
                k = blur_strength
                if face_region.shape[0] < k or face_region.shape[1] < k:
                    k = min(face_region.shape[0] | 1, face_region.shape[1] | 1)

                blurred = cv2.GaussianBlur(face_region, (k, k), 30)
                image_copy[y1:y2, x1:x2] = blurred

        else:
            st.warning("얼굴을 감지하지 못했습니다.")

    st.image(image_copy, caption="블러 처리된 이미지", use_column_width=True)

    # 이미지 저장
    result_pil = Image.fromarray(image_copy)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="블러 처리된 이미지 다운로드",
        data=byte_im,
        file_name="blurred_image.png",
        mime="image/png"
    )
