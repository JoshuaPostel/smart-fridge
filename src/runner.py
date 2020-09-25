from reader import read_time_series


class Simulator:
    def __init__(self, model, input_file, start_date, end_date, power_consumption):

        self.time_series = read_time_series(input_file)
        self.start_date = start_date
        self.end_date = end_date
        self.model = model
        self.history = []

    def run(self):
        for observation in self.time_series:
            is_on = self.model.update(observation.time, observation.moer)
            self.history.append(is_on)

    def plot(self):
        pass

    def total_runtime(self):
        return self.history.sum() * 5

    def total_co2(self):
        pass
