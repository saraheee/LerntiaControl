import sys

import cv2
from imutils.video import FPS

from src.MoveMouse import MoveMouse
from src.ProcessImage import ProcessImage

default_image = '../icon/control-teaser'
face_model = '../model/haarcascades/haarcascade_frontalface_alt.xml'
eye_model = '../model/haarcascades/haarcascade_eye_tree_eyeglasses.xml'
started = False
show_fps = False
ui = 0

print("Welcome to LerntiaControl!")
print("OpenCV Version: ", cv2.__version__)
print("Python Version: ", sys.version, '\n')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # connect to usb camera
if cap.isOpened():
    print("WARNING: Failed to connect to usb camera! Connecting to internal camera instead.")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # connect to internal camera
    if not cap.isOpened():
        print("ERROR: Failed to connect to internal camera!")

    fps = FPS().start()

    if not cv2.CascadeClassifier(face_model):
        print("ERROR: Failed to load face detector!")

    if not cv2.CascadeClassifier(eye_model):
        print("ERROR: Failed to load eye detector!")

    prev_data = []

    while cap.isOpened():
        # capture frame
        ret, rgb_frame = cap.read()

        # end of the stream reached
        if not ret:
            break

        # process camera frame
        img = ProcessImage(rgb_frame)
        # img.pre_processing()

        # detect face and eyes
        data = img.detect_face_and_eyes(cv2.CascadeClassifier(face_model), cv2.CascadeClassifier(eye_model))

        # move mouse
        m = MoveMouse(prev_data, data)
        m.move_mouse()
        prev_data = data

        # perform mouse clicks
        # todo

        # display mirrored frame in new window
        img = '[LerntiaControl] Kamerabild'
        cv2.imshow(img, cv2.flip(data.frame, 1))
        fps.update()

        # stop fps timer
        fps.stop()

        # show/hide FPS information in console if F key is pressed
        if cv2.waitKey(1) == ord('f'):
            show_fps = not show_fps
        if show_fps:
            # print("INFO: Elapsed time: {:.2f}".format(fps.elapsed()))
            print("INFO: ~FPS: {:.2f}".format(fps.fps()))

        # if ESC, or pause-button pressed, or window closed => release camera handle and close image window
        if cv2.waitKey(1) == 27 or started is False or cv2.getWindowProperty(img, cv2.WND_PROP_VISIBLE) < 1:
            cap.release()
            cv2.destroyAllWindows()
            break
