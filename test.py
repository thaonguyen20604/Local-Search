import numpy as np
import math
from problem import Problem
from search import LocalSearchStrategy

problem_instance = Problem()
problem_instance.load_state_space('monalisa.jpg')

class test:
    hcs = LocalSearchStrategy.random_restart_hill_climbing(problem_instance, 3)
    problem_instance.draw_path(hcs)

    def schedule(t):
        return 100*math.exp(-t*0.1)

    sas = LocalSearchStrategy.simulated_annealing_search(problem_instance, schedule)
    problem_instance.draw_path(sas)

    lcs = LocalSearchStrategy.local_beam_search(problem_instance, 5)
    problem_instance.draw_path(lcs)