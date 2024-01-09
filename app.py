import sys
import cv2
from utils import HolisticDetector,HolisticClassifier
from PyQt5 import uic  
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton
from PyQt5.QtGui import QPixmap,QImage

class MyForm(QWidget):  # Create a class for your form
    def __init__(self):
        super().__init__()
        self.detector = HolisticDetector()
        self.classifier = HolisticClassifier()
        uic.loadUi("form.ui", self)  # Load the UI file into this class
        
        #frames
        self.frame1 = self.findChild(QLabel, "image_frame1")
        self.frame2 = self.findChild(QLabel, "image_frame2")
        
        #buttons
        self.start_button = self.findChild(QPushButton, "start_button")
        self.stop_button = self.findChild(QPushButton, "stop_button")
        self.stop_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_video_capture)
        self.stop_button.clicked.connect(self.stop_video_capture)
        
        #output
        self.out = self.findChild(QLabel,'output')
       

    def display_frames(self, frame1_data, frame2_data):
        """Displays OpenCV frames onto the QLabels."""

        frame1_image = cv2.cvtColor(frame1_data, cv2.COLOR_BGR2RGB) 
        frame2_image = cv2.cvtColor(frame2_data, cv2.COLOR_BGR2RGB)

        frame1_qt_image = QImage(frame1_image.data, frame1_image.shape[1], frame1_image.shape[0], QImage.Format_RGB888)
        frame2_qt_image = QImage(frame2_image.data, frame2_image.shape[1], frame2_image.shape[0], QImage.Format_RGB888)

        self.frame1.setPixmap(QPixmap.fromImage(frame1_qt_image))
        self.frame2.setPixmap(QPixmap.fromImage(frame2_qt_image))


    def start_video_capture(self):
        self.stop_button.setEnabled(True) 
        self.start_button.setEnabled(False)
        self.cap = cv2.VideoCapture(0)  
        
        while self.cap.isOpened():
            ret, frame1 = self.cap.read()
            if not ret:
                break
            frame2,results = self.detector.apply_holistic(frame1)
            sentence = self.classifier.apply_classifier(results)
            self.out.setText(" ".join(sentence))
            
            self.display_frames(frame1, frame2)

    def stop_video_capture(self):

        if self.cap.isOpened():
            self.stop_button.setEnabled(False) 
            self.start_button.setEnabled(True)
            self.cap.release()  # Release the video capture object
            
            # Clear the labels to avoid displaying the last frame
            self.frame1.clear()
            self.frame2.clear()
        
        
            
    

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create a QApplication instance
    window = MyForm()  # Create an instance of your form class
    window.show()  # Display the window
    sys.exit(app.exec_())  # Start the Qt event loop    