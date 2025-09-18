import random
import numpy as np
from algorithms.protocol_nsga3 import Vector, Bounds

def sbx_crossover(
    parent1: Vector, 
    parent2: Vector, 
    bounds: Bounds,
    eta: float = 20.0,
    cxpb: float = 0.5,
    ) -> tuple[Vector, Vector]:
    """
    Simulated Binary Crossover
    SBX (Deb & Agrawal, 1995). Opera componente a componente.
    """
    n = parent1.shape[0]
    c1 = np.copy(parent1)
    c2 = np.copy(parent2)

    if random.random() < cxpb:           
        for i in range(n):
            x1 = parent1[i]
            x2 = parent2[i]

            u = random.random()
            
            if u <= 0.5:
                beta_q = (2 * u) ** (1 / (eta + 1))
            else:
                beta_q = (1 / (2 * (1 - u))) ** (1 / (eta + 1))

            c1[i] = 0.5 * ((x1 + x2) - beta_q * (x2 - x1))
            c2[i] = 0.5 * ((x1 + x2) + beta_q * (x2 - x1))
            
            c1[i] = min(max(c1[i], bounds[i][0]), bounds[i][1])
            c2[i] = min(max(c2[i], bounds[i][0]), bounds[i][1])

    return c1, c2
