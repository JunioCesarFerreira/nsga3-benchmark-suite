import numpy as np

def igd(approx_front: np.ndarray, true_front: np.ndarray) -> float:
    """
    Calcula o IGD (Inverted Generational Distance).

    :param approx_front: np.ndarray de shape (N, M), fronteira aproximada
    :param true_front: np.ndarray de shape (K, M), fronteira de Pareto de referência
    :return: valor do IGD
    """
    approx_front = np.asarray(approx_front, dtype=float)
    true_front = np.asarray(true_front, dtype=float)

    if approx_front.size == 0 or true_front.size == 0:
        raise ValueError("As fronteiras não podem ser vazias")

    distances = []
    for y in true_front:
        d = np.linalg.norm(approx_front - y, axis=1)
        distances.append(np.min(d))

    return float(np.mean(distances))
