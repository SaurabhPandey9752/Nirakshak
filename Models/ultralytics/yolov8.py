import streamlit as st
import cv2
import os
import datetime
import tempfile
import numpy as np
from PIL import Image
from ultralytics import YOLO

# Set environment variable to avoid conflicts
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Load the YOLOv8 model
model = YOLO('yolov8m.pt')

# Streamlit interface
st.title("YOLO Object Detection")

# Section for video upload and processing
st.header("Upload a Video File for Object Detection")
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_video.read())
        video_path = temp_file.name

    lower_resolution = (540, 380)
    start_time = datetime.datetime.now()

    # Detect objects in the video and display results
    results = model.track(source=video_path, show=False, tracker="bytetrack.yaml", batch=8, imgsz=lower_resolution)

    end_time = datetime.datetime.now()
    processing_time = end_time - start_time

    st.write(f"Processing Time: {processing_time}")

    # Display the results
    st.write("Detected Objects:")
    for result in results:
        st.image(result.orig_img, caption=f"Detected at {processing_time}")

    # Clean up the temporary file
    try:
        os.remove(video_path)
    except Exception as e:
        st.warning(f"Could not delete temp file: {e}")

# Section for photo upload
st.header("Upload a Photo for Object Detection")
uploaded_photo = st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])
if uploaded_photo:
    photo = Image.open(uploaded_photo)
    img_np = np.array(photo)

    start_time = datetime.datetime.now()

    results = model.track(source=img_np, show=False, tracker="bytetrack.yaml", batch=8, imgsz=lower_resolution)

    end_time = datetime.datetime.now()
    processing_time = end_time - start_time

    st.write(f"Processing Time: {processing_time}")

    st.image(results[0].orig_img, caption="Detected Objects")

# Section for live camera input
st.header("Live Camera for Object Detection")
camera_input = st.camera_input("Capture a photo using your camera")
if camera_input:
    captured_image = Image.open(camera_input)
    img_np = np.array(captured_image)

    start_time = datetime.datetime.now()

    results = model.track(source=img_np, show=False, tracker="bytetrack.yaml", batch=8, imgsz=lower_resolution)

    end_time = datetime.datetime.now()
    processing_time = end_time - start time

    st.write(f"Processing Time: {processing_time}")

    st.image(results[0].orig_img, caption="Detected Objects")

# Done with Streamlit
