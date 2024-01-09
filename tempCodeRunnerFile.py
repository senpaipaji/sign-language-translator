

    
    
    def stop_video_capture(self):

        if self.cap.isOpened():
            self.stop_button.setEnabled(False) 
            self.start_button.setEnabled(True)
            self.cap.release()  # Release the video capture object
            