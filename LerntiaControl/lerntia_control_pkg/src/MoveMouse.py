from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from pynput.mouse import Button, Controller
from win32api import GetSystemMetrics

from FileReader import ConfigFileReader

x_sens = 0.7  # sensitivity in x direction
y_sens = 0.9  # sensitivity in y direction
x_step = 1.3  # movement steps in x direction
y_step = 1.5  # movement steps in y direction
numf = 10  # frame number for mouse movement
center_mouse = 0  # center mouse after every left click

pop_eps = 5  # shift of the popup window from the cursor to be able to click
nod_diff_eps = 4  # shift in weighted difference values of head nods for robustness
mouse_position = (0, 0)
config_path = r'../../config.yaml'


class MyPopup(QWidget):
    """
    Define a popup window to show a visual feedback to the user.

    """

    def __init__(self):
        """
        The constructor that sets the initialization parameters for the popup window.


        """
        QWidget.__init__(self)


def set_config_parameters():
    """
    Set config parameters for the mouse movements.

    :return: none
    """
    global x_sens, y_sens, x_step, y_step, numf, center_mouse
    f = ConfigFileReader()

    value = f.read_float('sensitivity', 'x_sens')
    x_sens = value if value != -1 else x_sens

    value = f.read_float('sensitivity', 'y_sens')
    y_sens = value if value != -1 else y_sens

    value = f.read_float('steps', 'x_step')
    x_step = value if value != -1 else x_step

    value = f.read_float('steps', 'y_step')
    y_step = value if value != -1 else y_step

    value = f.read_int('frames', 'numf')
    numf = value if value != -1 else numf

    value = f.read_bool('mouse', 'center_mouse')
    center_mouse = value if value != -1 else center_mouse


class MoveMouse:
    """
    Manage operations for performing mouse movements and mouse left clicks.

    """

    def __init__(self, prev_data, data):
        """
        The constructor that sets the initialization parameters for mouse movement operations.

        :param prev_data:
        :param data:
        """
        self.prev_data = prev_data
        self.data = data
        self.mouse = Controller()
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.wait_for_click = False
        self.nod_detected = False
        set_config_parameters()

    def set_data(self, prev_data, data):
        """
        Set data for the analysis of mouse movements and clicks.

        :param prev_data: the data of previous frames
        :param data: the data of the active frame
        :return: none
        """
        self.prev_data = prev_data
        self.data = data

    def move_mouse(self):
        """
        Move mouse based on the direction and speed retrieved from the data analyzed.
        Show a visual feedback as a popup window if the movement detected is in a certain range.

        :return: none
        """
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
        """
        Center the mouse position on the screen.

        :return: none
        """
        self.mouse.position = (self.width / 2, self.height / 2)

    def open_popup(self):
        """
        Open a popup window as a click indicator

        :return: none
        """
        self.w = MyPopup()
        self.w.setGeometry(QRect(self.mouse.position[0] + pop_eps, self.mouse.position[1] + pop_eps, 50, 50))
        self.w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.wait_for_click = True
        self.w.setStyleSheet("background-color: darkgray;")
        self.w.show()

    def save_mouse_position(self):
        """
        Save the active mouse position globally.

        :return: none
        """
        global mouse_position
        mouse_position = self.mouse.position

    def lock_mouse_position(self):
        """
        Lock the active mouse position.

        :return: none
        """
        global mouse_position
        self.mouse.position = mouse_position

    def detect_head_nod(self, click_data):
        """
        Detect whether a head nod is performed and do a left mouse click if it is the case. A head nod is detected
        when the weighted head movements in vertical position exceed the weighted movements in horizontal position
        with more than a threshold defined.

        :param click_data: the frame data that is analyzed for nod detection
        :return: none
        """
        self.lock_mouse_position()

        x_differences = []
        y_differences = []
        for d in click_data:
            x_differences.append(abs(self.data.x_middle - d.x_middle))
            y_differences.append(abs(self.data.y_middle - d.y_middle))

        self.nod_detected = sum(y_differences) > sum(x_differences) + nod_diff_eps

        if self.nod_detected:
            self.mouse.click(Button.left, 1)
            print("nod detected!")
            self.w.setStyleSheet("background-color: darkgreen;")
            if center_mouse:
                self.center_mouse()

        else:
            print("no nod")
            self.w.setStyleSheet("background-color: darkred;")

        self.wait_for_click = False
