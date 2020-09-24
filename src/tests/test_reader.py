from reader import read_data_file, Datum
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


class TestReadDataFile:
    def test_first_five_lines_of_provided_data(self, data_dir):
        expected = [
            Datum(datetime(2019, 2, 28, 0, 0), 466),
            Datum(datetime(2019, 2, 28, 0, 5), 426),
            Datum(datetime(2019, 2, 28, 0, 10), 426),
            Datum(datetime(2019, 2, 28, 0, 25), 426),
        ]
        result = read_data_file(data_dir / "MOERS.csv")
        assert expected == result
