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
| 2    | 1    | nsga3_func        | 0.414    | 0.0029   | 0.0233   | 0.597          | 0.000096    | 1.000     | 0.914           |
|      |      | nsga3_deap_func   | 0.417    | 0.00157  | 0.00974  | 0.050          | 0.000069    | 1.000     | 0.935           |
|      |      | nsga3_pymoo_func  | 0.388    | 0.0135   | 0.0439   | 0.106          | 0.000031    | 1.000     | 1.000           |
| 3    | 2    | nsga3_func        | 0.796    | 0.0471   | 0.0771   | 0.650          | 0.000155    | 0.713     | 0.871           |
|      |      | nsga3_deap_func   | 0.690    | 0.0268   | 0.0808   | 0.078          | 0.000106    | 0.618     | 0.824           |
|      |      | nsga3_pymoo_func  | 0.781    | 0.0572   | 0.0934   | 0.140          | 0.000099    | 0.652     | 0.892           |
| 4    | 3    | nsga3_func        | 0.434    | 0.0814   | 0.231    | 0.679          | 0.000188    | 0.279     | 0.762           |
|      |      | nsga3_deap_func   | 0.533    | 0.0800   | 0.202    | 0.122          | 0.000159    | 0.200     | 0.674           |
|      |      | nsga3_pymoo_func  | 1.042    | 0.0934   | 0.141    | 0.113          | 0.000280    | 0.364     | 0.815           |
| 4*   | 4    | nsga3_func        | 0.514    | 0.0860   | 0.241    | 0.725          | 0.000218    | 0.245     | 0.731           |
|      |      | nsga3_deap_func   | 0.398    | 0.0885   | 0.270    | 0.129          | 0.000126    | 0.109     | 0.583           |
|      |      | nsga3_pymoo_func  | 1.159    | 0.1156   | 0.155    | 0.146          | 0.000281    | 0.332     | 0.797           |
| 5    | 4    | nsga3_func        | 0.280    | 0.144    | 0.342    | 0.820          | 0.000626    | 0.079     | 0.625           |
|      |      | nsga3_deap_func   | 0.530    | 0.138    | 0.264    | 0.336          | 0.000452    | 0.070     | 0.599           |
|      |      | nsga3_pymoo_func  | 0.840    | 0.1397   | 0.212    | 0.140          | 0.002499    | 0.122     | 0.689           |
| 6    | 5    | nsga3_func        | 0.0510   | 0.2286   | 0.524    | 1.149          | 0.002877    | 0.0267    | 0.544           |
|      |      | nsga3_deap_func   | 0.311    | 0.2378   | 0.336    | 0.592          | 0.001772    | 0.0200    | 0.483           |
|      |      | nsga3_pymoo_func  | 1.123    | 0.2028   | 0.270    | 0.255          | 0.033398    | 0.0346    | 0.578           |
| 6*   | 14   | nsga3_func        | 13.429   | 0.692    | 0.711    | 1.111          | 0.003091    | 0.000     | 0.000           |
|      |      | nsga3_deap_func   | 6.278    | 0.605    | 0.580    | 0.593          | 0.000476    | 0.00033   | 0.000           |
|      |      | nsga3_pymoo_func  | 14.235   | 0.516    | 0.453    | 0.208          | 0.027907    | 0.00033   | 0.000           |


[If you want to see the full results of the experiments.](./results_2025_09_15/)

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