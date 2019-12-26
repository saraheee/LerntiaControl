class MoveMouse:

    def __init__(self, prev_data, data):
        self.prev_data = prev_data
        self.data = data

    def move_mouse(self):
        print("data: ", self.data.gaze)
        # move mouse based on different gaze points
        if self.prev_data and self.prev_data.gaze < self.data.gaze:
            print("move right")

        if self.prev_data and self.prev_data.gaze > self.data.gaze:
            print("move left")

        print("gaze point: ", self.data.gaze)
        if self.prev_data:
            print("gaze point, previous: ", self.prev_data.gaze)

