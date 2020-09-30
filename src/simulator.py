from utils import attributed_pounds_co2

from collections import namedtuple

Event = namedtuple("event", ["time", "moer", "proportion_on"])


class Simulator:
    def __init__(
        self,
        model,
        observations,
        start_date,
        end_date,
        forecast_duration,
        timestep_duration,
    ):

        self.observations = observations
        self.start_date = start_date
        self.end_date = end_date
        self.model = model
        self.events = []
        self.forecast_timestep_offset = int(forecast_duration / timestep_duration)
        self.timestep_duration = timestep_duration

    def run(self):
        for idx, observation in enumerate(self.observations):
            if self.start_date <= observation.time <= self.end_date:

                proportion_on = self.model.action(observation.time)
                event = Event(observation.time, observation.moer, proportion_on)
                self.events.append(event)

                next_forecast = self.observations[idx + self.forecast_timestep_offset]
                self.model.update_forecast(next_forecast.time, next_forecast.moer)

    def total_runtime(self):
        return (
            sum(event.proportion_on for event in self.events) * self.timestep_duration
        )

    def total_co2(self, power_in_kw):
        return sum(
            attributed_pounds_co2(event.proportion_on, event.moer, power_in_kw)
            for event in self.events
        )
