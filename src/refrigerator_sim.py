from models import NaiveModel
from simulator import Simulator
from plotter import plot_refrigerator

from datetime import datetime, timedelta
from pathlib import Path


sim = Simulator(
    model=NaiveModel(),
    input_file=Path("/home/jpostel1/proj/watt-time/data/MOERS.csv"),
    start_date=datetime(2019, 3, 1),
    end_date=datetime(2019, 4, 1),
    horizon=timedelta(hours=1),
    time_delta=timedelta(minutes=5),
)

sim.run()
print(sim.events[:10])

# TODO implement configs to avoid the amount of parameter passing
plot_refrigerator(
    output_file=Path("/home/jpostel1/proj/watt-time/src/refrigerator_plot.png"),
    events=sim.events,
    power_in_kw=0.2,
    temp_delta_on=-10 / 12,
    temp_delta_off=5 / 12,
    temp_max=44,
    temp_min=33,
    starting_temp=33,
)
