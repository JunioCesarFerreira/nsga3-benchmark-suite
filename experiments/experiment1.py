import json
import time
from pathlib import Path
import numpy as np

from genetic_operators.crossover import sbx_crossover
from genetic_operators.mutation import polynomial_mutation
from algorithms.pure_nsga3 import nsga3_func
from problems.dtlz2 import dtlz2
from analysis.distance import count_points_around_refs_dtlz2
from analysis.hypervolume import hypervolume
from utils.generate_points import generate_reference_points

# Parameters
NUM_OBJ = 6
NUM_VAR = 14
NUM_GEN = 20
POP_SIZE = 60
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 

# Pasta de saída para resultados
output_dir = Path("results/experiment1")
output_dir.mkdir(parents=True, exist_ok=True)
 
# Pontos de referência précalculados para uso nas comparações   
ref_pts = generate_reference_points(NUM_OBJ, DIVISIONS)

# Loop de execuções
for i in range(100):
    start_time = time.time()

    pareto_front = nsga3_func(
        POP_SIZE,
        NUM_GEN,
        BOUNDS,
        lambda x : dtlz2(x, M=NUM_OBJ),
        sbx_crossover,
        polynomial_mutation,
        divisions=DIVISIONS
    )

    elapsed_time = time.time() - start_time
    
    ref_point = np.max(pareto_front, axis=0) + 0.1
    print(f'ref point={ref_point}')
    hv = hypervolume(pareto_front, ref_point.tolist())

    ptin, ptout = count_points_around_refs_dtlz2(pareto_front, ref_pts, R)

    print(f'elapsed_time: {elapsed_time}')
    print(f'hypervolume: {hv}')
    print(f'points_in_r: {ptin}')
    print(f'points_out_r: {ptout}')
    
    # Criar dicionário com resultados
    result = {
        "iteration": i,
        "elapsed_time": elapsed_time,
        "hypervolume": hv,
        "points_in_r": ptin,
        "points_out_r": ptout,
        "pareto_front": [list(map(float, sol)) for sol in pareto_front],
    }

    # Nome do arquivo (ex.: run_000.json)
    file_path = output_dir / f"run_{i:03d}.json"

    # Salvar JSON
    with open(file_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[{i}] Saved {file_path} (time={elapsed_time:.3f}s)")
