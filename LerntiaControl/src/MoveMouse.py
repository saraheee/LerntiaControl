import pyglet as pyglet
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from pyglet import canvas
from pynput.mouse import Button, Controller
import tkinter as tk
import win32gui
import win32api
import turtle
from win32api import GetSystemMetrics

x_sens = 0.5
y_sens = 0.5
x_step = 1.1
y_step = 0.8
numf = 20  # frame number


def change_mouse_cursor():
    pass
    # image = pyglet.image.load('../icon/control.png')
    # cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
    # window.set_mouse_cursor(cursor)

    # window = pyglet.window.Window()
    # cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
    # cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
    # window.set_mouse_cursor(cursor)

    # dc = win32gui.GetDC(0)
    # red = win32api.RGB(255, 0, 0)
    # win32gui.SetPixel(dc, 50, 20, red)  # draw red at 0,0

    # root = tk.Tk()
    # root.bind("<Motion>", motion)

    # canvas = tk.Canvas(root)
    # canvas.config(cursor='circle')


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

    def move_mouse(self):
        print("data: ", self.data.x_middle)

        print("Current mouse position: " + str(self.mouse.position))

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
                print("x len: ", len(x_differences))
                print("x val: ", sum(x_differences) / len(x_differences))
                x_value = sum(x_differences) / len(x_differences) * x_step
                x_cond = x_value > x_sens or x_value < -x_sens
                if x_cond:
                    self.mouse.move(x_value, 0)

            if len(y_differences):
                print("y len: ", len(x_differences))
                print("y val: ", sum(x_differences) / len(x_differences))
                y_value = sum(y_differences) / len(y_differences) * y_step
                y_cond = y_value > y_sens or y_value < -y_sens
                if y_cond:
                    self.mouse.move(0, y_value)

            if len(x_differences) and len(y_differences):
                if not x_cond and not y_cond:
                    # change_mouse_cursor()
                    self.open_popup()
                    self.mouse.click(Button.left, 1)  # todo: change mouse and detect click gesture

    def center_mouse(self):
        self.mouse.position = (self.width / 2, self.height / 2)

    def open_popup(self):  # popup window as a click indicator
        self.w = MyPopup()
        self.w.setGeometry(QRect(self.mouse.position[0], self.mouse.position[1], 100, 100))
        self.w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.w.show()

    def detect_head_nod(self):
        pass  # todo
