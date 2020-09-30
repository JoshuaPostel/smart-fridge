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

    def update_forecast(self, time, moer):
        pass


class LinearProgramming:
    """Determines optimal fridge operating schedule via a Linear Programming approach.

    Intended to interface with the Simulator class.

    Converts a fridge's operating constraints into the form Ax <= b and adjusts the fridge's state
    to minimize foercasted CO2 use: c^T * x. Solutions are found using a Linear Programming model.
    """

    def __init__(
        self,
        initial_forecast,
        initial_temp,
        delta_on,
        delta_off,
        temp_min,
        temp_max,
        optimization_horizon_timesteps,
    ):

        self.forecast = initial_forecast
        self.temp_now = initial_temp
        self.delta_on = delta_on
        self.delta_off = delta_off
        self.temp_min = temp_min
        self.temp_max = temp_max

        self.moer_history_sum = sum(initial_forecast)
        self.moer_history_count = len(initial_forecast)

        self.optimization_horizon_timesteps = optimization_horizon_timesteps
        self.A = self.get_constraint_A(self.optimization_horizon_timesteps)

    def action(self, time):
        """Called by the simulator to get the model's action (fridge on/off) at the next timestep"""
        is_on = self.model_decision(time)
        self.temp_now += self.temp_delta(is_on)
        return is_on

    def model_decision(self, time):
        """Minimize c^T * x with constraints Ax <= b and return optimal frige state based on x[0]"""
        # linear programming model finds a continuous solution which may violate constraints in the
        # discontinuous setting. These rules override the model at the min/max temprature boundries
        if self.temp_now + self.temp_delta(is_on=1) < self.temp_min:
            return 0

        elif self.temp_now + self.temp_delta(is_on=0) > self.temp_max:
            return 1

        # if the next moer = 0, turn the fridge on
        elif self.forecast[0] == 0:
            return 1

        else:
            b = self.get_constraint_b(self.optimization_horizon_timesteps)
            c = self.get_coefficients(self.optimization_horizon_timesteps)
            result = linprog(c, self.A, b, bounds=[(0, 1)], options={"maxiter": 50})
            logger.info(
                f"at: {time} temp: {self.temp_now} model's action: {result.x[0]}"
            )
            # handle numerical errors by bounding
            is_on = round(max(0, min(1, result.x[0])))
            return is_on

    def temp_delta(self, is_on):
        """Given the fridge state, returns the change in temprature for one timestep"""
        return temprature_delta(is_on, self.delta_on, self.delta_off)

    def update_forecast(self, time, moer):
        """Simulator calls this method and provides the next forecasted moer value"""
        self.forecast = self.forecast[1:]
        self.forecast.append(moer)
        self.moer_history_sum += moer
        self.moer_history_count += 1

    def get_coefficients(self, n):
        """Returns the (n by 1) coefficent vector c of the objective funtion c^T * x which are the
        moer values at time t, ..., t+n. If n > foercast length, average moer is concatenated
        """
        extension_length = n - len(self.forecast)
        moer_average = self.moer_history_sum / self.moer_history_count
        extended_forecast = self.forecast[:n] + [moer_average] * extension_length
        return np.array(extended_forecast)

    def get_constraint_b(self, n):
        """Calculates the (n by 1) vector b of Ax <= b given the constraints:
        1) temp_min <= fridge_temp(t) <= temp_max
        2) fridge_temp(t+1) = fridge_temp(t) + delta_off - (delta_on * fridge_on(t))
        3) fridge_temp(t=0)
        """
        b_max_temp = [
            self.temp_max - self.temp_now - self.delta_off * x for x in range(1, n + 1)
        ]
        b_min_temp = [
            self.temp_min - self.temp_now - self.delta_off * x for x in range(1, n + 1)
        ]
        # multiply by -1 so that minimum temprature constraint is expressed as Ax <= b
        b_min_temp = -1 * np.array(b_min_temp)
        b = np.concatenate((b_max_temp, b_min_temp))
        return b

    def get_constraint_A(self, n):
        """Calculates the (n by n) matrix A of Ax <= b givin the constraints:
        1) temp_min <= fridge_temp(t) <= temp_max
        2) fridge_temp(t+1) = fridge_temp(t) + delta_off - (delta_on * fridge_on(t))
        3) fridge_temp(t=0)
        """
        A_max_temp = np.tril(np.full((n, n), self.delta_on - self.delta_off))
        # multiply by -1 so that minimum temprature constraint is expressed as Ax <= b
        A_min_temp = -1 * A_max_temp
        A = np.vstack((A_max_temp, A_min_temp))
        return A
