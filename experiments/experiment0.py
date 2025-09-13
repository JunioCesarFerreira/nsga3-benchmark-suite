import json
import time
from pathlib import Path
import numpy as np

from algorithms.protocol_nsga3 import NSGA3Callable
from genetic_operators.crossover import sbx_crossover
from genetic_operators.mutation import polynomial_mutation
from algorithms.pure_nsga3 import nsga3_func
from algorithms.deap_nsga3 import nsga3_deap_func
from algorithms.pymoo_nsga3 import nsga3_pymoo_func
from problems.dtlz2 import dtlz2
from analysis.distance import count_points_around_refs_dtlz2
from analysis.hypervolume import hypervolume
from utils.generate_points import generate_reference_points

# Parameters
NUM_OBJ = 3
NUM_VAR = 2
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.1 # ~(pi/2)/DIVISIONS 

# Pasta de saída para resultados
output_dir = Path("results/experiment0")
output_dir.mkdir(parents=True, exist_ok=True)
 
# Pontos de referência précalculados para uso nas comparações   
ref_pts = generate_reference_points(NUM_OBJ, DIVISIONS)

impl: list[NSGA3Callable] = [
    nsga3_func,
    nsga3_deap_func,
    nsga3_pymoo_func
]

# Loop de execuções
for func in impl:
    print(f"[{func.__name__}] running")
    start_time = time.time()

    pareto_front = func(
        POP_SIZE,
        NUM_GEN,
        BOUNDS,
        lambda x : dtlz2(x, M=NUM_OBJ),
        sbx_crossover,
        polynomial_mutation,
        divisions=DIVISIONS
    )

    elapsed_time = time.time() - start_time
    
    hv = hypervolume(pareto_front, [1.1]*NUM_OBJ)

    ptin, ptout = count_points_around_refs_dtlz2(pareto_front, ref_pts, R)

    print(f'\telapsed_time: {elapsed_time}')
    print(f'\thypervolume: {hv}')
    print(f'\tpoints_in_r: {ptin}')
    print(f'\tpoints_out_r: {ptout}')
    
    # Criar dicionário com resultados
    result = {
        "implementation": func.__name__,
        "elapsed_time": elapsed_time,
        "hypervolume": hv,
        "points_in_r": ptin,
        "points_out_r": ptout,
        "pareto_front": [list(map(float, sol)) for sol in pareto_front],
    }

    file_path = output_dir / f"run_{func.__name__}.json"

    # Salvar JSON
    with open(file_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[{func.__name__}] Saved {file_path} (time={elapsed_time:.3f}s)")
