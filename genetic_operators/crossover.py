import random
import numpy as np
from algorithms.protocol_nsga3 import Vector

def sbx_crossover(
    parent1: Vector, 
    parent2: Vector, 
    eta: float = 20.0,
    cxpb: float = 0.5
    ) -> tuple[Vector, Vector]:
    """
    SBX (Deb & Agrawal, 1995). Opera componente a componente.
    """
    n = parent1.shape[0]
    c1 = np.empty_like(parent1)
    c2 = np.empty_like(parent2)

    for i in range(n):
        x1 = parent1[i]
        x2 = parent2[i]

        if random.random() < cxpb and abs(x1 - x2) > 1e-14:
            if x1 > x2:
                x1, x2 = x2, x1  # garantir x1 <= x2

            u = random.random()
            beta = 1.0 + (2.0 * (x1 - 0.0) / (x2 - x1 + 1e-14))  # limites desconhecidos aqui; não usados
            # Fórmula padrão sem limites explícitos:
            if u <= 0.5:
                beta_q = (2.0 * u) ** (1.0 / (eta + 1.0))
            else:
                beta_q = (1.0 / (2.0 * (1.0 - u))) ** (1.0 / (eta + 1.0))

            c1[i] = 0.5 * ((x1 + x2) - beta_q * (x2 - x1))
            c2[i] = 0.5 * ((x1 + x2) + beta_q * (x2 - x1))
        else:
            # sem recombinação (ou genes idênticos): copiar
            c1[i] = x1
            c2[i] = x2

    return (c1, c2)
