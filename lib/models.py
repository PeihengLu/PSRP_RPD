import numpy as np
from typing import List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join as pjoin

from scipy.optimize import minimize
from scipy.stats import truncnorm, norm
from lib.calculation import moving_window_mean

class RW:
    def __init__(self, v0=0, v1=0, beta=5, kappa=0.1, b=0, alpha=0.2, gamma=0.1) -> None:
        # initialize the record arrays
        self.choices = np.array([])
        self.rewards = np.array([])

        # initialize the model parameters
        self.v0 = v0
        self.v1 = v1
        self.beta = beta
        self.kappa = kappa
        self.b = b # initialize with no bias
        self.alpha = alpha
        self.gamma = gamma


    def update(self, outcome: int, choice: int) -> None:
        if choice == 0:
            self.v0 = self.alpha * (outcome - self.v0) + self.gamma * self.v0
            self.v1 = self.gamma * self.v1
        else:
            self.v1 = self.alpha * (outcome - self.v1) + self.gamma * self.v1
            self.v0 = self.gamma * self.v0


    def get_choice(self) -> tuple[int, float]:
        if self.choices.size == 0:
            # if this is the first trial, choose without kappa term
            p_r = 1 / (1 + np.exp(-self.beta * (self.v1 - self.v0 + self.b)))
        else:
            pre_choice = self.choices[-1]
            if pre_choice == 0:
                pre_choice = -1
            p_r = 1 / (1 + np.exp(-self.beta * (self.v1 - self.v0) + self.b + self.kappa * pre_choice)) 
        choice = np.random.binomial(1, p_r)
        self.choices = np.append(self.choices, choice)

        return (0, 1 - p_r) if choice == 0 else (1, p_r)


    def nll(self, parameters, choices_real: np.ndarray, rewards_real: np.ndarray) -> float:
        self.assign_parameters(parameters)
        self.choices = np.array([])
        neg_log_likelihood = 0
        self.v0, self.v1 = 0, 0

        for i in range(choices_real.size):
            choice = choices_real[i]
            c, prob = self.get_choice()
            self.choices[-1] = choice

            if prob == 0:
                prob += 0.0001
            elif prob == 1:
                prob -= 0.0001

            if c == choice:
                neg_log_likelihood += - np.log(prob)
            else:
                neg_log_likelihood += - np.log(1 - prob)

            reward = rewards_real[i]

            self.update(reward, choice)
            
        return neg_log_likelihood
    
    def fit(self, choices_real: np.ndarray, rewards_real: np.ndarray) -> Tuple[List[float], float]:
        # fit the model to the data return the best parameters and 
        # the corresponding negative log likelihood
        # parameters: beta, kappa, b
        # RW_Simple simulation
        fitted_parameters = None
        nll_min = np.inf

        for i in range(10):
            x0 = self.sample_parameters()
            bounds = [(0.00001, np.inf), (-np.inf, np.inf), (-np.inf, np.inf), (0.00001, 1), (0.00001, 1)]

            params = minimize(self.nll, x0=x0, args=(choices_real, rewards_real), method='Nelder-Mead', bounds=bounds)['x']
            if self.nll(params, choices_real, rewards_real) < nll_min:
                fitted_parameters = params
                nll_min = self.nll(params, choices_real, rewards_real)

        return fitted_parameters, nll_min

    # parameters: beta, kappa, b
    def assign_parameters(self, parameters):
        self.beta = parameters[0]
        self.kappa = parameters[1]
        self.b = parameters[2]
        self.alpha = parameters[3]
        self.gamma = parameters[4]

    def sample_parameters(self):
        beta = np.random.uniform(1, 10)
        kappa = np.random.uniform(-1, 1)
        b = np.random.uniform(-1, 1)
        alpha = np.random.uniform(0, 1)
        gamma = np.random.uniform(0, 1)
        return [beta, kappa, b, alpha,gamma]
    
    # v_r - v_l
    def get_delta_V(self, parameters, choices_real: np.ndarray, rewards_real: np.ndarray, session='session') -> np.ndarray:
        self.assign_parameters(parameters)
        simulated_choices = np.array([])
        self.choices = np.array([])
        delta_V = np.array([])
        neg_log_likelihood = 0
        self.v0, self.v1 = 0, 0
        delta_V = np.append(delta_V, self.v1 - self.v0)

        for i in range(choices_real.size):
            choice = choices_real[i]
            c, prob = self.get_choice()
            simulated_choices = np.append(simulated_choices, c)
            self.choices[-1] = choice
            reward = rewards_real[i]
            self.update(reward, choice)
            delta_V = np.append(delta_V, self.v1 - self.v0)
        
        # smoothen the choices
        simulated_choices = moving_window_mean(simulated_choices, 10)
        choices_real = np.convolve(choices_real, np.ones((10,))/10, mode='same')
        # plot simulated choices and real choices, and delta_V
        plt.plot(simulated_choices, label='simulated')
        plt.plot(choices_real, label='real')
        plt.legend()

        # save the plot in data/relative values
        plt.savefig(pjoin('data', 'relative_values', f'{session}.png'))
        plt.close()

        return delta_V

    # simulate according to a session of real behaviour
    def simulate(self, parameters, choices_real: np.ndarray, rewards_real: np.ndarray) -> float:
        self.assign_parameters(parameters)
        self.choices = np.array([])
        
        neg_log_likelihood = 0
        self.v0, self.v1 = 0, 0

        for i in range(choices_real.size):
            choice = choices_real[i]
            c, prob = self.get_choice()
            self.choices[-1] = choice
