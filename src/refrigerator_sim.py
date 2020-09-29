from models import LinearProgramming
from simulator import Simulator
from plotter import plot_refrigerator
from reader import read_time_series

from datetime import datetime, timedelta
from pathlib import Path

data_file = Path("/home/jpostel1/proj/watt-time/data/MOERS.csv")
horizon = [
    observation.moer
    for observation in read_time_series(data_file)
    if datetime(2019, 3, 1) <= observation.time < datetime(2019, 3, 1, 1)
]

lp_model = LinearProgramming(
    initial_horizon=horizon,
    initial_temp=33,
    temp_delta_on=-10 / 12,
    temp_delta_off=5 / 12,
    temp_min=33,
    temp_max=43,
    optimization_timesteps=24,
)

sim = Simulator(
    model=lp_model,
    input_file=data_file,
    start_date=datetime(2019, 3, 1),
    end_date=datetime(2019, 4, 1),
    horizon=timedelta(hours=1),
    time_delta=timedelta(minutes=5),
)

sim.run()

# TODO implement configs to avoid the amount of parameter passing
plot_refrigerator(
    output_file=Path("/home/jpostel1/proj/watt-time/src/refrigerator_plot.png"),
    events=sim.events,
    power_in_kw=0.2,
    temp_delta_on=-10 / 12,
    temp_delta_off=5 / 12,
    temp_max=43,
    temp_min=33,
    starting_temp=33,
)
