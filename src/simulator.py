from reader import read_time_series
from utils import attributed_pounds_co2

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
        self.time_delta = time_delta

    def run(self):
        for idx, observation in enumerate(self.time_series):
            if self.start_date <= observation.time <= self.end_date:

                proportion_on = self.model.action(observation.time)
                event = Event(observation.time, observation.moer, proportion_on)
                self.events.append(event)

                forecast = self.time_series[idx + self.horizon_n_timesteps]
                self.model.update_horizon(forecast.time, forecast.moer)

    def total_runtime(self):
        return sum(event.proportion_on for event in self.events) * self.time_delta

    def total_co2(self, power_in_kw):
        return sum(
            attributed_pounds_co2(event.proportion_on, event.moer, power_in_kw)
            for event in self.events
        )
