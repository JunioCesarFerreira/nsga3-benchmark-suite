import json
import time
from pathlib import Path
import numpy as np

from algorithms.protocol_nsga3 import Bounds, NSGA3Callable
from genetic_operators.crossover import sbx_crossover
from genetic_operators.mutation import polynomial_mutation
from problems.dtlz2 import dtlz2
from analysis.coverege_per_niche import count_points_per_niche_dtlz2, analyze_niche_distribution
from analysis.hypervolume import hypervolume
from utils.generate_points import generate_reference_points

def run_experiemnt_with_dtlz2(
    pop_size: int,
    num_gen: int,
    bounds: Bounds,
    num_obj: int,
    divisions: int,
    radius_ref: float,
    implementations: list[NSGA3Callable],
    num_loops: int,
    output_dir: Path
    )->None:
    
    # Pontos de referência précalculados para uso nas comparações   
    ref_pts = generate_reference_points(num_obj, divisions)
    
    stats = {
        func.__name__: {
            "elapsed_time": [], 
            "hv_elapsed_time": [], 
            "count_elapsed_time": [], 
            "analyze_elapsed_time": [], 
            "hypervolume": [],
            "coverage": [],
            "empty_ratio": [],
            "outside_rate": [],
            "entropy_norm": [],
            "gini": [],
            "chi2": [],
            "avg_active": [],
            "max_density": [],
            "std_density": [],
            "CUS": []
            } for func in implementations}

    for exp_index in range(num_loops):
        # Loop de execuções das implementações
        for func in implementations:
            print(f"[{func.__name__}] running")
            
            start_time = time.time() # START TIME
            pareto_front = func(
                pop_size,
                num_gen,
                bounds,
                lambda x : dtlz2(x, M=num_obj),
                sbx_crossover,
                polynomial_mutation,
                divisions=divisions
            )
            elapsed_time = time.time() - start_time # ELAPSED
            
            start_time = time.time() # START TIME
            delta = 0.1
            worst_pt = np.max(pareto_front, axis=0) + delta
            hv = hypervolume(pareto_front, worst_pt.tolist())
            hv_elapsed_time = time.time() - start_time # ELAPSED
            
            start_time = time.time() # START TIME            
            ptin, ptout = count_points_per_niche_dtlz2(pareto_front, ref_pts, radius_ref)            
            counter_elapsed_time = time.time() - start_time # ELAPSED
            
            start_time = time.time() # START TIME     
            niche_metrics = analyze_niche_distribution(ptin, ptout)   
            analyze_elapsed_time = time.time() - start_time # ELAPSED
            
            print_data = {
                "implementation": func.__name__,
                "elapsed_time": elapsed_time,
                "hv_elapsed_time": hv_elapsed_time,
                "count_elapsed_time": counter_elapsed_time,
                "analyze_elapsed_time": analyze_elapsed_time,
                "worst_point": worst_pt.tolist(),
                "delta": delta,
                "hypervolume": hv,
                "points_out_r": ptout,
                "niche_metrics": niche_metrics,
            }
            print(json.dumps(print_data, indent=2))
                
            # Acumula métricas
            stats[func.__name__]["elapsed_time"].append(elapsed_time)
            stats[func.__name__]["hv_elapsed_time"].append(hv_elapsed_time)
            stats[func.__name__]["count_elapsed_time"].append(counter_elapsed_time)
            stats[func.__name__]["analyze_elapsed_time"].append(analyze_elapsed_time)
            stats[func.__name__]["hypervolume"].append(hv)
            
            for key, value in niche_metrics.items():
                stats[func.__name__][key].append(value)
            
            data = {
                "implementation": func.__name__,
                "elapsed_time": elapsed_time,
                "hv_elapsed_time": hv_elapsed_time,
                "count_elapsed_time": counter_elapsed_time,
                "analyze_elapsed_time": analyze_elapsed_time,
                "worst_point": worst_pt.tolist(),
                "delta": delta,
                "hypervolume": hv,
                "points_per_niche": [float(v) for v in ptin],
                "points_out_r": ptout,
                "niche_metrics": niche_metrics,
                "pareto_front": [list(map(float, sol)) for sol in pareto_front],
            }

            file_path = output_dir / f"run_{exp_index:03d}_{func.__name__}.json"

            # Salvar JSON
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

            print(f"[{func.__name__}] Saved {file_path} (time={elapsed_time:.3f}s)")

    # --- Cálculo das médias finais ---
    summary = {
        "parameters": {
            "pop_size": pop_size,
            "num_gen": num_gen,
            "bounds": bounds,
            "num_obj": num_obj,
            "divisions": divisions,
            "radius_ref": radius_ref,
            "num_loops": num_loops,
        },
        "results": {}
    }
    for func in implementations:
        name = func.__name__
        summary["results"][name] = {
            "mean_elapsed_time": float(np.mean(stats[name]["elapsed_time"])),
            "mean_hv_elapsed_time": float(np.mean(stats[name]["hv_elapsed_time"])),
            "mean_count_elapsed_time": float(np.mean(stats[name]["count_elapsed_time"])),
            "mean_analyze_elapsed_time": float(np.mean(stats[name]["analyze_elapsed_time"])),
            "mean_hypervolume": float(np.mean(stats[name]["hypervolume"])),
            "coverage": float(np.mean(stats[name]["coverage"])),
            "empty_ratio": float(np.mean(stats[name]["empty_ratio"])),
            "outside_rate": float(np.mean(stats[name]["outside_rate"])),
            "entropy_norm": float(np.mean(stats[name]["entropy_norm"])),
            "gini": float(np.mean(stats[name]["gini"])),
            "chi2": float(np.mean(stats[name]["chi2"])),
            "avg_active": float(np.mean(stats[name]["avg_active"])),
            "max_density": float(np.mean(stats[name]["max_density"])),
            "std_density": float(np.mean(stats[name]["std_density"])),
            "CUS": float(np.mean(stats[name]["CUS"])),
        }

    print("\n=== Summary of Results ===")
    for name, values in summary["results"].items():
        print(f"\nImplementation: {name}")
        for k, v in values.items():
            print(f"  {k}: {v:.6f}")

    # Salvar resumo em JSON
    summary_file = output_dir / "summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary saved to {summary_file}")