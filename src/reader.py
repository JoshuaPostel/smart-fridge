from collections import namedtuple
from datetime import datetime
import logging

Datum = namedtuple("Datum", ["time", "moer"])


def parse_line(line):
    timestamp, moer, *rest = line.strip().split(",")
    date = datetime.strptime(timestamp.split("+")[0], "%Y-%m-%d %H:%M:%S")
    return Datum(date, int(moer))


def read_data_file(path):
    data = []
    with open(path, "r") as file:
        for line in file:
            try:
                datum = parse_line(line)
                data.append(datum)
            except (IndexError, ValueError):
                logging.warning(f"{path}: could not parse line: {line}")
    return data
