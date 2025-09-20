from pathlib import Path

from .experiment_runner import run_experiemnt_with_dtlz2
from algorithms.protocol_nsga3 import NSGA3Callable
from algorithms.pure_nsga3 import nsga3_func
from algorithms.deap_nsga3 import nsga3_deap_func
from algorithms.pymoo_nsga3 import nsga3_pymoo_func

# Parameters
NUM_OBJ = 6
NUM_VAR = 12
NUM_GEN = 16
POP_SIZE = 10
DIVISIONS = 21
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
CXPB = 0.8
MUTPB = 0.2
INDMUTPB = 0.0833
ETA_C = 20
ETA_M = 20 

output_dir = Path("results/experiment8")
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
    output_dir=output_dir,
    pb_c=CXPB,
    pb_m=MUTPB,
    pb_pg_m=INDMUTPB,
    eta_c=ETA_C,
    eta_m=ETA_M
)
