from pynput.mouse import Button, Controller

x_sens = 5
y_sens = 8
x_step = 50
y_step = 50


class MoveMouse:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data
        self.mouse = Controller()

    def move_mouse(self):
        print("data: ", self.data.gaze)

        print("Current mouse position: " + str(self.mouse.position))

        # move mouse based on different gaze points
        if self.prev_data and self.prev_data.gaze < self.data.gaze - x_sens:
            print("move right")
            self.mouse.move(x_step, 0)

        if self.prev_data and self.prev_data.gaze > self.data.gaze + x_sens:
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
