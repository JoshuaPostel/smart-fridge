from reader import read_time_series, parse_line, Observation
from datetime import datetime

import pytest

file_head = """timestamp,MOER
2019-02-28 00:00:00+00:00,466
2019-02-28 00:05:00+00:00,426
2019-02-28 00:10:00+00:00,423
2019-02-28 00:15:00+00:00,442"""


@pytest.fixture
def data_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp("data")
    (path / "MOERS.csv").write_text(file_head)
    return path


class TestParseLine:
    def test_successfully_parses_expected_formatt(self):
        expected = Observation(datetime(2019, 2, 28, 0, 0), 466)
        result = parse_line("2019-02-28 00:00:00+00:00,466\n")
        assert expected == result


class TestReadTimeSeries:
    def test_first_five_lines_of_provided_data(self, data_dir):
        expected = [
            Observation(datetime(2019, 2, 28, 0, 0), 466),
            Observation(datetime(2019, 2, 28, 0, 5), 426),
            Observation(datetime(2019, 2, 28, 0, 10), 423),
            Observation(datetime(2019, 2, 28, 0, 15), 442),
        ]
        result = read_time_series(data_dir / "MOERS.csv")
        assert expected == result
