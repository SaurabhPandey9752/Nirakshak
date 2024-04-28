import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from datetime import timedelta
import pytesseract

# Ensure the path to Tesseract is correctly set
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change to your Tesseract path

# Function to detect number plates
def detect_number_plates(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    edged = cv2.Canny(gray, 50, 200)  # Edge detection
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 50 < w < 200 and 20 < h < 100:  # Example thresholds for number plates
            roi = gray[y:y+h, x:x+w]  # Region of interest
            text = pytesseract.image_to_string(roi, config='--psm 8')  # OCR
            if text.strip():
                return text.strip(), frame
    return "No plate detected", frame


# Streamlit Interface
st.title("Number Plate Detection")

# Section for video upload
st.header("Upload a Video")
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
if uploaded_file:
    # Create a temporary file to store the video
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    video = cv2.VideoCapture(temp_file.name)
    frame_rate = video.get(cv2.CAP_PROP_FPS) if video.isOpened() else None

    if frame_rate is None:
        st.error("Error opening video file.")
    else:
        detected_plates = []
        frame_number = 0

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            # Process every Nth frame to save resources (example: every 10th frame)
            if frame_number % 10 == 0:
                plate, detected_frame = detect_number_plates(frame)
                time_stamp = str(timedelta(seconds=frame_number / frame_rate))

                detected_plates.append((plate, detected_frame, time_stamp))

            frame_number += 1

        video.release()  # Release video capture

        # Display detected plates and images
        if detected_plates:
            st.write("Detected Number Plates with Timestamps:")
            for plate, detected_frame, time_stamp in detected_plates:
                st.write(f"Number Plate: {plate}, Time: {time_stamp}")
                detected_frame_image = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
                st.image(detected_frame_image, caption=f"Frame at {time_stamp}")
        else:
            st.write("No number plates detected.")

    # Clean up temporary file
    try:
        os.remove(temp_file.name)
    except Exception as e:
        st.warning(f"Could not delete temp file: {e}")

# Section for photo upload
st.header("Upload a Photo")
uploaded_photo = st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])
if uploaded_photo:
    photo = Image.open(uploaded_photo)
    st.image(photo, caption="Uploaded Photo")

    # Detect number plate in the photo
    plate, detected_frame = detect_number_plates(np.array(photo))
    st.write(f"Detected Number Plate: {plate}")

# Section for live camera
st.header("Live Camera Access")
camera_input = st.camera_input("Capture a photo using your camera")
if camera_input:
    captured_image = Image.open(camera_input)
    st.image(captured_image, caption="Captured Photo")

    # Detect number plate in live camera photo
    plate, detected_frame = detect_number_plates(np.array(captured_image))
    st.write(f"Detected Number Plate: {plate}")
