import numpy as np
from algorithms.protocol_nsga3 import Vector 

def dtlz2(x: Vector, M: int = 6) -> Vector:
    """
    DTLZ2 (minimização). x: (n,), n = M-1 + k, tipicamente k=10 -> n=15 p/ M=6.
    Retorna vetor de M objetivos.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    assert n >= M - 1, "DTLZ2: n deve ser >= M-1"

    k = n - (M - 1)
    g = np.sum((x[n - k:] - 0.5) ** 2)

    f = np.empty(M, dtype=float)
    # produto de cossenos para os primeiros M-1 termos, sen no termo específico
    for m in range(M):
        val = 1.0 + g
        # cos terms
        for i in range(M - m - 1):
            val *= np.cos(0.5 * np.pi * x[i])
        if m > 0:
            val *= np.sin(0.5 * np.pi * x[M - m - 1])
        f[m] = val
    return f  # todos minimização

def dtlz2_true_front(n_points: int, n_obj: int) -> np.ndarray:
    """
    Gera amostras da fronteira verdadeira do DTLZ2.
    Cada ponto está na hiperesfera unitária (norma 1, coordenadas >= 0).
    """
    X = np.random.randn(n_points, n_obj)
    X = np.abs(X)  # primeiro quadrante
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    return X
