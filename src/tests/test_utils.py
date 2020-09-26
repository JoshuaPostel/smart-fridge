from utils import temprature_delta


class TestTempratureDelta:
    def test_on_for_full_hour(self):
        five_minute_delta = temprature_delta(
            proportion_on=1, temp_delta_on=-10 / 12, temp_delta_off=5 / 12
        )
        hour_delta = five_minute_delta * 12
        assert hour_delta == -10

    def test_off_for_full_hour(self):
        five_minute_delta = temprature_delta(
            proportion_on=0, temp_delta_on=-10 / 12, temp_delta_off=5 / 12
        )
        hour_delta = five_minute_delta * 12
        assert hour_delta == 5

    def test_on_for_half_hour(self):
        five_minute_delta = temprature_delta(
            proportion_on=0.5, temp_delta_on=-10 / 12, temp_delta_off=5 / 12
        )
        hour_delta = five_minute_delta * 12
        assert hour_delta == -2.5
