import random
import numpy as np
from algorithms.protocol_nsga3 import Vector, Bounds

def polynomial_mutation(
    individual: Vector, 
    bounds: Bounds,
    eta: float = 25.0,
    mutation_rate: float = 0.9,
    per_gene_prob: float | None = None
    ) -> Vector:
    """
    Polynomial mutation (Deb, 2001). Aplica por gene com prob ~ 1/n.
    Mantém a mesma probabilidade global de mutação do código original (_MUTATION_RATE).
    """
    n = individual.shape[0]
    
    if per_gene_prob is None:
        per_gene_prob = 1 / n

    if random.random() < mutation_rate:
        x = individual.copy()
        for i in range(n):
            if random.random() < per_gene_prob:
                lower, upper = bounds[i]
                if upper <= lower:  # proteção
                    continue
                x_i = x[i]
                # Normalizar para [0,1] dentro dos limites
                delta1 = (x_i - lower) / (upper - lower)
                delta2 = (upper - x_i) / (upper - lower)
                u = random.random()

                mut_pow = 1.0 / (eta + 1.0)
                if u < 0.5:
                    xy = 1.0 - delta1
                    xy = np.clip(xy, 0, 1)
                    val = 2.0 * u + (1.0 - 2.0 * u) * (xy ** (eta + 1.0))
                    delta_q = (val ** mut_pow) - 1.0
                else:
                    xy = 1.0 - delta2
                    xy = np.clip(xy, 0, 1)
                    val = 2.0 * (1.0 - u) + 2.0 * (u - 0.5) * (xy ** (eta + 1.0))
                    delta_q = 1.0 - (val ** mut_pow)

                x[i] = x_i + delta_q * (upper - lower)
                
                x[i] = np.clip(x[i], lower, upper)
        return x

    return individual
