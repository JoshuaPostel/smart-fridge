from collections import namedtuple
from datetime import datetime
import logging.config

from logger import logging_config


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


Observation = namedtuple("Observation", ["time", "moer"])


def parse_line(line):
    timestamp, moer, *rest = line.strip().split(",")
    date = datetime.strptime(timestamp.split("+")[0], "%Y-%m-%d %H:%M:%S")
    return Observation(date, int(moer))


def read_time_series(path):
    time_series = []
    with open(path, "r") as file:
        for line in file:
            try:
                observation = parse_line(line)
                time_series.append(observation)
            except (IndexError, ValueError):
                logger.warning(f"{path}: could not parse line: {line}")
    return time_series
