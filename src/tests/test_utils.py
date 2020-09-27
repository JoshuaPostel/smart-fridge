from utils import temprature_delta, attributed_kg_co2

import pytest


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


class TestAttributedCO2:
    def test_500_moer_and_200_watts_for_five_minutes(self):
        co2 = attributed_kg_co2(proportion_on=1, moer=500, kwh=0.2 / 12)
        assert co2 == pytest.approx(8.333, 0.001)
