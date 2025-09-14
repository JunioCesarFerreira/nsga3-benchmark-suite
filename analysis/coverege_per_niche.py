import numpy as np

def count_points_per_niche_dtlz2(
    pareto_front: np.ndarray,
    ref_points: np.ndarray,
    r: float
) -> tuple[np.ndarray, int]:
    """
    Conta quantos pontos da fronteira estão a menos que r de cada ponto de referência
    projetado na fronteira do DTLZ2. Também retorna quantos pontos ficaram fora de todos.

    :param pareto_front: np.ndarray de shape (N, M), pontos da fronteira aproximada
    :param ref_points: np.ndarray de shape (K, M), pontos de referência
    :param r: raio de associação
    :return: (counts, n_fora)
             counts -> array de shape (K,), com número de pontos associados a cada ref
             n_out -> número de pontos que não caíram em nenhum nicho
    """
    pareto_front = np.asarray(pareto_front, dtype=float)

    # Projetar ref_points na hiperesfera (DTLZ2)
    proj_refs = ref_points / np.linalg.norm(ref_points, axis=1, keepdims=True)

    counts = np.zeros(len(proj_refs), dtype=int)
    n_out = 0

    for p in pareto_front:
        # Distâncias até todos os pontos de referência
        dist = np.linalg.norm(proj_refs - p, axis=1)
        min_idx = np.argmin(dist)
        if dist[min_idx] <= r:
            counts[min_idx] += 1
        else:
            n_out += 1

    return counts, n_out


def analyze_niche_distribution(counts: np.ndarray, n_fora: int) -> dict[str, float]:
    """
    Calcula métricas de cobertura e densidade a partir da distribuição de pontos por nicho.

    :param counts: np.ndarray (K,), número de pontos em cada nicho
    :param n_fora: número de pontos fora de todos os nichos
    :return: dicionário com métricas
    """
    counts = np.asarray(counts, dtype=float)
    K = len(counts)
    N = counts.sum() + n_fora  # total de pontos
    active = counts[counts > 0]

    # --- Cobertura ---
    coverage = (active.size / K) if K > 0 else 0.0
    empty_ratio = ((K - active.size) / K) if K > 0 else 0.0
    outside_rate = n_fora / N if N > 0 else 0.0

    # --- Uniformidade ---
    if counts.sum() > 0:
        p = counts / counts.sum()
        ent = -np.sum([pi * np.log(pi) for pi in p if pi > 0])
        ent_norm = ent / np.log(K) if K > 1 else 0.0
        gini = np.sum(np.abs(p[:, None] - p[None, :])) / (2 * K * p.mean())
        expected = counts.sum() / K
        chi2 = np.sum((counts - expected) ** 2 / expected) if expected > 0 else 0.0
    else:
        ent_norm, gini, chi2 = 0.0, 0.0, 0.0

    # --- Densidade ---
    avg_active = active.mean() if active.size > 0 else 0.0
    max_density = counts.max() if K > 0 else 0.0
    std_density = counts.std() if K > 0 else 0.0

    # --- Score composto opcional ---
    cus = coverage * (1 - gini) * (1 - outside_rate)

    return {
        "coverage": coverage,
        "empty_ratio": empty_ratio,
        "outside_rate": outside_rate,
        "entropy_norm": ent_norm,
        "gini": gini,
        "chi2": chi2,
        "avg_active": avg_active,
        "max_density": max_density,
        "std_density": std_density,
        "CUS": cus
    }
