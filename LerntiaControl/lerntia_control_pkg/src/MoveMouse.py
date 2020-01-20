from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from pynput.mouse import Button, Controller
from win32api import GetSystemMetrics

x_sens = 0.5
y_sens = 0.7
x_step = 1.1
y_step = 0.8
numf = 10  # frame number
pop_eps = 5
nod_diff_eps = 4
mouse_position = (0, 0)
nod_threshold = 10


class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)


class MoveMouse:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data
        self.mouse = Controller()
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.wait_for_click = False
        self.nod_detected = False

    def set_data(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data

    def move_mouse(self):
        # print("data: ", self.data.x_middle)
        # print("Current mouse position: " + str(self.mouse.position))

        # consider last 'numf' frames
        if self.prev_data:
            last_frames = self.prev_data[-numf:]

            # weighted difference values
            x_differences = []
            y_differences = []

            for d in last_frames:
                x_differences.append(self.data.x_middle - d.x_middle)
                y_differences.append(self.data.y_middle - d.y_middle)

            x_cond = []
            y_cond = []

            if len(x_differences):
                # print("x len: ", len(x_differences))
                # print("x val: ", sum(x_differences) / len(x_differences))
                x_value = sum(x_differences) / len(x_differences) * x_step
                x_cond = x_value > x_sens or x_value < -x_sens
                if x_cond:
                    self.mouse.move(x_value, 0)

            if len(y_differences):
                # print("y len: ", len(x_differences))
                # print("y val: ", sum(x_differences) / len(x_differences))
                y_value = sum(y_differences) / len(y_differences) * y_step
                y_cond = y_value > y_sens or y_value < -y_sens
                if y_cond:
                    self.mouse.move(0, y_value)

            if len(x_differences) and len(y_differences):
                if not x_cond and not y_cond:
                    self.open_popup()
                    self.save_mouse_position()

    def center_mouse(self):
        self.mouse.position = (self.width / 2, self.height / 2)

    def open_popup(self):  # popup window as a click indicator
        self.w = MyPopup()
        self.w.setGeometry(QRect(self.mouse.position[0] + pop_eps, self.mouse.position[1] + pop_eps, 50, 50))
        self.w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.wait_for_click = True
        self.w.setStyleSheet("background-color: darkgray;")
        self.w.show()

    def save_mouse_position(self):
        global mouse_position
        mouse_position = self.mouse.position

    def lock_mouse_position(self):
        global mouse_position
        self.mouse.position = mouse_position

    def detect_head_nod(self, click_data):
        self.lock_mouse_position()

        x_differences = []
        y_differences = []
        for d in click_data:
            x_differences.append(abs(self.data.x_middle - d.x_middle))
            y_differences.append(abs(self.data.y_middle - d.y_middle))

        self.nod_detected = sum(y_differences) > sum(x_differences) + nod_diff_eps
        print("y differences: ", sum(y_differences))

        if self.nod_detected:
            self.mouse.click(Button.left, 1)
            print("nod detected!")
            self.w.setStyleSheet("background-color: darkgreen;")

        else:
            print("no nod")
            self.w.setStyleSheet("background-color: darkred;")

        self.wait_for_click = False
