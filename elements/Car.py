class Car:
    def __init__(self, name):
        self.orientation = None
        self.name = name
        self.positions = []

    def add_position(self, x, y):
        self.positions.append((x, y))
        if len(self.positions) > 1:
            if self.positions[-1][0] == self.positions[-2][0]:
                self.orientation = "horizontal"
            elif self.positions[-1][1] == self.positions[-2][1]:
                self.orientation = "vertical"