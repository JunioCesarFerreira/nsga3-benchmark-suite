import numpy as np
from algorithms.protocol_nsga3 import ObjVec

def gd(approx_front: list[ObjVec], true_front: np.ndarray) -> float:
    """
    Generational Distance (GD).
    
    Mede a proximidade média dos pontos da fronteira aproximada (A)
    em relação à fronteira de Pareto verdadeira (P*).
    
    GD(A, P*) = (1/|A|) * sum_{a in A} min_{z in P*} ||a - z||
    
    :param approx_front: np.ndarray, shape (N, M) = fronteira aproximada
    :param true_front: np.ndarray, shape (K, M) = fronteira de Pareto verdadeira
    :return: float, valor do GD
    """
    approx_front = np.asarray(approx_front, dtype=float)

    if approx_front.ndim != 2 or true_front.ndim != 2:
        raise ValueError("As entradas devem ser matrizes 2D (N x M e K x M).")

    distances = []
    for a in approx_front:
        d = np.min(np.linalg.norm(true_front - a, axis=1))
        distances.append(d)

    return float(np.mean(distances))

def igd(approx_front: list[ObjVec], true_front: np.ndarray) -> float:
    """
    Calcula o IGD (Inverted Generational Distance).

    :param approx_front: np.ndarray de shape (N, M), fronteira aproximada
    :param true_front: np.ndarray de shape (K, M), fronteira de Pareto de referência
    :return: valor do IGD
    """
    approx_front = np.asarray(approx_front, dtype=float)

    if approx_front.size == 0 or true_front.size == 0:
        raise ValueError("As fronteiras não podem ser vazias")

    distances = []
    for y in true_front:
        d = np.linalg.norm(approx_front - y, axis=1)
        distances.append(np.min(d))

    return float(np.mean(distances))
