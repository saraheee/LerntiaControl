import sys

import cv2
import numpy as np

conf_value = 0.10
face_color = (138, 0, 138)
face_color2 = (138, 138, 138)
face_eps = 10


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
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), face_color, 4)

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
                cv2.rectangle(roi, (left_ex, left_ey), (left_ex + left_ew, left_ey + left_eh), (0, 0, 255), 4)

            # cut face and eye out of the image
            cut_face = self.frame[y:y + h, x:x + w]
            cut_eye = cut_face[left_ey:left_ey + left_eh, left_ex:left_ex + left_ew]
            if cut_eye.size:
                cv2.imshow("cut_eye", cut_eye)

        return ProcessedImage(self.frame, cut_face, cut_eye, left_ex, left_ey)

    def detect_face_and_eyes_enhanced(self, net, eye_classifier):
        left_ey = 0
        right_ey = 0
        left_ew = 0
        right_ew = 0
        left_eh = 0
        right_eh = 0

        cut_face = self.frame
        # cut_eye = self.frame
        cut_left_eye = self.frame
        cut_right_eye = self.frame

        (h, w) = self.frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        faces = []
        left_faces = []
        right_faces = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < conf_value:
                print("INFO: Face found with confidence below threshold. Confidence value: ", confidence)

            if confidence >= conf_value:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                text = "Face: {:.2f}%".format(confidence * 100)
                y = startY - face_eps if startY - face_eps > 10 else startY + face_eps

                print("END X: ", endX)

                # left face half
                cv2.rectangle(self.frame, (startX, startY), (endX-int((endX-startX)/2)+face_eps, endY), face_color, 4)

                # right face half
                cv2.rectangle(self.frame, (startX+int((endX-startX)/2)-face_eps, startY), (endX, endY), face_color2, 4)
                # cv2.rectangle(self.frame, (x, y), (x + w, y + h), face_color, 4)

                # faces.append([startX, startY, endX - startX, endY - startY])
                left_faces.append([startX, startY, (endX-int((endX-startX)/2)+face_eps-startX), endY-startY])
                right_faces.append([startX+int((endX-startX)/2)-face_eps, startY, endX - startX, endY - startY])
                cv2.putText(self.frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 1, face_color, 2)
                break

        # for left eye
        left_ex = sys.maxsize
        for (x, y, w, h) in left_faces:
            # todo: move to method
            print("x, y, w, h: ", x, y, w, h)

            # detect eyes
            roi = self.frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(roi)
            i = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # get most left eye by x-coordinate
                if ex < left_ex:
                    left_ex = ex
                    left_ey = ey
                    left_ew = ew
                    left_eh = eh
                i = i + 1
            if left_ex < sys.maxsize:
                cv2.rectangle(roi, (left_ex, left_ey), (left_ex + left_ew, left_ey + left_eh), (0, 0, 255), 4)

            # cut face and eye out of the image
            cut_face = self.frame[y:y + h, x:x + w]
            cut_left_eye = cut_face[left_ey:left_ey + left_eh, left_ex:left_ex + left_ew]
            if cut_left_eye.size:
                cv2.imshow("left_eye", cut_left_eye)

        # for right eye
        right_ex = 0
        for (x, y, w, h) in right_faces:
            # todo: move to method
            print("x, y, w, h: ", x, y, w, h)

            # detect eyes
            roi = self.frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(roi)
            i = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # get most right eye by x-coordinate
                if ex > right_ex:
                    right_ex = ex
                    right_ey = ey
                    right_ew = ew
                    right_eh = eh
                i = i + 1
            if left_ex > 0:
                cv2.rectangle(roi, (right_ex, right_ey), (right_ex + right_ew, right_ey + right_eh), (0, 0, 255), 4)

            # cut face and eye out of the image
            cut_face = self.frame[y:y + h, x:x + w]
            cut_right_eye = cut_face[right_ey:right_ey + right_eh, right_ex:right_ex + right_ew]
            if cut_right_eye.size:
                cv2.imshow("right_eye", cut_right_eye)

        # cv2.imshow("both_eye", np.hstack(cut_left_eye, cut_left_eye))
        return ProcessedImage(self.frame, cut_face, cut_left_eye, int(round((left_ex+right_ex)/2)), int(round((left_ey+right_ey)/2)))


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
