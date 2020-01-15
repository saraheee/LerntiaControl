import sys

from pynput.mouse import Button, Controller

x_sens = 15
y_sens = 15
x_step = 50
y_step = 40
numf = 20


class MoveMouse:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data
        self.mouse = Controller()

    def move_mouse(self):
        print("data: ", self.data.xgaze)

        print("Current mouse position: " + str(self.mouse.position))

        # consider last 'numf' frames
        if self.prev_data:
            last_frames = self.prev_data[-numf:]

        # move mouse based on difference to gaze point
            # smallest_value = sys.maxsize
            # for f in last_frames:
            #    if f.xgaze < smallest_value:
            #        smallest_value = f.xgaze
            # if smallest_value < self.data.xgaze - x_sens:
            #    print("move right")
            #    self.mouse.move(x_step, 0)

            # weighted difference values
            xdifferences = []  # x - self.data.xgaze for x in last_frames]
            ydifferences = []  # y - self.data.ygaze for y in last_frames]

            for d in last_frames:
                xdifferences.append(self.data.xgaze - d.xgaze)
                ydifferences.append(self.data.ygaze - d.ygaze)

            # todo: consider x_sens and y_sens in difference
            for f in xdifferences:
                print("xdiff: ", f)

            for f in ydifferences:
                print("Y DIFF: ", f)

        # if self.prev_data:  # and self.prev_data.xgaze > self.data.xgaze + x_sens:
        #    largest_value = -1
        #    for f in last_frames:
        #        if f.xgaze > largest_value:
        #            largest_value = f.xgaze
            # if largest_value > self.data.xgaze + x_sens:
            #    print("move left")
            #    self.mouse.move(-x_step, 0)

        # if self.prev_data:
        #    smallest_value = sys.maxsize
        #    for f in last_frames:
        #        if f.ygaze < smallest_value:
        #            smallest_value = f.ygaze
            # if smallest_value < self.data.ygaze - y_sens:
            #    print("move up")
            #    self.mouse.move(0, y_step)

        # if self.prev_data:
        #    largest_value = -1
        #    for f in last_frames:
        #        if f.ygaze > largest_value:
        #            largest_value = f.ygaze
            # if largest_value > self.data.ygaze + y_sens:
            #    print("move down")
            #    self.mouse.move(0, -y_step)

    def detect_head_nod(self):
        pass  # todo

        # print("xgaze point: ", self.data.xgaze)
        # if self.prev_data:
        #    print("xgaze point, previous: ", self.prev_data.xgaze)

        # set mouse position
        # self.mouse.position = (0, 0)
        # move mouse
        # self.mouse.move(100, 0)

        # mouse left click
        # self.mouse.click(Button.left, 1)
