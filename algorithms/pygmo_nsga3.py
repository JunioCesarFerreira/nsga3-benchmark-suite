import numpy as np
import pygmo as pg
from typing import Callable
from .protocol_nsga3 import Vector, Bounds, ObjVec


def nsga3_pygmo_func(
    pop_size: int,
    generations: int,
    bounds: Bounds,
    functions: Callable[[Vector], Vector],
    crossover: Callable[[Vector, Vector], tuple[Vector, Vector]],  # ignorado (PyGMO tem os seus)
    mutation: Callable[[Vector, Bounds], Vector],                  # idem
    initial_pop: list[Vector] | None = None,
    divisions: int = 10,   # não usado explicitamente (PyGMO gere internamente)
    ref_points: Vector | None = None
) -> list[ObjVec]:
    """
    Resolve NSGA-III usando PyGMO (pagmo).
    O crossover/mutação customizados não são usados aqui, 
    pois o PyGMO encapsula o algoritmo completo.

    :param pop_size: Tamanho da população
    :param generations: Número de gerações
    :param bounds: Limites [(min, max), ...]
    :param functions: Função multiobjetivo f(x) -> Vector
    :return: Fronteira de Pareto aproximada
    """

    # Número de variáveis e objetivos
    n_var = len(bounds)
    test_obj = functions(np.zeros(n_var))
    if not isinstance(test_obj, np.ndarray):
        raise ValueError("A função multiobjetivo deve retornar np.ndarray")
    n_obj = test_obj.shape[0]

    # Definição do problema no estilo PyGMO
    class PyGMOProblem:
        def fitness(self, x):
            return functions(np.array(x, dtype=float)).tolist()

        def get_bounds(self):
            xl = [b[0] for b in bounds]
            xu = [b[1] for b in bounds]
            return (xl, xu)

        def get_nobj(self):
            return n_obj

    prob = pg.problem(PyGMOProblem())

    # Algoritmo NSGA-III do PyGMO
    algo = pg.algorithm(pg.nsga3(gen=generations))

    # População inicial
    if initial_pop:
        pop = pg.population(prob)
        for ind in initial_pop:
            pop.push_back(ind.tolist())
    else:
        pop = pg.population(prob, size=pop_size)

    # Evolve
    pop = algo.evolve(pop)

    # Extrair fronteira de Pareto (não-dominados)
    nds = pop.get_non_dominated_front()
    pareto_front = [tuple(pop.get_f()[i]) for i in nds]

    return pareto_front
