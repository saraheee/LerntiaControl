# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'ui\MainWindow.ui'
import configparser
import re
import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from imutils.video import FPS

from lerntia_control_pkg.src.MoveMouse import MoveMouse
from lerntia_control_pkg.src.NodShakeMode import NodShakeMode
from lerntia_control_pkg.src.ProcessImage import ProcessImage

default_image = '../icon/control-teaser'

# models applied for basic face/eye detection
face_model = '../model/haarcascades/haarcascade_frontalface_alt.xml'
eye_model = '../model/haarcascades/haarcascade_eye_tree_eyeglasses.xml'

# models used for enhanced face detection
net = cv2.dnn.readNetFromCaffe('../model/deploy.prototxt.txt', '../model/res10_300x300_ssd_iter_140000.caffemodel')

# number of frames for click detection
clickf = 10

# path of the configuration file
config_path = r'../control.config'
css = "../ui/style.css"

nod_shake_mode = False
started = False
show_fps = False
ui = 0

print("Welcome to LerntiaControl!")
print("OpenCV Version: ", cv2.__version__)
print("Python Version: ", sys.version, '\n')


def set_config_parameters():
    """
    Set parameters of the config file.

    :return: none
    """
    global clickf, nod_shake_mode
    config_parser = configparser.RawConfigParser()
    config_parser.read(config_path)

    value = get_value(config_parser, 'frames', 'clickf')
    if value and int(value) > 0:
        clickf = int(value)

    value = get_value(config_parser, 'mode', 'nod_shake_mode')
    nod_shake_mode = bool(int(value))


def set_style_sheet(widget):
    """
    Set style sheet for a widget.

    :param widget: the widget to be styled
    :return: none
    """
    with open(css, "r") as fh:
        widget.setStyleSheet(fh.read())
    fh.close()


def get_value(parser, section, var):
    """
    Get a value from the config file.

    :param parser: the parser of the config file
    :param section: the section that contains the entry
    :param var: the variable that holds the value
    :return: the retrieved value
    """
    value = parser.get(section, var)
    value = re.search(r"[-+]?\d*\.\d+|\d+", value).group()
    return value


def on_click():
    """
    The main method that is called, when the start button is clicked. It connects to the camera, and calls methods for
    processing the camera image, for maintaining the mode, and for performing an action. In normal mode the actions are
    taken through mouse movements and mouse left clicks, while in 2-gestures mode keyboard events are accomplished.

    :return: none
    """
    global started
    if not started:
        activate_start_button()

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # connect to usb camera
        # cap = cv2.VideoCapture('../model/test.mp4')
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
        data = []
        click_data = []
        click_counter = 0
        m = MoveMouse(prev_data, data)
        m.center_mouse()

        mode2 = NodShakeMode(prev_data, data)

        while cap.isOpened():
            # capture frame
            ret, rgb_frame = cap.read()

            # end of the stream reached
            if not ret:
                break

            # process camera frame
            img = ProcessImage(rgb_frame)
            img.pre_processing()

            # detect face and eyes
            # data = img.detect_face_and_eyes(cv2.CascadeClassifier(face_model), cv2.CascadeClassifier(eye_model))
            data = img.detect_face_and_eyes_enhanced(net, cv2.CascadeClassifier(eye_model))

            if nod_shake_mode:  # navigate only through head-nod and head-shake (two gestures mode)
                mode2.set_data(prev_data, data)
                mode2.apply()

            else:  # normal mode with mouse movement
                # move mouse
                if m.wait_for_click:

                    # collect frames needed
                    if click_counter < clickf:
                        click_data.append(data)
                        click_counter = click_counter + 1
                    else:
                        # analyze mouse clicks
                        m.detect_head_nod(click_data)
                        click_counter = 0
                        click_data = []
                        if m.nod_detected:
                            prev_data = []
                            m.nod_detected = False
                else:
                    m.set_data(prev_data, data)
                    m.move_mouse()
            prev_data.append(data)

            # convert frame to qt format and display image in main window
            set_image_in_main_window(data.frame)

            # display frame in new window
            img = '[LerntiaControl] Kamerabild'
            cv2.imshow(img, data.frame)
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
    """
    Set the processed camera image in the main window of the user interface to show a status picture while using the
    application. Print a text on the image frame that indicates the active mode.

    :param frame: the processed image frame to set
    :return: none
    """
    global nod_shake_mode
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(rgb_image, ("Modus: 2 Gesten" if nod_shake_mode else "Modus: Normal"), (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (150, 255, 0), 6)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_qt_format.scaled(w / 3, h / 3, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    ui.camera_view.setPixmap(QPixmap(p))


def activate_pause_button():
    """
    Update the appearance of the pause button and show a default image when the application is stopped.

    :return: none
    """
    global started
    started = False
    ui.start_button.setText("Start")
    print('pause button clicked')
    set_image(default_image)


def activate_start_button():
    """
    Update the appearance of the start button when the application is started.

    :return: none
    """
    global started
    started = True
    ui.start_button.setText("Pause")
    print('start button clicked')


def set_image(img):
    """
    Set an image in the user interface that indicates the current status.

    :param img: the image to set
    :return: none
    """
    status_img = QPixmap(img)
    ui.camera_view.setPixmap(QPixmap(status_img))
    ui.camera_view.setScaledContents(True)


def change_mode():
    """
    Change the active mode. There are two modes available: 'normal' and '2-gestures'.

    :return: none
    """
    global nod_shake_mode
    nod_shake_mode = not nod_shake_mode
    print("mode changed to:", "2-gestures" if nod_shake_mode else "normal")


class Ui_MainWindow(object):
    """
    The main window of the user interface (ui). It defines all ui elements.

    """

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
        self.vertical_layout.addWidget(self.camera_view, 0)
        self.verticalLayout_2.addLayout(self.vertical_layout)
        set_image(default_image)

        self.start_button = QtWidgets.QPushButton(self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.start_button.setFont(font)
        self.start_button.setAutoRepeatInterval(93)
        self.start_button.setObjectName("start_button")
        self.verticalLayout_2.addWidget(self.start_button, 0)

        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 870, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu = QtWidgets.QMenu(self.menu_bar)
        self.menu.setObjectName("menu")
        font.setPointSize(14)
        self.menu_bar.setFont(font)
        self.menu.setFont(font)
        main_window.setMenuBar(self.menu_bar)

        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.change_mode = QtWidgets.QAction(main_window)
        self.change_mode.setObjectName("change_mode")
        self.menu.addAction(self.change_mode)
        self.menu_bar.addAction(self.menu.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        set_config_parameters()
        set_style_sheet(self.central_widget)
        set_style_sheet(self.start_button)
        set_style_sheet(self.menu_bar)

    def retranslate_ui(self, main_window):
        """
        Retranslate the view of the ui.

        :param main_window: the main window of the ui
        :return: none
        """
        global ui
        ui = self
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Status"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menu.setTitle(_translate("MainWindow", "Menü"))
        self.change_mode.setText(_translate("MainWindow", "Modus ändern"))

        # connect signals to slots
        self.start_button.clicked.connect(on_click)
        self.change_mode.triggered.connect(change_mode)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
