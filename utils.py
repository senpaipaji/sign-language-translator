import cv2
import os
from tensorflow.keras.models import load_model
import mediapipe as mp
import numpy as np


class HolisticDetector:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils

    def mediapipe_detection(self, img, model):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        results = model.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img, results

    def draw_landmarks(self, img, results):
        self.mp_drawing.draw_landmarks(img, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
        self.mp_drawing.draw_landmarks(img, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        self.mp_drawing.draw_landmarks(img, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

    def apply_holistic(self, frame):
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            image, results = self.mediapipe_detection(frame, holistic)
            self.draw_landmarks(image, results)
        return image, results

class HolisticClassifier:
    def __init__(self,path='model_final.keras',threshold = 0.6):
        if os.path.exists(path):
            self.signs = ['hello','how','you','people']
            self.model = load_model(path)
            self.sequence = []
            self.sentence = []
            self.threshold = threshold
        else:
            raise Exception('unable to load model')
    
    def extract_data(self,results):
        left_hand_data = np.array([[res.x,res.y,res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        right_hand_data = np.array([[res.x,res.y,res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([left_hand_data,right_hand_data])
    
    def apply_classifier(self,results):
        keypoints_data = self.extract_data(results)
        self.sequence.append(keypoints_data)
        self.sequence = self.sequence[-30:]
        if len(self.sequence) == 30:
            res = self.model.predict(np.expand_dims(self.sequence,axis=0))[0]
            word = self.signs[np.argmax(res)]
            curr_threshold = np.max(res)
            if curr_threshold > self.threshold:
                if len(self.sentence) > 0:
                    if word != self.sentence[-1]:
                        self.sentence.append(word)
                else:
                    self.sentence.append(word)
        if len(self.sentence) > 5:
            self.sentence = self.sentence[-5:]
        return self.sentence
        