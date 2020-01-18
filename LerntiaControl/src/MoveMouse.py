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
        print("data: ", self.data.x_middle)

        print("Current mouse position: " + str(self.mouse.position))

        # consider last 'numf' frames
        if self.prev_data:
            last_frames = self.prev_data[-numf:]

        # move mouse based on difference to gaze point
            # smallest_value = sys.maxsize
            # for f in last_frames:
            #    if f.x_middle < smallest_value:
            #        smallest_value = f.x_middle
            # if smallest_value < self.data.x_middle - x_sens:
            #    print("move right")
            #    self.mouse.move(x_step, 0)

            # weighted difference values
            xdifferences = []  # x - self.data.x_middle for x in last_frames]
            ydifferences = []  # y - self.data.y_middle for y in last_frames]

            for d in last_frames:
                # print("x_middle:", d.x_middle)
                # print("y_middle:", d.y_middle)
                xdifferences.append(self.data.x_middle - d.x_middle)
                ydifferences.append(self.data.y_middle - d.y_middle)

            # todo: consider x_sens and y_sens in difference
            # print("xlen: ", len(xdifferences))
            # print("ylen: ", len(ydifferences))

            # for f in xdifferences:
            #     print("xdiff: ", f)

            # for f in ydifferences:
            #     print("Y DIFF: ", f)

        # CRASH START
        #    if len(xdifferences):
        #        self.mouse.move(sum(xdifferences) / len(xdifferences), 0)
        #    if len(ydifferences):
        #        self.mouse.move(0, sum(ydifferences) / len(ydifferences))
        # CRASH END

        # if self.prev_data:  # and self.prev_data.x_middle > self.data.x_middle + x_sens:
        #    largest_value = -1
        #    for f in last_frames:
        #        if f.x_middle > largest_value:
        #            largest_value = f.x_middle
            # if largest_value > self.data.x_middle + x_sens:
            #    print("move left")
            #    self.mouse.move(-x_step, 0)

        # if self.prev_data:
        #    smallest_value = sys.maxsize
        #    for f in last_frames:
        #        if f.y_middle < smallest_value:
        #            smallest_value = f.y_middle
            # if smallest_value < self.data.y_middle - y_sens:
            #    print("move up")
            #    self.mouse.move(0, y_step)

        # if self.prev_data:
        #    largest_value = -1
        #    for f in last_frames:
        #        if f.y_middle > largest_value:
        #            largest_value = f.y_middle
            # if largest_value > self.data.y_middle + y_sens:
            #    print("move down")
            #    self.mouse.move(0, -y_step)

    def detect_head_nod(self):
        pass  # todo

        # print("x_middle point: ", self.data.x_middle)
        # if self.prev_data:
        #    print("x_middle point, previous: ", self.prev_data.x_middle)

        # set mouse position
        # self.mouse.position = (0, 0)
        # move mouse
        # self.mouse.move(100, 0)

        # mouse left click
        # self.mouse.click(Button.left, 1)
