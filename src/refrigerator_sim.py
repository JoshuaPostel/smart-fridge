from models import LinearProgramming
from simulator import Simulator
from plotter import plot_refrigerator
from reader import read_time_series

from datetime import datetime, timedelta
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
data_file = repo_root / "data" / "MOERS.csv"
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

total_co2 = round(sim.total_co2(0.2 / 12), 3)
print(f"total associated CO2: {total_co2} lbs")

total_runtime = sim.total_runtime()
print(f"total fridge run time: {total_runtime}")

# TODO implement configs to avoid the amount of parameter passing
plot_refrigerator(
    output_file=repo_root / "output" / "refrigerator.png",
    events=sim.events,
    power_in_kw=0.2,
    temp_delta_on=-10 / 12,
    temp_delta_off=5 / 12,
    temp_max=43,
    temp_min=33,
    starting_temp=33,
)
