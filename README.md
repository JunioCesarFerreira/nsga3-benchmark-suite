# nsga3-benchmark-suite
This repository provides a collection of Python implementations of the NSGA-III algorithm. The goal is to create a flexible and reproducible framework for systematic experiments and exhaustive comparisons of NSGA-III across different coding paradigms and libraries.

## Experiment 1
```py
NUM_OBJ = 2
NUM_VAR = 1
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
in my localhost:
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 3.329954
  mean_hv_elapsed_time: 0.000752
  mean_count_elapsed_time: 0.002248
  mean_analyze_elapsed_time: 0.000361
  mean_hypervolume: 0.413788
  coverage: 1.000000
  empty_ratio: 0.000000
  outside_rate: 0.000000
  entropy_norm: 0.914359
  gini: 3.857400
  chi2: 40.078400
  avg_active: 9.090909
  max_density: 19.980000
  std_density: 5.755045
  CUS: -2.857400

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.215610
  mean_hv_elapsed_time: 0.000763
  mean_count_elapsed_time: 0.002070
  mean_analyze_elapsed_time: 0.000345
  mean_hypervolume: 0.416761
  coverage: 1.000000
  empty_ratio: 0.000000
  outside_rate: 0.000000
  entropy_norm: 0.934055
  gini: 3.382800
  chi2: 31.931800
  avg_active: 9.000909
  max_density: 17.020000
  std_density: 5.110473
  CUS: -2.382800

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.447453
  mean_hv_elapsed_time: 0.000380
  mean_count_elapsed_time: 0.000315
  mean_analyze_elapsed_time: 0.000258
  mean_hypervolume: 0.388372
  coverage: 1.000000
  empty_ratio: 0.000000
  outside_rate: 0.000000
  entropy_norm: 1.000000
  gini: 0.000000
  chi2: 0.000000
  avg_active: 1.000000
  max_density: 1.000000
  std_density: 0.000000
  CUS: 1.000000
```

## Experiment 2
```py
NUM_OBJ = 3
NUM_VAR = 2
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 0.625505
  mean_hypervolume: 2.499829
  mean_points_in_r: 92.080000
  mean_points_out_r: 7.920000

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.065403
  mean_hypervolume: 1.917100
  mean_points_in_r: 100.000000
  mean_points_out_r: 0.000000

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.104636
  mean_hypervolume: 1.934488
  mean_points_in_r: 46.000000
  mean_points_out_r: 2.000000
```

## Experiment 3
```py
NUM_OBJ = 4
NUM_VAR = 3
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 0.680038
  mean_hypervolume: 29.120823
  mean_points_in_r: 98.010000
  mean_points_out_r: 1.990000

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.117443
  mean_hypervolume: 8.441090
  mean_points_in_r: 98.940000
  mean_points_out_r: 1.000000

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.112579
  mean_hypervolume: 73.406961
  mean_points_in_r: 117.000000
  mean_points_out_r: 4.000000
```

## Experiment 4
```py
NUM_OBJ = 4
NUM_VAR = 4
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 0.697056
  mean_hypervolume: 21.701992
  mean_points_in_r: 98.000000
  mean_points_out_r: 2.000000

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.116821
  mean_hypervolume: 2.275165
  mean_points_in_r: 52.900000
  mean_points_out_r: 11.020000

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.110262
  mean_hypervolume: 61.996564
  mean_points_in_r: 109.000000
  mean_points_out_r: 10.000000
```


## Experiment 5
```py
NUM_OBJ = 5
NUM_VAR = 4
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 0.826085
  mean_hypervolume: 112.311653
  mean_points_in_r: 92.950000
  mean_points_out_r: 7.050000

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.300050
  mean_hypervolume: 34.979089
  mean_points_in_r: 90.030000
  mean_points_out_r: 7.000000

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.139307
  mean_hypervolume: 434.260298
  mean_points_in_r: 138.000000
  mean_points_out_r: 2.000000
```


## Experiment 6
```py
NUM_OBJ = 6
NUM_VAR = 5
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```

```


## Experiment 7
```py
NUM_OBJ = 6
NUM_VAR = 14
NUM_GEN = 16
POP_SIZE = 100
DIVISIONS = 10
BOUNDS = [(0.0, 1.0)] * NUM_VAR # bounds to dtlz2
R = 0.15 # ~(pi/2)/DIVISIONS 
```
```
=== Summary of Results ===

Implementation: nsga3_func
  mean_elapsed_time: 1.154998
  mean_hypervolume: 19066.551006
  mean_points_in_r: 0.000000
  mean_points_out_r: 100.000000

Implementation: nsga3_deap_func
  mean_elapsed_time: 0.607317
  mean_hypervolume: 263.077361
  mean_points_in_r: 1.010000
  mean_points_out_r: 51.920000

Implementation: nsga3_pymoo_func
  mean_elapsed_time: 0.230685
  mean_hypervolume: 30831.357062
  mean_points_in_r: 1.000000
  mean_points_out_r: 129.000000
```