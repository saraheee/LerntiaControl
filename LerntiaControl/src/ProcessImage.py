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
            print("a")
            rows, cols, _ = cut_eye.shape
            print("aa")
            gray_roi = cv2.cvtColor(cut_eye, cv2.COLOR_BGR2GRAY)
            # gray_roi = cv2.GaussianBlur(gray_roi, (2, 2), 0)
            print("b")
            _, threshold = cv2.threshold(gray_roi, 3, 255, cv2.THRESH_BINARY_INV)
            print("c", threshold)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            print("cc")
            if contours:
                contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
                print("d")
                for cnt in contours:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.drawContours(cut_eye, [cnt], -1, (0, 0, 255), 3)
                    cv2.rectangle(cut_eye, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.line(cut_eye, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
                    cv2.line(cut_eye, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
                    break

            # cv2.imshow("eye", gray_roi)
            # cv2.imshow("threshold", threshold)
            # cv2.waitKey(0)

            # circles = cv2.HoughCircles(cut_eye, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=50,
            #                                       minRadius=0, maxRadius=1)

            # circles = np.uint16(np.around(circles))
            # for i in circles[0, :]:
            # outer circle
            #    cv2.circle(cut_eye, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # circle center
            #    cv2.circle(cut_eye, (i[0], i[1]), 2, (0, 0, 255), 3)

            # cv2.imshow('circles', cut_eye)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


        print("left eye, x-coordinate: ", left_ex)
        return self.frame
