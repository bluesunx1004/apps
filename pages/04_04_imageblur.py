import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io

# Streamlit 설정
st.set_page_config(page_title="얼굴 + 사용자 선택 블러 앱", layout="wide")
st.title("👤 얼굴 자동 검출 + 🖍️ 사용자 선택 블러 처리 앱")

# 얼굴 검출 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 파일 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 블러 강도 슬라이더
blur_strength = st.slider("블러 강도 (홀수만 허용)", min_value=15, max_value=99, step=2, value=51)

if uploaded_file:
    # 이미지 로드 및 변환
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np.copy(), cv2.COLOR_RGB2BGR)

    # 1. 얼굴 자동 검출 및 블러 처리
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    st.write(f"🔍 자동으로 감지된 얼굴 수: {len(faces)}")

    for (x, y, w, h) in faces:
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_bgr.shape[1])
        y2 = min(y + h + pad, image_bgr.shape[0])

        roi = image_bgr[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 30)
        image_bgr[y1:y2, x1:x2] = blurred

    # 얼굴 블러 처리된 RGB 이미지
    blurred_image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    # PIL 이미지로 변환 및 복사 → 반드시 새 이미지로 전달
    blurred_pil = Image.fromarray(blurred_image_rgb).copy()

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        background_image=blurred_pil,
        update_streamlit=True,
        height=blurred_pil.height,
        width=blurred_pil.width,
        drawing_mode="rect",
        key="canvas"
    )

    # 2. 사용자가 지정한 영역 추가 블러 처리
    if canvas_result.json_data and canvas_result.json_data["objects"]:
        for obj in canvas_result.json_data["objects"]:
            if obj["type"] == "rect":
                x = int(obj["left"])
                y = int(obj["top"])
                w = int(obj["width"])
                h = int(obj["height"])

                x1 = max(x, 0)
                y1 = max(y, 0)
                x2 = min(x + w, image_bgr.shape[1])
                y2 = min(y + h, image_bgr.shape[0])

                roi = image_bgr[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 30)
                image_bgr[y1:y2, x1:x2] = blurred

    # 최종 이미지 출력
    final_image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    final_pil = Image.fromarray(final_image_rgb)

    st.subheader("✅ 최종 결과")
    st.image(final_pil, use_column_width=True)

    # 다운로드 버튼
    buf = io.BytesIO()
    final_pil.save(buf, format="PNG")
    st.download_button(
        label="📥 블러 처리된 이미지 다운로드",
        data=buf.getvalue(),
        file_name="blurred_result.png",
        mime="image/png"
    )
