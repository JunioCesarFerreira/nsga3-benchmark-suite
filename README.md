# NSGA-III Benchmark Suite

This repository provides a collection of Python implementations of the **NSGA-III algorithm** (Non-dominated Sorting Genetic Algorithm III).  
The main goal is to create a flexible and reproducible framework for **systematic experiments** and **exhaustive comparisons** of NSGA-III across different coding paradigms and libraries.

By using this benchmark suite, researchers and practitioners can:
- Compare **performance**, **efficiency**, and **solution quality** of different NSGA-III implementations.
- Run **reproducible experiments** on well-known test problems (e.g., DTLZ2).
- Generate results in multiple formats (**CSV**, **JSON**, and plots) for further analysis.
- Extend the suite with new algorithms, problems, or performance metrics.

---

## 📂 Directory Organization

- `algorithms/` → Implementations of NSGA-III (pure Python, DEAP, PyMoo, PyGMO, etc.).
- `analysis/` → Metrics and tools for performance evaluation (e.g., hypervolume, coverage, IGD).
- `experiments/` → Ready-to-run experiment scripts with configurable parameters.
- `genetic_operators/` → Crossover and mutation operators (e.g., SBX, polynomial mutation).
- `problems/` → Benchmark problems (e.g., DTLZ2).
- `utils/` → Helper utilities such as reference point generation.
- `results/` → JSON/CSV files and summaries from executed experiments.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have **Python 3.12+** installed.  
It is recommended to use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Linux/macOS
.venv\Scripts\activate      # On Windows
````

### Installation

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 📊 Results

We conducted a benchmark study comparing three implementations of the NSGA-III algorithm (`nsga3_func`, `nsga3_deap_func`, and `nsga3_pymoo_func`) across different problem sizes.
The experiments varied both the number of **objectives** (from 2 up to 6) and the number of **decision variables** (from 1 up to 14). 

For each configuration, we executed **100 independent runs** of 16 generations with a population size of 100.
Performance was measured in terms of **Hypervolume (HV)**, **Generational Distance (GD)**, **Inverted Generational Distance (IGD)**, coverage, entropy-based diversity indicators, and execution time.

A key observation is the **increasing computational cost of hypervolume calculation** as the number of objectives grows.
For problems with five or more objectives, the HV computation time dominated the overall runtime.
Part of this slowdown is attributable to the **current Python-based implementation of the HV calculation**, which introduces additional overhead compared to optimized low-level implementations.

These results provide an initial baseline for evaluating multi-objective optimization frameworks within our platform.
However, **further experiments are needed** to better understand the complexity relationships between the number of objectives, the number of decision variables, and the runtime behavior of different NSGA-III implementations.


| #Obj | #Var | Method            | Mean HV        | Mean GD     | Mean IGD    | Mean Time (s) | HV Time (s) | Coverage | Entropy Norm. |
|------|------|-------------------|----------------|-------------|-------------|---------------|-------------|-----------|----------------|
| 2    | 1    | nsga3_func        | 0.414          | 0.0027      | 0.0205      | 0.602         | 0.00029     | 1.000     | 0.914          |
|      |      | nsga3_deap_func   | 0.417          | 0.0015      | 0.0097      | 0.051         | 0.00025     | 1.000     | 0.935          |
|      |      | nsga3_pymoo_func  | 0.388          | 0.0128      | 0.0447      | 0.108         | 0.00017     | 1.000     | 1.000          |
| 3    | 2    | nsga3_func        | 2.499          | 0.0494      | 0.0784      | 0.642         | 0.00432     | 0.712     | 0.871          |
|      |      | nsga3_deap_func   | 1.925          | 0.0259      | 0.0785      | 0.078         | 0.00461     | 0.622     | 0.826          |
|      |      | nsga3_pymoo_func  | 1.934          | 0.0533      | 0.0902      | 0.138         | 0.00127     | 0.652     | 0.892          |
| 4    | 3    | nsga3_func        | 29.135         | 0.0884      | 0.2384      | 0.683         | 0.14921     | 0.280     | 0.762          |
|      |      | nsga3_deap_func   | 8.430          | 0.0810      | 0.2156      | 0.124         | 0.14936     | 0.199     | 0.673          |
|      |      | nsga3_pymoo_func  | 73.407         | 0.0924      | 0.1378      | 0.114         | 0.26167     | 0.364     | 0.815          |
| 4*   | 4    | nsga3_func        | 22.012         | 0.0816      | 0.2348      | 0.749         | 0.15374     | 0.245     | 0.732          |
|      |      | nsga3_deap_func   | 2.246          | 0.0946      | 0.2785      | 0.127         | 0.04222     | 0.109     | 0.582          |
|      |      | nsga3_pymoo_func  | 61.997         | 0.1101      | 0.1558      | 0.142         | 0.25549     | 0.332     | 0.797          |
| 5    | 4    | nsga3_func        | 112.484        | 0.1529      | 0.3495      | 0.820         | 3.83746     | 0.079     | 0.625          |
|      |      | nsga3_deap_func   | 35.066         | 0.1296      | 0.2552      | 0.324         | 3.41635     | 0.070     | 0.600          |
|      |      | nsga3_pymoo_func  | 434.260        | 0.1469      | 0.2220      | 0.137         | 14.27146    | 0.122     | 0.689          |
| 6    | 5    | nsga3_func        | 32.445         | 0.2093      | 0.5156      | 1.139         | 83.14360    | 0.027     | 0.543          |
|      |      | nsga3_deap_func   | 82.165         | 0.1918      | 0.3323      | 0.580         | 83.17883    | 0.020     | 0.483          |
|      |      | nsga3_pymoo_func  | 1978.796       | 0.1952      | 0.2688      | 0.241         | 490.26166   | 0.035     | 0.578          |
| 6*   | 14   | nsga3_func        | 19170.302      | 0.6745      | 0.7019      | 1.115         | 80.90625    | 0.000     | 0.000          |
|      |      | nsga3_deap_func   | 261.854        | 0.5995      | 0.5765      | 0.579         | 3.91010     | 0.0003    | 0.000          |
|      |      | nsga3_pymoo_func  | 30831.357      | 0.5217      | 0.4632      | 0.199         | 289.88638   | 0.0003    | 0.000          |

[If you want to see the full results of the experiments.](./results_2025_09_14/)

### 📈 Host Information

* **Operating System**: Ubuntu 24.04.2 LTS (Noble Numbat)  
* **Kernel**: 6.8.0 (generic)  
* **Virtualization**: KVM (AMD-V enabled)  

#### CPU
* **Vendor**: AuthenticAMD  
* **Model**: AMD EPYC-Milan Processor  
* **Architecture**: x86_64  
* **Cores/Threads**: 2 cores, 2 threads (1 thread per core, 2 sockets × 1 core each)  
* **Base Frequency**: ~3.8 GHz (reported)  
* **Caches**:  
  * L1d: 64 KiB (2 × 32 KiB)  
  * L1i: 64 KiB (2 × 32 KiB)  
  * L2: 1 MiB (2 × 512 KiB)  
  * L3: 64 MiB (2 × 32 MiB)  

#### Memory
* **Total RAM**: 3.4 GiB  
* **Used**: 741 MiB  
* **Available**: 2.6 GiB  
* **Swap**: 0 B


---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---