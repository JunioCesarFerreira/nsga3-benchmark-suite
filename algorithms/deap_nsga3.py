from deap import base, creator, tools, algorithms
import numpy as np
from typing import Callable
from .protocol_nsga3 import Vector, Bounds, ObjectiveVec

def nsga3_deap_func(
    pop_size: int,
    generations: int,
    bounds: Bounds,
    functions: Callable[[Vector], Vector],
    crossover: Callable[[Vector, Vector], tuple[Vector, Vector]],
    mutation: Callable[[Vector, Bounds], Vector],
    initial_pop: list[Vector] = None,
    divisions: int = 10,
    ref_points: Vector = None
) -> list[ObjectiveVec]:
    """
    Utiliza DEAP para resolver NSGA-III com os parâmetros especificados.
    Suporta tanto lista de funções escalares [f1, f2, ..., fM]
    quanto uma única função multiobjetivo f(x) -> Vector.
    """
    # Número de objetivos
    test_obj = functions(np.zeros(len(bounds)))
    if not isinstance(test_obj, Vector):
        raise ValueError("A função multiobjetivo deve retornar Vector")
    n_obj = test_obj.shape[0]

    # Criação dos tipos básicos para DEAP
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,) * n_obj)
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Inicializador de indivíduos
    toolbox.register(
        "individual",
        lambda: creator.Individual(
            [np.random.uniform(b[0], b[1]) for b in bounds]
        ),
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Avaliação personalizada
    def evaluate(individual):
        x = np.array(individual, dtype=float)
        obj_vec = functions(x)
        if not isinstance(obj_vec, Vector):
            raise ValueError("A função multiobjetivo deve retornar Vector")
        return tuple(float(v) for v in obj_vec)

    toolbox.register("evaluate", evaluate)

    # Geração dos pontos de referência para o NSGA-III
    if ref_points is None:
        ref_points = tools.uniform_reference_points(nobj=n_obj, p=divisions)
        
    # Crossover personalizado
    def custom_crossover(ind1, ind2):
        child1, child2 = crossover(np.array(ind1), np.array(ind2))
        return creator.Individual(child1.tolist()), creator.Individual(child2.tolist())

    toolbox.register("mate", custom_crossover)

    # Mutação personalizada
    def custom_mutation(individual):
        mutated = mutation(np.array(individual), bounds)
        individual[:] = mutated.tolist()
        return individual,

    toolbox.register("mutate", custom_mutation)

    # Operador de seleção
    toolbox.register("select", tools.selNSGA3)

    # Inicialização da população
    if initial_pop:
        population = [creator.Individual(ind.tolist()) for ind in initial_pop]
    else:
        population = toolbox.population(n=pop_size)
    
    # Avaliação inicial da população
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
        
    # Loop evolutivo
    for gen in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=1.0, mutpb=1.0)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population), ref_points=ref_points)
        
    front = tools.emo.sortNondominated(population, len(population), first_front_only=True)[0]

    # Retornar a frente de Pareto
    pareto_front = [tuple(ind.fitness.values) for ind in front]
            
    return pareto_front
