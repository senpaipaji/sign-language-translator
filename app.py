import streamlit as st
import cv2
import numpy as np
from utils import HolisticDetector

def classify_real_time():
    st.write("Real-time hand sign classification")

    button_placeholder1 = st.empty()
    button_placeholder2 = st.empty()

    toggle_button_start = button_placeholder1.button('Start', key=1)

    toggle_value = False

    col1, col2 = st.columns(2)

    video_frame1 = col1.empty()
    video_frame2 = col2.empty()

    if toggle_button_start:
        button_placeholder1.empty()
        toggle_button_stop = button_placeholder2.button('Stop', key=2)
        toggle_value = True

    if toggle_value:
        cap = cv2.VideoCapture(0)
        detector = HolisticDetector()
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                if not ret:
                    break

                # Decimate frames to process only a fraction of them
                if np.random.rand() > 0.5:
                    continue

                # Resize frame for faster processing
                frame = cv2.resize(frame, (640, 480))

                image, results2 = detector.apply_holistic(frame)

                cv2.putText(frame, "capture input :", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 1,
                            cv2.LINE_AA)
                cv2.putText(image, "holistic output :", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 1,
                            cv2.LINE_AA)

                # Update images asynchronously
                video_frame1.image(frame, channels="BGR", use_column_width=True)
                video_frame2.image(image, channels="BGR", use_column_width=True)

                if cv2.waitKey(10) & toggle_button_stop:
                    break
        finally:
            toggle_value = False
            button_placeholder2.empty()
            cap.release()


    


def record_and_train():
    
    st.write("Video recording for training")


def main():
    st.title("Hand Sign Translation App")

    # Sidebar with navigation options
    page = st.sidebar.radio("Select Function", ["Real-time Classification", "Record and Train"])

    # Main content based on selected page
    if page == "Real-time Classification":
        classify_real_time()
    elif page == "Record and Train":
        record_and_train()

# Run the app
if __name__ == "__main__":
    main()
