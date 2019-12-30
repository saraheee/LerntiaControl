import sys

import cv2
import numpy as np

conf_value = 0.85
face_color = (138, 0, 138)


class ProcessImage:

    def __init__(self, frame):
        self.frame = frame

    def pre_processing(self):
        # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.frame = cv2.flip(self.frame, 1)
        return self.frame

    def detect_face_and_eyes(self, face_classifier, eye_classifier):
        left_ex = sys.maxsize
        left_ey = 0
        left_ew = 0
        left_eh = 0

        cut_face = self.frame
        cut_eye = self.frame

        # objects = cv2.CascadeClassifier.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, maxSize)
        faces = face_classifier.detectMultiScale(self.frame, 1.35, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # detect eyes
            cut_eye = detect_eyes(x, y, w, h)

        return ProcessedImage(self.frame, cut_face, cut_eye, left_ex, left_ey)

    def detect_face_and_eyes_enhanced(self, net):

        (h, w) = self.frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < conf_value:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "Face: {:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(self.frame, (startX, startY), (endX, endY), face_color, 4)
            cv2.putText(self.frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 1, face_color, 2)

        return EnhancedProcessing(self.frame)

    def detect_eyes(self, x, y, w, h):
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

class ProcessedImage:
    def __init__(self, frame, face, eye, xgaze, ygaze):
        self.frame = frame
        self.face = face
        self.eye = eye
        self.xgaze = xgaze
        self.ygaze = ygaze


class EnhancedProcessing:
    def __init__(self, frame):
        self.frame = frame
