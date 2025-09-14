from pathlib import Path

from .experiment_runner import run_experiemnt_with_dtlz2
from algorithms.protocol_nsga3 import NSGA3Callable
from algorithms.pure_nsga3 import nsga3_func
from algorithms.deap_nsga3 import nsga3_deap_func
from algorithms.pymoo_nsga3 import nsga3_pymoo_func

# Parameters
NUM_OBJ = 6
NUM_VAR = 14
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 

output_dir = Path("results/experiment7")
output_dir.mkdir(parents=True, exist_ok=True)
 
impl: list[NSGA3Callable] = [
    nsga3_func,
    nsga3_deap_func,
    nsga3_pymoo_func
]

run_experiemnt_with_dtlz2(
    pop_size=POP_SIZE,
    num_gen=NUM_GEN,
    bounds=BOUNDS,
    num_obj=NUM_OBJ,
    divisions=DIVISIONS,
    radius_ref=R,
    implementations=impl,
    num_loops=100,
    output_dir=output_dir
)
