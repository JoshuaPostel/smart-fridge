def temprature_delta(proportion_on, temp_delta_on, temp_delta_off):
    return temp_delta_off + ((temp_delta_on - temp_delta_off) * proportion_on)


def attributed_kg_co2(proportion_on, moer, kwh):
    return proportion_on * moer * kwh
