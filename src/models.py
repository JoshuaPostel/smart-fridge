class NaiveModel:
    def __init__(self):
        self.counter = 0

    def update(self, time, moer):
        self.counter += 1
        if self.counter % 3 == 0:
            return 1
        else:
            return 0
