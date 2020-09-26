from utils import temprature_delta, attributed_co2

# import matplotlib.pyplot as plt


def plot_refrigerator(events, power_in_kw):
    times, moers, proportions_on = zip(*events)
    # TODO move to parameters
    tempratures = _get_tempratures(events, 33, -10 / 12, 5 / 12)
    cumulative_co2 = _get_cumulative_co2(moers, proportions_on, power_in_kw)
    print(times[:15])
    print(moers[:15])
    print(proportions_on[:15])
    print(tempratures[:15])
    print(cumulative_co2[:15])


def _get_tempratures(events, starting_temp, temp_delta_on, temp_delta_off):
    tempratures = [starting_temp]
    for event in events:
        temp_delta = temprature_delta(
            event.proportion_on, temp_delta_on, temp_delta_off
        )
        tempratures.append(tempratures[-1] + temp_delta)
    return tempratures


def _get_cumulative_co2(moers, proportions_on, power_in_kw):
    cumulative_co2 = [0]
    for proportion_on, moer in zip(proportions_on, moers):
        co2 = attributed_co2(proportion_on, moer, power_in_kw / 12)
        cumulative_co2.append(cumulative_co2[-1] + co2)
    return cumulative_co2
