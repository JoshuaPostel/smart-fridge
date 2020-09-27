from reader import read_time_series

from datetime import timedelta
from collections import namedtuple

Event = namedtuple("event", ["time", "moer", "proportion_on"])


class Simulator:
    def __init__(self, model, input_file, start_date, end_date, horizon, time_delta):

        self.time_series = read_time_series(input_file)
        self.start_date = start_date
        self.end_date = end_date
        self.model = model
        self.events = []
        self.horizon_n_timesteps = int(horizon / time_delta)

    def run(self):
        for idx, observation in enumerate(self.time_series):
            if self.start_date <= observation.time <= self.end_date:

                proportion_on = self.model.action(observation.time)
                event = Event(observation.time, observation.moer, proportion_on)
                self.events.append(event)

                forecast = self.time_series[idx + self.horizon_n_timesteps]
                self.model.update_horizon(forecast.time, forecast.moer)

    def plot(self):
        pass

    def total_runtime(self):
        # TODO fiture out what unit to return
        event_length = self.time_delta / timedelta(hours=1)
        return (event.proportion_on for event in self.events).sum() * event_length

    def total_co2(self):
        pass
