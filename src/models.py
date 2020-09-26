class NaiveModel:
    def __init__(self):
        self.counter = 0
        self.horizon = []

    def action(self, time):
        self.counter += 1
        if self.counter % 3 == 0:
            return 1
        else:
            return 0

    def update_horizon(self, time, moer):
        pass
