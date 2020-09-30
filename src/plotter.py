from utils import temprature_delta, attributed_pounds_co2

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def _get_tempratures(events, starting_temp, temp_delta_on, temp_delta_off):
    tempratures = [starting_temp]
    for event in events:
        temp_delta = temprature_delta(
            event.proportion_on, temp_delta_on, temp_delta_off
        )
        tempratures.append(tempratures[-1] + temp_delta)
    return tempratures[:-1]


def _get_cumulative_pounds_co2(moers, proportions_on, power_in_kw):
    cumulative_co2 = [0]
    for proportion_on, moer in zip(proportions_on, moers):
        co2 = attributed_pounds_co2(proportion_on, moer, power_in_kw / 12)
        cumulative_co2.append(cumulative_co2[-1] + co2)
    return cumulative_co2[:-1]


# not a big fan of multi-y-axis plots
# modified version of: https://stackoverflow.com/a/45925049/6876077
def plot_refrigerator(
    output_file,
    events,
    power_in_kw,
    temp_delta_on,
    temp_delta_off,
    temp_max,
    temp_min,
    starting_temp,
):

    times, moers, proportions_on = zip(*events)
    tempratures = _get_tempratures(events, starting_temp, temp_delta_on, temp_delta_off)
    cumulative_co2_pounds = _get_cumulative_pounds_co2(
        moers, proportions_on, power_in_kw
    )

    fig = plt.figure(figsize=(20, 10))
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    host.set_xlim(min(times), max(times))
    host.set_ylim(temp_min * 0.95, temp_max * 1.05)
    par1.set_ylim(-max(moers) * 0.05, max(moers) * 1.05)
    par2.set_ylim(-max(cumulative_co2_pounds) * 0.05, max(cumulative_co2_pounds) * 1.05)
    par3.set_ylim(0, 50)

    host.set_xlabel("Date")
    host.set_ylabel("Temperature F°")
    par1.set_ylabel("MOER")
    par2.set_ylabel("Cumulative CO2 lbs")
    par3.set_ylabel("Plug Off/On")

    color1 = plt.cm.viridis(0)
    color2 = plt.cm.viridis(0.5)
    color3 = plt.cm.viridis(0.8)
    color4 = plt.cm.viridis(0.2)

    p1, = host.plot(times, tempratures, color=color1, label="MOER")
    p2, = par1.plot(times, moers, color=color2, label="Temperature F°")
    p3, = par2.plot(
        times, cumulative_co2_pounds, color=color3, label="Cumulative CO2 lbs"
    )
    p4, = par3.plot(times, proportions_on, color=color4, label="Plug Off/On")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

    par2.spines["right"].set_position(("outward", 60))
    par3.spines["right"].set_position(("outward", 120))
    par3.yaxis.set_ticks([0, 1])

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())

    plt.savefig(output_file, bbox_inches="tight")
