import sys

import cv2
import numpy as np

conf_value = 0.10
face_left_color = (138, 0, 138)
face_right_color = (138, 138, 138)
face_middle_color = (0, 138, 0)
face_eps = 10
middle_point = []


class ProcessImage:
    """
    Process the image frame, detect face and eyes, and retrieve the middle point for consequent mouse and key actions.

    """

    def __init__(self, frame):
        """
        The constructor that sets the initialization parameters for the class.

        :param frame: the initial image frame to be processed
        """
        self.frame = frame

    def pre_processing(self):
        """
        Conduct a preprocessing on the image frame.

        :return: the preprocessed image frame
        """
        # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.frame = cv2.flip(self.frame, 1)
        return self.frame

    def detect_face_and_eyes(self, face_classifier, eye_classifier):
        """
        Detect face and eyes in the image frame and return the data processed, as an image object.
        This method is outdated. For enhanced results, the method `detect_face_and_eyes_enhanced` is used instead.

        :param face_classifier: the classifier for detecting the face
        :param eye_classifier: the classifier for detecting eyes
        :return: the data of the processed image frame
        """
        left_ex = sys.maxsize
        left_ey = 0
        left_ew = 0
        left_eh = 0

        # objects = cv2.CascadeClassifier.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, maxSize)
        faces = face_classifier.detectMultiScale(self.frame, 1.35, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), face_left_color, 4)

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

        return ProcessedImage(self.frame, left_ex, left_ey)

    def detect_face_and_eyes_enhanced(self, net, eye_classifier):
        """
        An enhanced method for face and eye detection. Faces are detected through a pretrained network. Every eye is
        searched for separately in a vertical face half. The reference point is computed from both eye positions if
        available, or estimated if no two eyes are detected.

        :param net: the network used for face detection
        :param eye_classifier: the classifier used for eye detection
        :return: the data of the processed image frame
        """
        left_ey = 0
        right_ey = 0
        left_ew = 0
        right_ew = 0
        left_eh = 0
        right_eh = 0

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

                # left face half
                cv2.rectangle(self.frame, (startX, startY), (endX - int((endX - startX) / 2) + face_eps, endY),
                              face_left_color, 4)

                # right face half
                cv2.rectangle(self.frame, (startX + int((endX - startX) / 2) - face_eps, startY), (endX, endY),
                              face_right_color, 4)

                faces.append([startX, startY, endX - startX, endY - startY])
                left_faces.append(
                    [startX, startY, (endX - int((endX - startX) / 2) + face_eps - startX), endY - startY])
                right_faces.append([startX + int((endX - startX) / 2) - face_eps, startY, endX - startX, endY - startY])
                cv2.putText(self.frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 1, face_left_color, 2)
                break

        # for left eye
        left_ex = sys.maxsize
        x_left_face = 0
        y_left_face = 0
        for (x, y, w, h) in left_faces:

            # detect eyes
            roi = self.frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(roi)
            i = 0
            for (ex, ey, ew, eh) in eyes:
                # get most left eye by x-coordinate
                if ex < left_ex:
                    left_ex = ex
                    left_ey = ey
                    left_ew = ew
                    left_eh = eh
                    x_left_face = x
                    y_left_face = y
                i = i + 1
            if left_ex < sys.maxsize:
                cv2.rectangle(roi, (left_ex, left_ey), (left_ex + left_ew, left_ey + left_eh), face_left_color, 4)

        # for right eye
        right_ex = 0
        x_right_face = 0
        y_right_face = 0
        for (x, y, w, h) in right_faces:
            # detect eyes
            roi = self.frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(roi)
            i = 0
            for (ex, ey, ew, eh) in eyes:
                # get most right eye by x-coordinate
                if ex > right_ex:
                    right_ex = ex
                    right_ey = ey
                    right_ew = ew
                    right_eh = eh
                    x_right_face = x
                    y_right_face = y
                i = i + 1
            if right_ex > 0:
                cv2.rectangle(roi, (right_ex, right_ey), (right_ex + right_ew, right_ey + right_eh), face_right_color,
                              4)

        global middle_point
        if left_ex < sys.maxsize and right_ex > 0:

            # point for left eye
            left_point = (x_left_face + left_ex, y_left_face + left_ey + int(round(left_eh / 2)))
            cv2.circle(self.frame, left_point, 10, face_left_color, -1)

            # point for right eye
            right_point = (x_right_face + right_ex + right_ew, y_right_face + right_ey + int(round(right_eh / 2)))
            cv2.circle(self.frame, right_point, 10, face_right_color, -1)

            middle_point = int(round((left_point[0] + right_point[0]) / 2)), int(round((left_point[1] + right_point[1])
                                                                                       / 2))
        else:
            if len(faces) > 0:
                for (x, y, w, h) in faces:  # relevant only if a face but no eyes are recognized
                    middle_point = int(round((x + (x + w)) / 2)), int(round((y + (y + h)) / 2)) - 2 * face_eps
            if not len(middle_point) > 0:  # no middle point retrieved before, if no face and no eyes are found
                middle_point = (0, 0)
        cv2.circle(self.frame, middle_point, 10, face_middle_color, -1)

        return ProcessedImage(self.frame, middle_point[0], middle_point[1])


class ProcessedImage:
    """
    The data of the processed image frame, which is calculated from face and eye positions.

    """

    def __init__(self, frame, x_middle, y_middle):
        """
        The constructor that sets the initialization parameters for the processed image class.

        :param frame: the processed frame after face and eye detection
        :param x_middle: the x coordinate of the retrieved reference point
        :param y_middle: the y coordinate of the retrieved reference point
        """
        self.frame = frame
        self.x_middle = x_middle
        self.y_middle = y_middle
