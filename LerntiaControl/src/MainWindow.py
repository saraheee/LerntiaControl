# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'ui\MainWindow.ui'

import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from imutils.video import FPS

from src.ProcessImage import ProcessImage
from src.MoveMouse import MoveMouse

default_image = '../icon/control-teaser'
face_model = '../model/haarcascades/haarcascade_frontalface_alt.xml'
eye_model = '../model/haarcascades/haarcascade_eye_tree_eyeglasses.xml'
started = False
show_fps = False
ui = 0

print("Welcome to LerntiaControl!")
print("OpenCV Version: ", cv2.__version__)
print("Python Version: ", sys.version, '\n')


def on_click():
    global started
    if not started:
        activate_start_button()

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # connect to usb camera
        if not cap.isOpened():
            print("WARNING: Failed to connect to usb camera! Connecting to internal camera instead.")
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # connect to internal camera
            if not cap.isOpened():
                print("ERROR: Failed to connect to internal camera!")
                return

        fps = FPS().start()

        if not cv2.CascadeClassifier(face_model):
            print("ERROR: Failed to load face detector!")
            return

        if not cv2.CascadeClassifier(eye_model):
            print("ERROR: Failed to load eye detector!")
            return

        prev_data = []

        while cap.isOpened():
            # capture frame
            ret, rgb_frame = cap.read()

            # end of the stream reached
            if not ret:
                break

            # frame = imutils.resize(frame, width=450)
            # frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
            # frame = np.dstack([frame, frame, frame])

            # process camera frame
            img = ProcessImage(rgb_frame)
            # img.pre_processing()

            # detect face and eyes
            data = img.detect_face_and_eyes(cv2.CascadeClassifier(face_model), cv2.CascadeClassifier(eye_model))

            # move mouse
            m = MoveMouse(prev_data, data)
            m.move_mouse()
            prev_data.append(data)

            # perform mouse clicks
            # todo

            # convert mirrored frame to qt format and display image in main window
            set_image_in_main_window(data.frame)

            # display mirrored frame in new window
            img = '[LerntiaControl] Kamerabild'
            cv2.imshow(img, cv2.flip(data.frame, 1))
            fps.update()

            # stop fps timer
            fps.stop()

            # show/hide FPS information in console if F key is pressed
            global show_fps
            if cv2.waitKey(1) == ord('f'):
                show_fps = not show_fps
            if show_fps:
                # print("INFO: Elapsed time: {:.2f}".format(fps.elapsed()))
                print("INFO: ~FPS: {:.2f}".format(fps.fps()))

            # if ESC, or pause-button pressed, or window closed => release camera handle and close image window
            if cv2.waitKey(1) == 27 or started is False or cv2.getWindowProperty(img, cv2.WND_PROP_VISIBLE) < 1:
                cap.release()
                cv2.destroyAllWindows()
                activate_pause_button()
                break

    else:
        activate_pause_button()


def set_image_in_main_window(frame):
    rgb_image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    cv2.putText(rgb_image, "CAMERA ", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (150, 255, 0), 6)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_qt_format.scaled(w / 3, h / 3, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    ui.camera_view.setPixmap(QPixmap(p))


def activate_pause_button():
    global started
    started = False
    ui.start_button.setText("Start")
    print('pause button clicked')
    set_image(default_image)


def activate_start_button():
    global started
    started = True
    ui.start_button.setText("Pause")
    print('start button clicked')


def set_image(img):
    status_img = QPixmap(img)
    ui.camera_view.setPixmap(QPixmap(status_img))
    ui.camera_view.setScaledContents(True)


class Ui_MainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        main_window.setWindowIcon(QtGui.QIcon('../icon/control.ico'))

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout")

        self.camera_view = QLabel(self.central_widget)
        self.camera_view.setObjectName("camera_view")
        self.vertical_layout.addWidget(self.camera_view)
        self.verticalLayout_2.addLayout(self.vertical_layout)
        set_image(default_image)

        self.start_button = QtWidgets.QPushButton(self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.start_button.setFont(font)
        self.start_button.setAutoRepeatInterval(93)
        self.start_button.setObjectName("start_button")
        self.verticalLayout_2.addWidget(self.start_button)

        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 870, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu = QtWidgets.QMenu(self.menu_bar)
        self.menu.setObjectName("menu")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.do_something = QtWidgets.QAction(main_window)
        self.do_something.setObjectName("do_something")
        self.menu.addAction(self.do_something)
        self.menu_bar.addAction(self.menu.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        global ui
        ui = self
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Status"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menu.setTitle(_translate("MainWindow", "Menü"))
        self.do_something.setText(_translate("MainWindow", "Klick"))

        # connect signals to slots
        self.start_button.clicked.connect(on_click)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
