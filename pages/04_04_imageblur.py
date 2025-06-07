import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io

# 얼굴 검출기 로드 (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.set_page_config(page_title="얼굴 + 사용자 지정 블러", layout="wide")
st.title("얼굴 자동 검출 + 사용자 지정 영역 블러 처리 앱")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 블러 강도 조절 슬라이더
blur_strength = st.slider("블러 강도 (홀수만 허용)", min_value=15, max_value=101, step=2, value=51)

if uploaded_file is not None:
    # 원본 이미지 로드
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    img_copy = image_np.copy()

    # OpenCV용 BGR 이미지
    image_cv = cv2.cvtColor(img_copy, cv2.COLOR_RGB2BGR)

    # 얼굴 자동 검출
    faces = face_cascade.detectMultiScale(image_cv, scaleFactor=1.1, minNeighbors=5)
    st.write(f"자동 검출된 얼굴 수: {len(faces)}")

    for (x, y, w, h) in faces:
        # 약간의 여유 padding
        pad = int(0.2 * w)
        x1 = max(x - pad, 0)
        y1 = max(y - pad, 0)
        x2 = min(x + w + pad, image_cv.shape[1])
        y2 = min(y + h + pad, image_cv.shape[0])
        region = image_cv[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(region, (blur_strength, blur_strength), 30)
        image_cv[y1:y2, x1:x2] = blurred

    # 얼굴 블러 처리된 이미지 (BGR → RGB)
    auto_blurred_img = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

    # 사용자가 블러 처리할 영역 선택
    st.subheader("추가적으로 블러할 영역을 직접 그려주세요 (선택사항)")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        background_image=Image.fromarray(auto_blurred_img),
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas",
    )

    if canvas_result.json_data:
        for obj in canvas_result.json_data["objects"]:
            if obj["type"] == "rect":
                left = int(obj["left"])
                top = int(obj["top"])
                width = int(obj["width"])
                height = int(obj["height"])

                x1 = max(left, 0)
                y1 = max(top, 0)
                x2 = min(left + width, img_copy.shape[1])
                y2 = min(top + height, img_copy.shape[0])

                region = image_cv[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(region, (blur_strength, blur_strength), 30)
                image_cv[y1:y2, x1:x2] = blurred

    # 최종 결과 출력
    final_result = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    result_img = Image.fromarray(final_result)

    st.subheader("최종 블러 처리된 이미지")
    st.image(result_img, use_column_width=True)

    # 다운로드 버튼
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    st.download_button(
        label="이미지 다운로드",
        data=buf.getvalue(),
        file_name="final_blurred.png",
        mime="image/png"
    )
