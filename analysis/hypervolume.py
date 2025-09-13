import numpy as np

def hypervolume(
    pareto_front: list[tuple[float, ...]] | np.ndarray,
    reference_point: list[float] | np.ndarray | None = None,
    delta: float = 0.1
) -> float:
    """
    Hipervolume (minimização em todos os objetivos).
    Corrigido para ordenar por f1 decrescente e evitar larguras negativas.

    :param pareto_front: lista/array (n_soluções x M)
    :param reference_point: ponto de referência (pior que todos os pontos). Se None, usa max + delta.
    :param delta: margem para referência automática
    """
    pf = np.array(pareto_front, dtype=float)
    if pf.ndim != 2:
        raise ValueError("pareto_front deve ser 2D (n_soluções x M).")

    # referência automática
    if reference_point is None:
        ref = np.max(pf, axis=0) + float(delta)
    else:
        ref = np.array(reference_point, dtype=float)

    if ref.shape[0] != pf.shape[1]:
        raise ValueError("Dimensão do reference_point deve ser igual ao número de objetivos.")
    if np.any(pf > ref):
        raise ValueError("reference_point deve ser >= a todos os pontos do Pareto em cada objetivo (minimização).")

    # remove duplicatas (opcional)
    pf = np.unique(pf, axis=0)

    # Ordena por f1 DECRESCENTE (minimização) para garantir widths positivos: width = prev - f1_i
    order = np.argsort(-pf[:, 0])
    pf = pf[order]

    def hv_2d(points: np.ndarray, ref2d: np.ndarray) -> float:
        # points: (k, 2) ordenado por f1 DECRESCENTE
        hv, prev_f1 = 0.0, ref2d[0]
        for f1, f2 in points:
            width = prev_f1 - f1
            if width < 0:
                # se acontecer, é bug de ordenação -> saneia para zero
                width = 0.0
            height = ref2d[1] - f2
            if height < 0:
                # ponto de referência inválido
                raise ValueError("reference_point[1] menor que um f2; HV negativo não faz sentido em minimização.")
            hv += width * height
            prev_f1 = f1
        return hv

    def recursive_hv(points: np.ndarray, ref_nd: np.ndarray) -> float:
        m = points.shape[1]
        if m == 2:
            return hv_2d(points, ref_nd)
        # Ordenado por f1 DECRESCENTE; fatiamos o “slab” entre prev e p[0]
        volume, prev_f1 = 0.0, ref_nd[0]
        for i, p in enumerate(points):
            width = prev_f1 - p[0]
            if width < 0:
                width = 0.0
            # Subconjunto relevante para este slab: pontos com f1 <= prev_f1,
            # o que corresponde a points[i:] pois estamos em ordem decrescente.
            slice_points = points[i:, 1:]
            volume += width * recursive_hv(slice_points, ref_nd[1:])
            prev_f1 = p[0]
        return volume

    return recursive_hv(pf, ref)
