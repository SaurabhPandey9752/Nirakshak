import streamlit as st
import cv2
import numpy as np
from roboflow import Roboflow
from datetime import datetime
from playsound import playsound
import tempfile
import os

# Initialize Roboflow
rf = Roboflow(api_key="gfENJ7NUVSKxc9RmM4Uw")
project = rf.workspace().project("violence-weapon-detection")
model = project.version(1).model

# Alert function to play sound
def alert_sound():
    playsound(r'D:\Desktop\violese\alert.mp3')

# Function to predict on a frame and return results
def predict_on_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB for Roboflow
    result = model.predict(frame_rgb, confidence=40, overlap=50).json()  # Predict

    predictions = result.get("predictions", [])

    for prediction in predictions:
        confidence = prediction.get("confidence", None)
        predicted_class = prediction.get("class", None)

        if predicted_class != "NonViolence":
            alert_sound()  # Trigger sound alert if violence/weapon detected

        # Draw bounding box and add text
        x, y, width, height = (
            int(prediction.get("x")),
            int(prediction.get("y")),
            int(prediction.get("width")),
            int(prediction.get("height")),
        )
        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2,
        )
        cv2.putText(
            frame,
            f"{predicted_class}: {confidence:.2f}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    return frame  # Return frame with bounding boxes and text

# Streamlit interface
st.title("Violence and Weapon Detection")

# Section for video upload
st.header("Upload a Video")
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
if uploaded_file:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    cap = cv2.VideoCapture(temp_file.name)
    if not cap.isOpened():
        st.error("Error: Could not open video.")
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
        frame_interval = int(round(fps / 4))  # Example: process every 4th frame

        frame_count = 0
        frames_to_show = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_count % frame_interval == 0:
                # Predict and draw results
                detected_frame = predict_on_frame(frame)
                frames_to_show.append((frame_count, detected_frame))

            frame_count += 1

        # Release video capture
        cap.release()

        # Display frames with predictions
        if frames_to_show:
            st.write("Detected frames with predictions:")
            for frame_count, detected_frame in frames_to_show:
                detected_frame_rgb = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
                st.image(
                    detected_frame_rgb,
                    caption=f"Frame {frame_count}",
                )

        # Clean up temporary files
        try:
            os.remove(temp_file.name)
        except Exception as e:
            st.warning(f"Could not delete temp file: {e}")

    # Release OpenCV windows
    cv2.destroyAllWindows()
