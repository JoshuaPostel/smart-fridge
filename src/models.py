from utils import temprature_delta
from logger import logger

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
        optimization_timesteps,
    ):

        self.horizon = initial_horizon
        self.temp_now = initial_temp
        self.temp_delta_on = temp_delta_on
        self.temp_delta_off = temp_delta_off
        self.temp_min = temp_min
        self.temp_max = temp_max

        self.moer_history_sum = sum(initial_horizon)
        self.moer_history_length = len(initial_horizon)

        self.optimization_timesteps = optimization_timesteps
        self.A = self.get_constraint_A(n=self.optimization_timesteps)

    def action(self, time):
        is_on = self.decide_action(time)
        self.temp_now += self.temp_delta(is_on)
        return is_on

    def decide_action(self, time):

        if self.temp_now + self.temp_delta(is_on=1) < self.temp_min:
            return 0

        elif self.temp_now + self.temp_delta(is_on=0) > self.temp_max:
            return 1

        elif self.horizon[0] == 0:
            return 1

        else:
            b = self.get_constraint_b(self.optimization_timesteps)
            c = self.get_cost(self.optimization_timesteps)
            result = linprog(c, self.A, b, bounds=[(0, 1)], options={"maxiter": 50})
            logger.info(
                f"at {time} temp: {self.temp_now} model's action: {result.x[0]}"
            )
            # handle numerical errors by bounding
            is_on = round(max(0, min(1, result.x[0])))
            return is_on

    def temp_delta(self, is_on):
        return temprature_delta(is_on, self.temp_delta_on, self.temp_delta_off)

    def update_horizon(self, time, moer):
        self.horizon = self.horizon[1:]
        self.horizon.append(moer)
        self.moer_history_sum += moer
        self.moer_history_length += 1

    def get_cost(self, n):
        extension_length = n - len(self.horizon)
        moer_average = self.moer_history_sum / self.moer_history_length
        extended_horizon = self.horizon[:n] + [moer_average] * extension_length
        return np.array(extended_horizon)

    def get_constraint_b(self, n):
        # max temperature constraint
        b_max_temp = [
            self.temp_max - self.temp_now - self.temp_delta_off * x
            for x in range(1, n + 1)
        ]
        b_min_temp = [
            self.temp_min - self.temp_now - self.temp_delta_off * x
            for x in range(1, n + 1)
        ]
        # multiply by -1 so that min temprature constraint is expressed as Ax <= b
        b_min_temp = -1 * np.array(b_min_temp)
        # combine the constraints
        b = np.concatenate((b_max_temp, b_min_temp))

        return b

    def get_constraint_A(self, n):
        A_max_temp = np.tril(np.full((n, n), self.temp_delta_on - self.temp_delta_off))
        # multiply by -1 so that min temprature constraint is expressed as Ax <= b
        A_min_temp = -1 * A_max_temp
        # combine the constraints
        A = np.vstack((A_max_temp, A_min_temp))
        return A
