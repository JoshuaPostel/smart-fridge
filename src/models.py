from utils import temprature_delta

import numpy as np
from scipy.optimize import linprog


class Naive:
    def __init__(self):
        self.counter = 0

    def action(self, time):
        self.counter += 1
        if self.counter % 3 == 0:
            return 1
        else:
            return 0

    def update_horizon(self, time, moer):
        pass


class LinearProgramming:
    def __init__(
        self,
        initial_horizon,
        initial_temp,
        temp_delta_on,
        temp_delta_off,
        temp_min,
        temp_max,
    ):

        self.horizon = initial_horizon
        self.temp_now = initial_temp
        self.temp_delta_on = temp_delta_on
        self.temp_delta_off = temp_delta_off
        self.temp_min = temp_min
        self.temp_max = temp_max

    def action(self, time):
        A, b = self.get_constrains()
        c = self.get_cost()
        result = linprog(c, A, b, bounds=[(0, 1)])
        is_on = round(result.x[0])
        self.temp_now = self.temp_now + temprature_delta(
            is_on, self.temp_delta_on, self.temp_delta_off
        )
        # print(time, is_on, result.x[0])
        return is_on

    def update_horizon(self, time, moer):
        self.horizon = self.horizon[1:]
        self.horizon.append(moer)

    def get_cost(self):
        return np.array(self.horizon)

    # TODO A is the same throughout, no need to keep generating
    # TODO n is the same throughout, no need to recompute it
    def get_constrains(self):
        n = len(self.horizon)
        # Ax <= b constraint (max temp)
        A_less_than = np.tril(np.full((n, n), self.temp_delta_on - self.temp_delta_off))
        b_less_than = np.array(
            [self.temp_max - self.temp_now - self.temp_delta_off * x for x in range(n)]
        )

        # Ax >= b constraint (min temp)
        # multiply both sides by -1 so that it is formulated as Ax <= b
        A_greater_than = -1 * np.tril(
            np.full((n, n), self.temp_delta_on - self.temp_delta_off)
        )
        b_greater_than = -1 * np.array(
            [self.temp_min - self.temp_now - self.temp_delta_off * x for x in range(n)]
        )

        # combine the constraints
        A = np.vstack((A_less_than, A_greater_than))
        b = np.concatenate((b_less_than, b_greater_than))

        return A, b
