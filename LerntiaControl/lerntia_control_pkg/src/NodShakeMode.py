from pynput.keyboard import Key, Controller

num_frames = 20
nod_diff_eps = 150
shake_diff_eps = 200


class NodShakeMode:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data
        self.nod_detected = False
        self.shake_detected = False
        self.keyboard = Controller()

    def set_data(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data

    def apply(self):
        if self.prev_data and self.data:
            last_frames = self.prev_data[-num_frames:]

            # weighted difference values
            x_differences = []
            y_differences = []

            for d in last_frames:
                x_differences.append(abs(self.data.x_middle - d.x_middle))
                y_differences.append(abs(self.data.y_middle - d.y_middle))

            self.shake_detected = sum(x_differences) > sum(y_differences) + shake_diff_eps
            self.nod_detected = sum(y_differences) > sum(x_differences) + nod_diff_eps

            # print("x differences: ", sum(x_differences))
            # print("y differences: ", sum(y_differences))

        if self.nod_detected:
            print("nod detected!")
            # click and go to next button
            self.keyboard.press(Key.space)
            self.keyboard.press(Key.tab)

        elif self.shake_detected:
            print("shake detected!")
            # go to next button
            self.keyboard.press(Key.tab)

        # else:
            # print("nothing detected")

