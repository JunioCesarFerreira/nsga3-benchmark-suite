import numpy as np
from pymoo.indicators.gd import GD
from pymoo.indicators.igd import IGD
from deap.tools._hypervolume import hv

def gd(approx_front: np.ndarray, true_front: np.ndarray) -> float:
    ind = GD(pf=true_front)
    return ind(approx_front)
    
def igd(approx_front: np.ndarray, true_front: np.ndarray) -> float:
    ind = IGD(pf=true_front)
    return ind(approx_front)

def hypervolume(
    pareto_front: list[tuple[float, ...]] | np.ndarray,
    reference_point: list[float] | np.ndarray | None = None,
    delta: float = 0.1
) -> float:
    pf = np.array(pareto_front, dtype=float)
    if pf.ndim != 2:
        raise ValueError("pareto_front must be 2D (n_solutions x M).")

    # referência automática
    if reference_point is None:
        ref = np.max(pf, axis=0) + float(delta)
    else:
        ref = np.array(reference_point, dtype=float)

    if ref.shape[0] != pf.shape[1]:
        raise ValueError("Reference point size must be equal to the number of objectives.")
    if np.any(pf > ref):
        raise ValueError("reference_point must be >= all Pareto points in each objective (minimization).")
    
    return hv.hypervolume(pareto_front, reference_point)
