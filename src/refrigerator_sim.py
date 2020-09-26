from models import NaiveModel
from runner import Simulator
from datetime import datetime, timedelta

from pathlib import Path


sim = Simulator(
    model=NaiveModel(),
    input_file=Path("/home/jpostel1/proj/watt-time/data/MOERS.csv"),
    start_date=datetime(2019, 3, 1),
    end_date=datetime(2019, 4, 1),
    horizon=timedelta(hours=1),
    time_delta=timedelta(minutes=5),
    power_in_watts=0,
)

sim.run()
print(sim.events[:10])
