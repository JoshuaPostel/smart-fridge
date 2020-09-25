from models import NaiveModel
from runner import Simulator

from pathlib import Path


sim = Simulator(
    NaiveModel(), Path("/home/jpostel1/proj/watt-time/data/MOERS.csv"), 0, 0, 0
)

sim.run()
print(sim.history[:50])
