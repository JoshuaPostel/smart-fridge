from models import LinearProgramming
from simulator import Simulator
from plotter import plot_refrigerator
from reader import read_time_series

from datetime import datetime, timedelta
from pathlib import Path

# TODO implement as a config file
##############
# parameters #
##############
initial_temprature = 33
maximum_temprature = 43
minimum_temprature = 33

# temprature(t + 1) = temprature(t) + delta_off + (delta_on * fridge_on(t))
# where fridge_on(t) -> [0,1]
delta_on = -10 / 12
delta_off = 5 / 12
fridge_power_kw = 0.2

start_date = datetime(2019, 3, 1)
end_date = datetime(2019, 4, 1)

forecast_duration = timedelta(hours=1)
timestep_duration = timedelta(minutes=5)

optimization_horizon_timesteps = 24
##############


repo_root = Path(__file__).resolve().parent.parent

observations = read_time_series(repo_root / "data" / "MOERS.csv")
initial_forecast = [
    observation.moer
    for observation in observations
    if start_date <= observation.time <= start_date + forecast_duration
]

lp_model = LinearProgramming(
    initial_forecast,
    initial_temprature,
    delta_on,
    delta_off,
    minimum_temprature,
    maximum_temprature,
    optimization_horizon_timesteps,
)

sim = Simulator(
    lp_model, observations, start_date, end_date, forecast_duration, timestep_duration
)

sim.run()

# TODO
total_co2 = sim.total_co2(fridge_power_kw / 12)
print(f"total associated CO2: {round(total_co2, 3)} lbs")

total_runtime = sim.total_runtime()
print(f"total fridge run time: {total_runtime}")

plot_refrigerator(
    repo_root / "output" / "refrigerator.png",
    sim.events,
    fridge_power_kw,
    delta_on,
    delta_off,
    maximum_temprature,
    minimum_temprature,
    initial_temprature,
)
