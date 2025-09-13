import numpy as np

def count_points_around_refs_dtlz2(
    pareto_front: np.ndarray,
    ref_points: np.ndarray,
    r: float
) -> tuple[int, int]:
    """
    Conta quantos pontos da fronteira estão a menos que r dos pontos de referência projetados
    na fronteira do DTLZ2 e quantos estão fora.

    :param pareto_front: np.ndarray de shape (N, M), pontos da fronteira aproximada
    :param n_obj: número de objetivos (M)
    :param divisions: número de divisões para gerar pontos de referência
    :param r: raio das bolinhas
    :return: (n_dentro, n_fora)
    """
    pareto_front = np.asarray(pareto_front, dtype=float)

    # Projetar na fronteira da hiperesfera (DTLZ2)
    proj_refs = ref_points / np.linalg.norm(ref_points, axis=1, keepdims=True)

    # Para cada ponto da fronteira, calcular distância mínima até as refs
    n_dentro = 0
    for p in pareto_front:
        dist = np.linalg.norm(proj_refs - p, axis=1)
        if np.min(dist) <= r:
            n_dentro += 1

    n_fora = len(pareto_front) - n_dentro
    return n_dentro, n_fora
