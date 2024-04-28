

# Nirakshak Geotagging and Surveillance Platform

Welcome to the Nirakshak Geotagging and Surveillance Platform! This comprehensive solution provides law enforcement agencies with a powerful tool for monitoring public and private cameras, issuing alerts for specific events, and ensuring camera safety. This README outlines the key features, technical requirements, and future scope of the platform.

## Live Demo
Experience a live demo of the Nirakshak platform at [https://nirakshak.vercel.app/](https://nirakshak.vercel.app/). Explore the features and see how the platform works in real-time.

## Features

### Geotagging and User Registration
- **User Registration**: Users must provide personal details, including Name, Phone No., and Email ID.
- **Camera Information**: Users can enter the IP address and camera model to provide camera access.
- **Camera Consent**: Users must consent to provide camera access before the platform can include the camera in its system.
- **Map View**: The platform provides law enforcement with a comprehensive map view, distinguishing between private and public cameras.
- **Camera Details**: Clicking on a camera point reveals detailed information about the camera and its owner from the database, along with the nearest police chowki.

### Alerts and Detections
- **Object Detection with Yolov8**: The platform uses Yolov8 to analyze large video streams, capable of detecting over 80 distinct objects.
- **Violence and Weapons Detection**: A custom-trained model detects Violence/Fight, Guns, and Knives, triggering an alert (beep sound) upon detection.
- **License Plate Detection with OpenCV and Easy-OCR**: The platform uses OpenCV for license plate detection and reads text using Easy-OCR.

### Camera Safety
- **Initial Picture Capture**: An algorithm captures an initial picture from the CCTV, stored in the database.
- **Live Footage Comparison**: The initial picture is periodically compared with live footage to generate a similarity score.
- **Alerts for Displacement/Obstruction**: If the similarity score falls below a set threshold, an alert is triggered to notify of potential issues with the camera, aiding in identifying displacements or obstructions.

## Future Scope
- **Path Tracking for License Plates**: An algorithm will be introduced to track specific license plates, plotting their paths. This feature will enhance law enforcement capabilities by providing insights into potential routes a vehicle may take.
- **Face Detection on CCTV Footage**: Implement a Face Detection algorithm to alert law enforcement when a wanted/criminal individual is spotted in CCTV footage.

## Technical Requirements

### Backend
- **Flask**: For building and running the backend of the platform.
- **SQL/MySQL**: For database management and data storage.

### Machine Learning and Computer Vision
- **Streamlit**: For building user interfaces and interactive web applications.
- **Ultralytics**: For running Yolov8-based object detection models.
- **OpenCV**: For computer vision tasks and license plate detection.
- **Tesseract**: For OCR (Optical Character Recognition).

## Installation and Setup
Follow these steps to set up and run the platform:

### Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
## Dependecies
pip install flask sql easy-ocr streamlit ultralytics opencv-python tesseract
flask run
streamlit run <streamlit-app-file>
## Contributing
Contributions are welcome! If you'd like to contribute to the Nirakshak platform, please submit a pull request or open an issue on the repository.
## License

This README file provides a comprehensive overview of your platform, including its features, technical requirements, installation steps, and future scope. It also includes guidance on how to contribute and mentions the licensing information. Adjust the placeholders (`<repository-url>`, `<streamlit-app-file>`, etc.) as needed to fit your project specifics.

