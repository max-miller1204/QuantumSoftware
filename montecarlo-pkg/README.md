# montecarlo

[![GitHub Actions Build Status](https://github.com/max-miller1204/montecarlo/workflows/CI/badge.svg)](https://github.com/max-miller1204/montecarlo/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/max-miller1204/montecarlo/branch/main/graph/badge.svg)](https://codecov.io/gh/max-miller1204/montecarlo/branch/main)
[![Documentation Status](https://readthedocs.org/projects/montecarlo-max-miller1204/badge/?version=latest)](https://montecarlo-max-miller1204.readthedocs.io/en/latest/?badge=latest)

A Python package for Monte Carlo simulation of Ising models on arbitrary graphs.

`montecarlo` provides:

- A `BitString` class for representing spin configurations.
- An `IsingHamiltonian` class for computing energies and exact thermodynamic
  averages (energy, magnetization, heat capacity, magnetic susceptibility).
- A `MonteCarlo` class implementing Metropolis sampling for systems too large
  to enumerate exactly.

## Installation

You will need an environment with the following packages:

- Python >= 3.8
- NumPy
- NetworkX

Clone the repository and install in development mode:

```sh
git clone https://github.com/max-miller1204/montecarlo.git
cd montecarlo
pip install -e .
```

## Basic usage

```python
import networkx as nx
import montecarlo

# Build a 6-site ring with uniform coupling J = 2.0
N = 6
G = nx.Graph()
G.add_nodes_from(range(N))
G.add_edges_from([(i, (i + 1) % N) for i in range(N)])
for e in G.edges:
    G.edges[e]['weight'] = 2.0

# Exact thermodynamic averages
ham = montecarlo.IsingHamiltonian(G)
E, M, HC, MS = ham.compute_average_values(T=1.0)
print(f"E = {E:.6f}, M = {M:.6f}, HC = {HC:.6f}, MS = {MS:.6f}")

# Metropolis sampling
mc = montecarlo.MonteCarlo(ham)
energies, magnetizations = mc.run(T=2.0, n_samples=10_000, n_burn=200)
```

See the [documentation](https://montecarlo-max-miller1204.readthedocs.io) for a full user
guide and API reference.

## Running the tests

```sh
pip install -e ".[test]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgements

Project structure based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms).

Copyright (c) 2026, Max Miller.
