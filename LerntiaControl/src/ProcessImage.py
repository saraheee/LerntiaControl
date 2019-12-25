import sys

import cv2
import numpy as np


class ProcessImage:

    def __init__(self, frame):
        self.frame = frame

    def pre_processing(self):
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # cv2.equalizeHist(self.frame, self.frame)
        return self.frame

    def detect_face_and_eyes(self, face_classifier, eye_classifier):
        left_ex = sys.maxsize
        left_ey = 0
        left_ew = 0
        left_eh = 0

        # objects = cv2.CascadeClassifier.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, maxSize)
        faces = face_classifier.detectMultiScale(self.frame, 1.35, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # detect eyes
            roi = self.frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(roi)
            i = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # get left eye by x-coordinate
                if ex < left_ex:
                    left_ex = ex
                    left_ey = ey
                    left_ew = ew
                    left_eh = eh
                i = i + 1
            if left_ex < sys.maxsize:
                cv2.rectangle(roi, (left_ex, left_ey), (left_ex + left_ew, left_ey + left_eh),
                              (0, 0, 255), 4)

            # cut face and eye out of the image
            cut_face = self.frame[y:y + h, x:x + w]
            cut_eye = cut_face[left_ey:left_ey + left_eh, left_ex:left_ex + left_ew]
            if cut_eye.size:
                cv2.imshow("cut_eye", cut_eye)

        print("left eye, x-coordinate: ", left_ex)
        return self.frame
