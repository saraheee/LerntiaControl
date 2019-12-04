import cv2


class ProcessImage:

    def __init__(self, frame):
        self.frame = frame

    def pre_processing(self):
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(self.frame, self.frame)
        return self.frame

    def detect_face_and_eyes(self, face_classifier, eye_classifier):
        # todo
        return self.frame

