import sys

from pynput.mouse import Button, Controller

x_sens = 50
y_sens = 80
x_step = 50
y_step = 50
numf = 10


class MoveMouse:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data
        self.mouse = Controller()

    def move_mouse(self):
        print("data: ", self.data.gaze)

        print("Current mouse position: " + str(self.mouse.position))

        # consider last 'numf' frames
        last_frames = self.prev_data[-numf:]

        # move mouse based on different gaze points
        if self.prev_data:  # and self.prev_data.gaze < self.data.gaze - x_sens:
            smallest_value = sys.maxsize
            for f in last_frames:
                if f.gaze < smallest_value:
                    smallest_value = f.gaze
            if smallest_value < self.data.gaze - x_sens:

                print("move right")
                self.mouse.move(x_step, 0)

        if self.prev_data:  # and self.prev_data.gaze > self.data.gaze + x_sens:
            largest_value = -1
            for f in last_frames:
                if f.gaze > largest_value:
                    largest_value = f.gaze
            if largest_value > self.data.gaze + x_sens:

                print("move left")
                self.mouse.move(-x_step, 0)

        # print("gaze point: ", self.data.gaze)
        # if self.prev_data:
        #    print("gaze point, previous: ", self.prev_data.gaze)

        # set mouse position
        # self.mouse.position = (0, 0)
        # move mouse
        # self.mouse.move(100, 0)

        # mouse left click
        # self.mouse.click(Button.left, 1)
