import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io

# 얼굴 검출 모델
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

st.set_page_config(page_title="얼굴 블러 앱", layout="wide")
st.title("🧠 얼굴 자동 검출 + 🎨 사용자 지정 블러 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
blur_strength = st.slider("블러 강도 (홀수)", min_value=15, max_value=99, step=2, value=31)

if uploaded_file:
    # 원본 PIL 이미지 생성
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np.copy(), cv2.COLOR_RGB2BGR)

    # 얼굴 검출 및 블러 처리
    faces = face_cascade.detectMultiScale(image_bgr, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_bgr.shape[1])
        y2 = min(y + h + pad, image_bgr.shape[0])
        roi = image_bgr[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 30)
        image_bgr[y1:y2, x1:x2] = blurred

    # 얼굴 블러 후 RGB 이미지로 변환
    blurred_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # PIL 이미지로 변환 → 저장 → 다시 읽기 (이게 핵심)
    buf = io.BytesIO()
    Image.fromarray(blurred_rgb).save(buf, format="PNG")
    buf.seek(0)
    pil_for_canvas = Image.open(buf)

    # 사용자 선택 블러용 캔버스
    st.subheader("🖍️ 추가로 블러할 영역을 직접 지정하세요")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        background_image=pil_for_canvas,
        update_streamlit=True,
        height=pil_for_canvas.height,
        width=pil_for_canvas.width,
        drawing_mode="rect",
        key="canvas",
    )

    # 사용자가 그린 사각형 블러 처리
    if canvas_result.json_data and "objects" in canvas_result.json_data:
        for obj in canvas_result.json_data["objects"]:
            if obj["type"] == "rect":
                x, y = int(obj["left"]), int(obj["top"])
                w, h = int(obj["width"]), int(obj["height"])
                x1, y1 = max(x, 0), max(y, 0)
                x2, y2 = min(x + w, image_bgr.shape[1]), min(y + h, image_bgr.shape[0])
                roi = image_bgr[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 30)
                image_bgr[y1:y2, x1:x2] = blurred

    # 최종 출력
    final_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    final_pil = Image.fromarray(final_rgb)

    st.subheader("✅ 최종 결과")
    st.image(final_pil, use_column_width=True)

    # 다운로드
    out_buf = io.BytesIO()
    final_pil.save(out_buf, format="PNG")
    st.download_button(
        "📥 이미지 다운로드",
        data=out_buf.getvalue(),
        file_name="blurred_result.png",
        mime="image/png"
    )
